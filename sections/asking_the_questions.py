import streamlit as st

def main():
    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 3px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;">Asking the Questions</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1: 
        st.markdown("#### Research Questions")

        st.markdown("""
        1. How do actual temperature and perceived temperature differ during extreme heat conditions?
        2. What is the frequency and duration of extreme heat stress events within the observed period?
        3. Which combinations of temperature and humidity result in the highest levels of heat stress?
        4. Does heat stress severity vary significantly across different cities, and can perceived temperature better explain these differences than air temperature alone
        """)
    with col2: 
        st.markdown("#### Research Hypotheses")

        st.markdown(
        """
        1. Higher Humidity levels significantly increase perceived heat stress even when actual air temperature remains constant.
        2. Perceived temperature is significantly higher than actual air temperature during high humidity conditions.
        3. Perceived temperature is a better indicator of climate extremes than air temperature alone.
        4. Heat stress severity differs significantly across cities due to varying climate action.
    """
    )