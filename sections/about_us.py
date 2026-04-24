import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="About Us")

BASE_DIR = Path(__file__).resolve().parent.parent

# to load image
def img_to_base64(path):
    full_path = BASE_DIR / path

    if not full_path.exists():
        st.error(f"Image not found: {full_path}")
        return ""

    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def team_card(img_path, name):
    img_base64 = img_to_base64(img_path)

    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 100%;
    ">
        <div style="
            width: 300px;
            height: 300px;
            overflow: hidden;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        ">
            <img src="data:image/jpg;base64,{img_base64}" style="
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            ">
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='text-align:center; font-size:25px; font-weight:600; margin-top:10px;'>{name}</p>", unsafe_allow_html=True)

def main():

    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1 style="font-size: 42px; color: white; margin: 0;">About Us</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>Who We Are</h2>", unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center; max-width:750px; margin:auto; line-height:1.6;">
                
    As Computer Science students in the Philippines, we are driven by curiosity in how data and technology can be used to better understand real-world environmental challenges. Our team is particularly interested in applying computational methods to analyze climate-related phenomena, especially those that directly affect daily life in the Philippines.
    By combining data analysis with environmental insights, we hope to better understand patterns of extreme heat and contribute to more informed discussions on climate awareness and resilience. We continue to develop our skills in data analysis and problem-solving while utilizing technology to turn data into meaningful understanding of the world around us.
        
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; margin-top:40px;'>The Team</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        team_card("assets/team/Gabriel.jpg", "Gabriel De Guzman")

    with col2:
        team_card("assets/team/Princessa.jpg", "Princessa Gonzales")

    with col3:
        team_card("assets/team/Sam.jpg", "Samantha Teng")

    st.write("Made as a requirement for the CS 132 Final Project (WFX AY 2025-2026 2nd Sem)")
