import streamlit as st
import base64
import sections.asking_the_questions as q
import sections.data_collection as d
import sections.exploratory_data_analysis as e
import sections.about_us as a
import sections.overview as o

st.set_page_config(layout="wide")


def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("assets/about/header.jpg")

st.markdown(f"""
            
<div class="main">
    <div class="main-title">
        Not A Ghost Project: Analysis of Climate Extremes and Heat Stress Using Meteorological Data
    </div>
</div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;600&display=swap');
            
html, body {{
    font-family: 'Inter', sans-serif;
}}
            
[data-testid="stAppViewContainer"] {{
    background-color: #000000 !important;
}}

section.main {{
    background-color: #000000 !important;
}}

div.block-container {{
    background-color: #000000 !important;
}}

html, body, p, h1, h2, h3, h4, h5, h6 {{
    color: white !important;
}}
            
/* header  */
.main {{
    position: relative;
    width: 100%;
    height: 220px;
    margin-bottom: 15px;
    border-radius: 12px;
    overflow: hidden;

    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center 67%;
}}

.main::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.35);
}}

.main-title {{
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    
    font-size: 40px;
    font-weight: 800;
    color: white;
    text-align: center;
    
    z-index: 2;
    text-shadow: 0px 2px 10px rgba(0,0,0,0.6);
    width: 100%;
}}

/* Tabs */
div[data-testid="stTabs"] {{
    position: sticky;
    top: 0;
    z-index: 9999;
    background: #111;
    padding-top: 0.5rem;
}}

button[data-baseweb="tab"] {{
    padding: 10px 18px !important;
    color: white !important;
}}

button[data-baseweb="tab"] > div > p {{
    font-size: 18px !important;
    color: white !important;
    font-weight: 600 !important;
}}

button[aria-selected="true"] {{
    background: #333 !important;
    border-radius: 8px 8px 0 0 !important;
}}

/* text */
h1 {{font-size: 40px !important;}}
h2 {{font-size: 30px !important;}}
h3 {{font-size: 24px !important;}}
h4 {{font-size: 20px !important;}}
h5 {{font-size: 18px !important;}}
h6 {{font-size: 16px !important;}}

header[data-testid="stHeader"] {{
    display: none;
}}

/* Fix markdown specifically */
.stMarkdown, .stMarkdown p {{
    color: white !important;
}}

/* Optional: make secondary text less gray */
[data-testid="stCaption"] {{
    color: #cccccc !important;
}}

</style>
""", unsafe_allow_html=True)


tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Overview", "Questions", "Collection", "Exploration", "Team"
])

with tab0:
    o.main()
with tab1:
    q.main()
with tab2:
    d.main()
with tab3:
    e.main()
with tab4:
    a.main()