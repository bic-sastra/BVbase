import os
import sys
import base64
from PIL import Image
import time
import streamlit as st
import streamlit.components.v1 as components


db_path = sys.argv[1] if len(sys.argv) > 1 else "default.db"

# Run `search.py` with the database path as an argument using os.system
os.system(f"python search.py {db_path}")

st.set_page_config(page_title="PaVarDB", page_icon="🧬", layout="wide")



st.markdown(
    """
    <style>
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: white !important;
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
    </style>
    """,
    unsafe_allow_html=True
)


def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

bic_base64 = image_to_base64("bic.png")
sastra_base64 = image_to_base64("sastra.png")
mylogo_base64 = image_to_base64("pavardb.png")

  #  .title-banner {
  #      background: white;
   # padding: 4px 12px 8px 12px;  /* tighter padding on all sides */
    #    border-radius: 10px;
     #   box-shadow: 0 8px 16px rgba(0,0,0,0.1);
      #  border: 1px solid #e0e0e0;
       # max-width: 380px; 
   # }

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Comfortaa&display=swap');


    .header-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 200px;
        margin-top: 5px;
        margin-bottom: 10px;
        width: 100%;
    }

   
    .title-text {
        font-size: 45px;
        display: flex;
        align-items: baseline;
        line-height: 1;
    }

    .title-text span {
        display: inline-block;
        vertical-align: middle;
        padding: 0;
        margin: 0;
    }

    .pa {
        color: red;
        font-family: 'Caveat', cursive;
        font-weight: 600;
    }

    .var {
        color: green;
        font-family: 'Comfortaa', sans-serif;
        font-weight: 600;
    }

    .db {
        color: #007acc;
        font-family: 'Courier New', monospace;
        font-weight: 550;
    }

    .logo-standard {
        width: 110px;
        height: 130px;
        object-fit: contain;
    }

    .logo-tall {
        width: 380px;
        height: 110px;
        align-items: right;
        
    }
    
    .logo-short {
        width: 400px;
        height: 90px;
        
    }
    
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <img src="data:image/png;base64,{bic_base64}" class="logo-short">
        <div class="title-banner">
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{mylogo_base64}" class="logo-standard" style="border-radius: 50%;">
                <div style="margin-left: 1px;">
                    <div class="title-text" style="text-shadow: 1px 1px 2px #888888;">
                        <span class="pa">Pa</span><span class="var">Var</span><span class="db">DB</span>
                    </div>
                    <div class="title-text" style="font-weight: bold; font-size: 16px; color: #333; margin-top: -4px; text-shadow: 1px 1px 2px #888888;">
                        Genomic Variant Database
                    </div>
                </div>
            </div>
        </div>
        <img src="data:image/png;base64,{sastra_base64}" class="logo-tall">
    </div>
""", unsafe_allow_html=True)



st.markdown(
    """
    <style>
        .marquee-container {
            width: 100%;
            overflow: hidden;
            background-color: #007acc;
            padding: 6px 0;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .marquee-content {
            display: inline-block;
            white-space: nowrap;
            font-size: 28px;
            font-weight: 900;
            color: white;
            animation: scrollMarquee 30s linear infinite;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            padding-left: 100%;
        }

        @keyframes scrollMarquee {
            0%   { transform: translateX(0%); }
            100% { transform: translateX(-100%); }
        }
    </style>

    <div class="marquee-container">
        <div class="marquee-content"> Welcome to PaVarDB - Comprehensive Genomic Variant Database of <i>Pseudomonas aeruginosa</i>!</div>
    </div>
    """,
    unsafe_allow_html=True
)



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
        .stats-box {
            background-color: #f1f1f1;
            border-left: 6px solid #007acc;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            animation: slideUp 5s infinite;
            font-size: 22px;
        }

        .stats-title {
            font-size: 26px;
            font-weight: bold;
            color: #003366;
            margin-bottom: 10px;
            text-align: left;
        }

        .stats-box li {
            margin-bottom: 8px;
        }

        .intro-text {
            font-size: 24px; /* Increased paragraph font size */
            line-height: 1.6;
        }

        @keyframes slideUp {
            0% { transform: translateY(30px); opacity: 0.2; }
            50% { transform: translateY(0px); opacity: 1; }
            100% { transform: translateY(30px); opacity: 0.2; }
        }
    </style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown("""
    <div class="intro-text">
        <h3>Introduction</h3>
        <p>
        Antimicrobial resistance (AMR) has been identified by the World Health Organization (WHO) as one of the most critical global health threats. It results in reduced efficacy of antibiotics, thereby making the treatment of infections significantly more difficult. <i>Pseudomonas aeruginosa</i> represents a major challenge in the context of AMR due to its intrinsic and acquired resistance mechanisms, particularly in the treatment of bloodstream infections and respiratory tract infections.
        </p>
        <p>
        To support efforts in clinical decision-making and therapeutic development, the establishment of a comprehensive variant database is essential. This website provides access to a structured variant database designed for advanced genomic analysis and AMR research.
        </p>
        <h3>Features:</h3>
        <ul>
            <li><b>Search</b> for genetic variants and resistance profiles.</li>
            <li><b>Visualize</b> data using charts and graphs.</li>
            <li><b>Learn More</b> about the database and project in the About section.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-title">📈 PaVarDB Statistics</div>
        <ul>
            <li><b>Genomes: </b>  1506</li>
            <li><b>Geographical location: </b>  Asia</li>
            <li><b>Antibiotics: </b>  9</li>
            <li><b>Resistance: </b>  959</li>
            <li><b>Susceptible: </b>  700</li>
            <li><b>Intermediate: </b>  19</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
def get_base64_images(folder):
    images_base64 = []
    for img_name in sorted(os.listdir(folder)):
        if img_name.endswith(".jpg"):
            with open(os.path.join(folder, img_name), "rb") as f:
                data = base64.b64encode(f.read()).decode()
                images_base64.append(f"data:image/png;base64,{data}")
    return images_base64

chart_images = get_base64_images("charts")
amr_images = get_base64_images("images")

slideshow_html = f"""
<style>

.slideshow-header {{
    background-color: white;
    padding: 10px;
    border-radius: 10px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 15px;
    text-align: center;
}}

.container {{
    display: flex;
    justify-content: space-between;
    gap: 30px;
    width: 100%;
    margin-top: 25px;
}}

.left-panel, .right-panel {{
    flex: 1;
    border-radius: 15px;
    padding: 20px;
    background-color:white;
    box-shadow: 0 0 15px rgba(0,0,0,0.1);
    overflow: hidden;
    min-height: 690px;
    position: relative;
}}

.left-panel {{
    animation: slideLeftToRight 2s ease-out forwards;
}}

.right-panel {{
    animation: slideRightToLeft 2s ease-out forwards;
}}

@keyframes slideRightToLeft {{
    0% {{ transform: translateX(100%); opacity: 0; }}
    100% {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes slideLeftToRight {{
    0% {{ transform: translateX(-100%); opacity: 0; }}
    100% {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes fadeSlide {{
    0% {{ opacity: 0; transform: translateX(100px); }}
    100% {{ opacity: 1; transform: translateX(0); }}
}}

img {{
    max-width: 100%;
    max-width: 600px;
    max-height: 700px;

}}

.slide, .right-slide {{
    display: none;
    text-align: center;
    position: absolute;
    width: 100%;
    top: 80px;
    left: 0;
    animation: fadeSlide 1s ease-in-out;
}}

.slide img {{
    
    max-width: 730px;
    max-height: 720px;
     margin-top: 30px; /* Add this line to push the image down */
    margin-bottom: 15px;
    
}}

.right-slide img {{
    width: 100%;
    max-width: 1300px;
    max-height: 1300px;
     margin-top: 30px; /* Add this line to push the image down */
    margin-bottom: 5px;
    
}}

.slideshow-title {{
    text-align: left;
    font-size: 22px;
    font-weight: bold;
    color: #004d99;
    margin-bottom: 10px;
}}

.amr-description {{
    font-size: 16px;
    color: #333;
    line-height: 1.6;
    text-align: center;
    margin-bottom: 25px;
    padding: 0 10px;
}}
</style>

<div class="container">
    <!-- Left Slideshow Panel -->
    <div class="left-panel">
        <div class="slideshow-header">
    <div class="slideshow-title">PaVarDB Statistics</div>
  </div>
  <div class="slide-container">
"""

# Add chart images
for i, img in enumerate(chart_images):
    display = "block" if i == 0 else "none"
    slideshow_html += f"""
        <div class="slide" style="display: {display};">
            <img src="{img}" alt="Chart {i+1}">
        </div>
    """

slideshow_html += """
        </div>
    </div>

    <!-- Right Slideshow Panel -->
    <div class="right-panel">
         <div class="slideshow-header">
        <div class="slideshow-title">PaVarDB Schema</div>
    </div>
   
        <div class="slide-container">
"""

# Add AMR images
for i, img in enumerate(amr_images):
    display = "block" if i == 0 else "none"
    slideshow_html += f"""
        <div class="right-slide" style="display: {display};">
            <img src="{img}" alt="AMR Image {i+1}">
        </div>
    """

slideshow_html += """
        </div>
    </div>
</div>

<script>
function startSlideshow(className, interval=3000) {
    let index = 0;
    const slides = document.getElementsByClassName(className);

    function showSlides() {
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        index++;
        if (index > slides.length) { index = 1; }
        slides[index - 1].style.display = "block";
        setTimeout(showSlides, interval);
    }
    showSlides();
}

window.addEventListener('DOMContentLoaded', function() {
    startSlideshow("slide");
    startSlideshow("right-slide");
});
</script>
"""

# Display in Streamlit
components.html(slideshow_html, height=720)


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
        margin-top: 150px;
    }
    </style>

    <div class="footer-bar">
       Copyright © 2025 - Maintained by Bioinformatics Center (BIC), SASTRA Deemed University, Thanjavur, India.
    </div>
    """,
    unsafe_allow_html=True
)

