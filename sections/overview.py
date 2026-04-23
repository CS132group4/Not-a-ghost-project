import streamlit as st
import pandas as pd

def main():

    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 3px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;"> Overview </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        text-align:center;
        max-width:750px;
        margin: 0 auto;
        line-height:1.6;
        font-size:16px;
    ">
    The Philippines has historically achieved record-high numbers of extreme heat events. In this project, we want to find the relationships between actual and perceived temperature, the frequency and duration of extreme heat stress events in an observed period, 
    which combinations of temperature and humidity result in the highest levels of heat stress, and whether heat stress severity varies significantly across different cities, and if perceived temperature can better explain these differences than air temperature alone.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:800px; margin: 30px auto 0 auto;">
        <h2>Objectives</h2>
        <ul style="text-align:left; display:inline-block;">
            <li>To compare actual temperature and perceived temperature during extreme heat events</li>
            <li>To examine the effect of humidity on heat stress intensity</li>
            <li>To analyze temporal patterns and trends in heat stress over the study period</li>
            <li>To evaluate differences in heat stress exposure across cities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

