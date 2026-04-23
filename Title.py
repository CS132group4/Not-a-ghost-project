import streamlit as st
import pandas as pd

st.title("# Not a Ghost Project")

st.write("Made as a requirement for the CS 132 Final Project")

st.sidebar.success("Select a page.")

st.markdown(
    """
    The Philippines has historically achieved record-high numbers of extreme heat events. In this project,
    we want to find out the relationships between actual and perceived temperature, the frequency and duration
    of extreme heat stress events in an observed period, which combinations of temperature and humidity result in 
    the highest levels of heat stress, and find out if heat stress severity varies significantly across different
    cities, and if perceived temperature can better explain these differences than air temperature alone. 
"""
)