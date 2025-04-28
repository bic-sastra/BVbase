import streamlit as st
import base64
# Set up the page configuration
st.set_page_config(page_title="About", layout="wide")

# Custom CSS for general page styling
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #d6e8db;
        color: black;
    }

    /* Make sidebar text bold and black */
    [data-testid="stSidebar"] * {
             font-size: 20px;
        font-weight: bold;
        color: #000000;
    }

    /* Info box styling */
    .info-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Styling for page content */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background: white;
        height: 100%;
        margin: 0;
        padding: 0;
    }

    [data-testid="stHeader"] {
        background: transparent;
        height: 0;
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    .block-container {
        padding-top: 0rem;
    }

    .big-text {
        font-size: 22px;
        color: #000;
    }

    .big-title {
        font-size: 26px;
        font-weight: bold;
        color: #000000;
    }

    /* Footer styling */
    .footer-bar {
        width: 100%;
        background-color: #d6e8db;
        text-align: center;
        padding: 4px 8px;  /* Reduced padding */
        font-size: 13px;
        font-weight: bold;  /* Bold text */
        border-top: 1px solid #ccc;
        color: #000;
        margin-top: 00px;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.title(" About PaVarDB")

def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

encoded_image = get_base64_image("image/db_structure.jpg")
encoded_image1 = get_base64_image("image/search_schema.jpg")
st.markdown(f"""
<div class="big-text">
<p>
PaVarDB is a comprehensive database of genomic variants in <i>Pseudomonas aeruginosa</i>, providing valuable information for clinical studies.
</p>

<!-- Features Section -->
<div class="section-title big-title">Features</div>
<div class="info-box">
    <p>➣ Shows variant data along with resistance phenotype and country information.</p>
    <p>➣ Provides visualizations of gene counts and amino acid changes.</p>
    <p>➣ Allows users to filter data interactively based on country, antibiotics, strains, genes, and phenotype.</p>
    <p>➣ Users can download CSV reports and charts for offline use.</p>
</div>

<!-- Technologies Used Section -->
<div class="section-title big-title">Technologies Used</div>
<div class="info-box">
    <p>PaVarDB utilizes the Nextflow pipeline, which incorporates bioinformatics tools like Fastp, Snippy, SnpEff, VCFtools, BCFtools, Samtools, and custom bash scripts. The pipeline  uses Python to generate an SQLite database. It is adaptable for any bacterial species and can produce annotated VCF and CSV files. To use the pipeline, visit our GitHub repository and follow the manual instructions to download and customize the tools for your specific bacterial species.</p>
    <p><a href="https://github.com/bic-sastra/Pa_var_db" target="_blank">Visit our GitHub repository here</a></p>
</div>

<!-- PaVarDB Database Schema -->
<div class="section-title big-title">PaVarDB Database Schema</div>
<div class="info-box">
    <p>

The PaVarDB database schema is designed to efficiently store and manage genomic variant data in the context of antimicrobial resistance (AMR). It consists of two relational tables: Strains and Variants, which are connected through a composite key consisting of Genome_id and Sra_accession. The Strains table has metadata associated with each bacterial genome, including its geographic origin (isolation_country, geographic_group), taxonomic identifier (taxon_id), genome-specific information (genome_name), the antibiotic  (antibiotic), and its observed phenotype (resistant_phenotype). This table uses several indexes to enhance query performance, specifically on fields like geographical_group, isolation_country, antibiotic, resistant_phenotype, and genome_name.

The Variants table stores detailed information about each genomic variant detected in the strains. Each record in this table is linked to the corresponding strain via the shared Genome_id and Sra_accession. The table includes variant-specific attributes such as the chromosome location (chromosome, position), reference and alternate alleles (ref, alt), quality scores (qual), and alleles. It also has annotation information including the gene name and ID, feature type and ID, biotype, variant effect (annotation_type, annotation_impact), and various sequence-level annotations like HGVS notations (hgvs_c, hgvs_p) and amino acid changes (aa_change). The schema supports detailed analysis by also including position and length data for cDNA, CDS, and amino acid changes, as well as reference strain information and also this schema enables a comprehensive representation of strain-level genomic variations and facilitates complex queries linking phenotype, geography, gene function, and variant effects—critical for AMR research. The relational design and indexed fields ensure high performance and scalability for large-scale multi-strain datasets.</p>
<img src="data:jpg;base64,{encoded_image}" alt="Database Structure" style="width:60%;border-radius:10px;margin-top:10px;display:block;margin-left:auto;margin-right:auto;" />

</div>

<!-- PaVarDB Search Schema and Approaches -->
<div class="section-title big-title">PaVarDB Search Schema and Approaches</div>
<div class="info-box">
    <p>The PaVarDB search system has two main ways to search: Region-Based Search and Phenotype-Based Search. These help users find important information related to clinical studies and antimicrobial resistance more easily. In both methods, some search fields are mandatory (shown in yellow), and some are optional (shown in green).

In Region-Based Search, users must enter the Geographical Location, Isolation Country, and Antibiotic. These help narrow down the search to a specific region and antibiotic resistance. Users can also choose to add Gene Name or Phenotypes to get more specific results.
In Phenotype-Based Search, the focus is on whether the bacteria are resistant or susceptible to antibiotics. The required fields are Geographical Location, Phenotypes, and Antibiotic and also users can  include Gene Name and Isolation Country to refine the search further.

This simple and flexible search system allows users to explore data from either a regional view or based on resistance , making it useful for researchers and clinical studies.</p>
    <img src="data:jpg;base64,{encoded_image1}" alt="Search Schema" style="width:60%;border-radius:10px;margin-top:10px;display:block;margin-left:auto;margin-right:auto;" />

</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .footer-bar {
        width: 100%;
        background-color: #d6e8db;
        text-align: center;
        padding: 4px 8px;  /* Reduced padding */
        font-size: 16px;
        font-weight: bold;  /* Bold text */
        border-top: 1px solid #ccc;
        color: #000;
        margin-top: 100px;
    }
    </style>

    <div class="footer-bar">
       Copyright © 2025 - Maintained by Bioinformatics Center (BIC), SASTRA Deemed University, Thanjavur, India.
    </div>
    """,
    unsafe_allow_html=True
)



