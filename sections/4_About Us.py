import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="About Us")
def main():
    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;">About Us</h1>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("About Us")
    st.markdown("#### WHO WE ARE")
    st.markdown(
        """
        <div style="
            border-left: 3px solid #D85A30;
            padding: 1.25rem 1.5rem;
            border-radius: 8px;
        ">
            <p style="font-size: 15px; line-height: 1.75">
            We're the team members of Not a Ghost Project. We're people who are interested
            in finding the reasons behind daily problems that Filipinos face, and what's a 
            more common experience in the Philippines than suffering through extreme heat?
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### THE TEAM")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("assets/team/Gabriel.jpg", use_container_width=True)
        st.subheader("Gabriel de Inigo")

    with col2:
        st.image("assets/team/Princessa.jpg", use_container_width=True)
        st.subheader("Princessa Gonzales")

    with col3:
        st.image("assets/team/Sam.jpg", use_container_width=True)
        st.subheader("Samantha Teng")