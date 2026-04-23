import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("Datasets/filtered_weather_data.csv")
    df = df.dropna()
    df['main.temp'] = pd.to_numeric(df['main.temp'])
    df['main.feels_like'] = pd.to_numeric(df['main.feels_like'])
    df['main.humidity'] = pd.to_numeric(df['main.humidity'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['date'] = df['datetime'].dt.date
    df['extreme_heat'] = df['main.feels_like'] > 38
    return df

df = load_data()