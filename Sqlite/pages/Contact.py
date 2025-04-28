import streamlit as st

st.set_page_config(page_title="Contact", layout="wide")


st.markdown(
    """
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
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("""
<style>
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
    font-size: 24px;
    color: #000;
}
.big-title {
    font-size: 26px;
    font-weight: bold;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# Page title
st.title("Contact")

st.markdown(
    """
    <style>
    .info-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05);
        font-size: 22px; 
    }
    .info-box h4 {
        margin-bottom: 10px;
        font-size: 26px;
        color: #333;
        border-bottom: 1px solid #ccc;
        padding-bottom: 5px;
    }

    </style>

    <div class="info-box">
        <h4>Developer</h4>
        Virudhagiri E<br>
        125121031, MSc Bioinformatics<br>
        DBT-Bioinformatics Center<br>
        School of Chemical & Biotechnology<br>
        SASTRA Deemed University
    </div>

    <div class="info-box">
        <h4>Research Advisor</h4>
        Dr. Vigneshwar Ramakrishnan <br>
        Professor<br>
        DBT-Bioinformatics Center<br>
        School of Chemical & Biotechnology<br>
        SASTRA Deemed University
    </div>


    <div class="info-box">
        <h4>Contact</h4>
        Mail ID: bic@sastra.ac.in
    </div>

 
    """,
    unsafe_allow_html=True
)


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

