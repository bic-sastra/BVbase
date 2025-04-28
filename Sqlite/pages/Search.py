import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import sys

# **Clear caches to reduce RAM usage**
st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(page_title="Search Variants", page_icon="", layout="wide")

# Get path from command-line arguments (provided by home.py)
db_path = sys.argv[1] if len(sys.argv) > 1 else "default.db"

# ---- Custom Styling ----
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #d6e8db;
        color: black;
    }
    [data-testid="stSidebar"] * {
        font-size: 18px !important;
        font-weight: bold !important;
        color: black !important;
    }
    section[data-testid="stSidebar"] .stSelectbox div, 
    section[data-testid="stSidebar"] .stMultiSelect div {
        font-size: 18px !important;
    }
    .stSelectbox, .stMultiSelect {
        font-size: 18px !important;
        padding: 10px !important;
    }
    div[role="listbox"] > div {
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 18px !important;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .dataframe {
        font-size: 16px !important;
    }
    .element-container:has(.dataframe) {
        max-height: 600px;
        overflow: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Database connection ----
def get_db_connection():
    return sqlite3.connect(db_path)

print(f"Connected to database: {db_path}")

def get_filter_options():
    conn = get_db_connection()
    try:
        filters = {
            "Geographic Group": pd.read_sql("SELECT DISTINCT geographic_group FROM strains", conn)["geographic_group"].dropna().tolist(),
            "Isolation Country": pd.read_sql("SELECT DISTINCT isolation_country FROM strains", conn)["isolation_country"].dropna().tolist(),
            "Phenotype": pd.read_sql("SELECT DISTINCT resistant_phenotype FROM strains", conn)["resistant_phenotype"].dropna().tolist(),
            "Antibiotic": pd.read_sql("SELECT DISTINCT antibiotic FROM strains", conn)["antibiotic"].dropna().tolist(),
            "Strain Name": pd.read_sql("SELECT DISTINCT genome_name FROM strains", conn)["genome_name"].dropna().tolist(),
            "Gene Name": pd.read_sql("SELECT DISTINCT gene_name FROM variants", conn)["gene_name"].dropna().tolist(),
        }
    except Exception as e:
        st.error(f"Error fetching filter options: {e}")
        filters = {}
    finally:
        conn.close()
    return filters

filter_options = get_filter_options()
print("Filter options loaded:", filter_options)

def get_filtered_data(filters):
    conn = get_db_connection()
    query = """
        SELECT DISTINCT s.genome_id, s.sra_accession, s.genome_name, s.antibiotic, s.resistant_phenotype, 
                        s.geographic_group, s.isolation_country,
                        v.ref_strain, v.chromosome, v.position, v.ref, v.alt, v.allele, v.qual, 
                        v.gene_name, v.gene_id, v.feature_type, v.feature_id, v.biotype, v.rank, 
                        v.annotation_type, v.annotation_impact, v.aa_change, v.hgvs_p, v.aa_pos_length, 
                        v.hgvs_c, v.cdna_pos_length
        FROM variants v
        JOIN strains s ON s.genome_id = v.genome_id
        WHERE 1=1
    """
    
    params = []
    filter_map = {
        "s.geographic_group": filters.get("Geographic Group", []),
        "s.isolation_country": filters.get("Isolation Country", []),
        "s.resistant_phenotype": filters.get("Phenotype", []),
        "s.antibiotic": filters.get("Antibiotic", []),
        "v.gene_name": filters.get("Gene Name", []),
    }

    for column, values in filter_map.items():
        if values:
            placeholders = ",".join(["?"] * len(values))
            query += f" AND {column} IN ({placeholders})"
            params.extend(values)

    print("\n🔍 SQL Query:")
    print(query)
    print(" Parameters:", params)

    try:
        df = pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    
    return df

# ---- UI Elements ----
st.title(" Search for Variants")

# Sidebar Filters
st.sidebar.header("Filters")
selected_filters = {}
filter_mode = st.sidebar.radio("Choose Filter Mode", ["Region Based Search", "Phenotype Based Search"])

if filter_mode == "Region Based Search":
    selected_filters["Geographic Group"] = [st.sidebar.selectbox("Geographic Group*", [""] + filter_options.get("Geographic Group", []))]
    selected_filters["Isolation Country"] = [st.sidebar.selectbox("Isolation Country*", [""] + filter_options.get("Isolation Country", []))]
    selected_filters["Phenotype"] = st.sidebar.multiselect("Phenotype", filter_options.get("Phenotype", []))
    selected_filters["Antibiotic"] = [st.sidebar.selectbox("Antibiotic*", [""] + filter_options.get("Antibiotic", []))]
    selected_filters["Gene Name"] = st.sidebar.multiselect("Gene Name", filter_options.get("Gene Name", []))
else:
    selected_filters["Phenotype"] = [st.sidebar.selectbox("Phenotype*", [""] + filter_options.get("Phenotype", []))]
    selected_filters["Antibiotic"] = [st.sidebar.selectbox("Antibiotic*", [""] + filter_options.get("Antibiotic", []))]
    selected_filters["Geographic Group"] = [st.sidebar.selectbox("Geographic Group*", [""] + filter_options.get("Geographic Group", []))]
    selected_filters["Isolation Country"] = st.sidebar.multiselect("Isolation Country", filter_options.get("Isolation Country", []))
    selected_filters["Gene Name"] = st.sidebar.multiselect("Gene Name", filter_options.get("Gene Name", []))


# ---- Apply Filters ----
if st.sidebar.button("Apply Filters"):
    with st.spinner("Running query... Please wait."):
        data = get_filtered_data(selected_filters)

    if data.empty:
        st.warning("No records found for the selected filters.")
    else:
        st.session_state["filtered_data"] = data
        st.success("Filters applied successfully!")

# ---- Display Table and Visualizations if Available ----
if "filtered_data" in st.session_state:
    data = st.session_state["filtered_data"]

    # Create two columns
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        st.write("### Filtered Results")

    with col2:
        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_results.csv",
            mime="text/csv"
        )

    st.dataframe(data)

    # ---- Statistics ----
    total_cases = len(data)
    resistant_cases = len(data[data["resistant_phenotype"] == "Resistant"])
    susceptible_cases = len(data[data["resistant_phenotype"] == "Susceptible"])
    total_genes = data["gene_name"].nunique()
    antibiotic_counts = data["antibiotic"].value_counts()
    country_counts = data["isolation_country"].value_counts()
    gene_counts = data["gene_name"].value_counts().head(3)
    aa_counts = data["aa_change"].value_counts().head(3)
    phenotype_counts = data["resistant_phenotype"].value_counts()

    formatted_genes = ", ".join([f"{gene} ({count})" for gene, count in gene_counts.items()])
    formatted_aa_changes = ", ".join([f"{aa} ({count})" for aa, count in aa_counts.items()])
    formatted_antibiotics = ", ".join([f"{ab} ({count})" for ab, count in antibiotic_counts.items()])

    st.markdown(f"""
    ###  Statistics
    **Total Data**  : {total_cases}  

    **Phenotype Distribution** :  
    **Resistant** : {resistant_cases}  
    **Susceptible** : {susceptible_cases}  

    **Total Genes Count**: {total_genes}  

    **Top 3 Identified Genes** :  
    {formatted_genes}  

    **Top 3 Amino Acid Changes** :  
    {formatted_aa_changes}  

    **Antibiotic Counts** :  
    {formatted_antibiotics}  
    """)

   # --- Visualization Section ---
    st.markdown("### Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        if not gene_counts.empty:
            fig, ax = plt.subplots(figsize=(5, 4))
            gene_counts.plot(kind="bar", ax=ax, color="green", edgecolor="black")
            ax.set_title("Top 3 Genes")
            st.pyplot(fig)

    with col2:
        if not aa_counts.empty:
            fig, ax = plt.subplots(figsize=(5, 4))
            aa_counts.plot(kind="bar", ax=ax, color="blue", edgecolor="black")
            ax.set_title("Top 3 Amino Acid Changes")
            st.pyplot(fig)

    with col1:
        if not phenotype_counts.empty:
            fig, ax = plt.subplots(figsize=(5, 4))
            phenotype_counts.plot(kind="bar", ax=ax, color=["yellow", "red"], edgecolor="black")
            ax.set_title("Resistant vs Susceptible")
            st.pyplot(fig)

    with col2:
        if not country_counts.empty:
            fig, ax = plt.subplots(figsize=(5, 4))
            country_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, cmap="tab20")
            ax.set_title("Country-wise Distribution")
            st.pyplot(fig)

    with col1:
        if not antibiotic_counts.empty:
            fig, ax = plt.subplots(figsize=(5, 4))
            antibiotic_counts.head(10).plot(kind="bar", ax=ax, color="orange", edgecolor="black")
            ax.set_title("Antibiotics")
            ax.set_xlabel("Antibiotic", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)
            ax.tick_params(axis="x", rotation=90, labelsize=8)
            st.pyplot(fig)

st.markdown(
    """
    <style>
    .footer-bar {
        width: 100%;
        background-color: #d6e8db;
        text-align: center;
        padding: 4px 8px;  /* Reduced padding */
        font-size: 16px;
        font-weight: bold;
        border-top: 1px solid #ccc;
        color: #000;
        margin-top: 700px;  /* Reduced margin */
    }
    </style>

    <div class="footer-bar">
        © 2025 - Maintained by <strong>Bioinformatics Center (BIC)</strong>, <strong>SASTRA Deemed University</strong>, Thanjavur, India.
    </div>
    """,
    unsafe_allow_html=True
)

