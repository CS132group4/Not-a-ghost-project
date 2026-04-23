import streamlit as st

def main():
    st.set_page_config(page_title="Asking the Questions")

    st.sidebar.header("Asking the Questions")

    st.title("Asking the Questions")

    st.markdown(
        """
        Research Questions
        1. How do actual temperature and perceived temperature differ during extreme heat conditions?
        2. What is the frequency and duration of extreme heat stress events within the observed period?
        3. Which combinations of temperature and humidity result in the highest levels of heat stress?
        4. Does heat stress severity vary significantly across different cities, and can perceived temperature better explain these differences than air temperature alone
        
        Research Hypotheses
        1. Higher Humidity levels significantly increase perceived heat stress even when actual air temperature remains constant.
        2. Perceived temperature is significantly higher than actual air temperature during high humidity conditions.
        3. Perceived temperature is a better indicator of climate extremes than air temperature alone.
        4. Heat stress severity differs significantly across cities due to varying climate action.

        Objectives
        1. To compare actual temperature and perceived temperature during extreme heat events
        2. To examine the effect of humidity on heat stress intensity
        3. To analyze temporal patterns and trends in heat stress over the study period
        4. To evaluate differences in heat stress exposure across cities
    """
    )