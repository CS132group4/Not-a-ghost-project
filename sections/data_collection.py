import streamlit as st
import pandas as pd
from scipy.stats import shapiro, spearmanr, wilcoxon, kruskal

def main():
    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 3px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;">Data Collection</h1>
    </div>
    """, unsafe_allow_html=True)

    df = pd.read_csv("Datasets/filtered_weather_data.csv")

    st.dataframe(df.head())

    # Remove missing values
    df = df.dropna()

    st.write("#### Missing Values")
    st.write(df.columns[df.isna().any()].tolist())

    # Convert to correct types
    df['main.temp'] = pd.to_numeric(df['main.temp'])
    df['main.feels_like'] = pd.to_numeric(df['main.feels_like'])
    df['main.humidity'] = pd.to_numeric(df['main.humidity'])

    # Convert datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Create useful columns
    df['hour'] = df['datetime'].dt.hour
    df['date'] = df['datetime'].dt.date

    # Define extreme heat
    df['extreme_heat'] = df['main.feels_like'] > 38

    st.markdown("#### Convert to Correct Types")
    st.code("""
        df['main.temp'] = pd.to_numeric(df['main.temp'])
        df['main.feels_like'] = pd.to_numeric(df['main.feels_like'])
        df['main.humidity'] = pd.to_numeric(df['main.humidity'])
            """)

    st.markdown("#### Convert datetime")
    st.code("""
        df['datetime'] = pd.to_datetime(df['datetime'])
            """)

    st.markdown("#### Create useful columns")
    st.code("""
        df['hour'] = df['datetime'].dt.hour
        df['date'] = df['datetime'].dt.date
            """)

    st.markdown("#### Define extreme heat")
    st.code("""
        df['extreme_heat'] = df['main.feels_like'] > 38
            """)