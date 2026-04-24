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

    st.write('#### Data Downloading')
    st.markdown("We downloaded our data from Kaggle, from the following link: https://www.kaggle.com/datasets/bwandowando/philippine-major-cities-weather-data-2025?fbclid=IwY2xjawRX-2RleHRuA2FlbQIxMQBzcnRjBmFwcF9pZAEwAAEe1PKwmgA4w9SV8pSPF3ggW0bzYflUzjHxJbwldW2yjvhRT2KHUiv2EEsoVcM_aem_EJhDXl6vQYVPqlbN8a5V9g")
    st.code('''
        df = pd.read_excel("Datasets/Combinedcsv.xlsx")    
''', language="python")
    
    st.markdown("Then, we keep only the columns needed for your research, removing all other columns")
    st.code('''
        df = df[[
        "datetime",
        "main.temp",
        "main.humidity",
        "main.feels_like",
        "city_name"
    ]]
''', language="python")
    st.markdown("Then, we selected a number of cities of random cities to keep, deleting the rest")
    st.code('''
    cities = [
    "Angeles City",
    "Antipolo",
    "Baguio",
    "Batangas City",
    "BiÃ±an",
    "Cabanatuan City",
    "Calamba",
    "Caloocan City",
    "Dagupan",
    "DasmariÃ±as",
    "Legazpi City",
    "Lucena",
    "Makati City",
    "Manila",
    "Quezon City",

    "Bacolod",
    "Bais",
    "Baybay",
    "Bogo",
    "Borongan",
    "Cadiz",
    "Calbayog City",
    "Catbalogan",
    "Cebu City",
    "Dumaguete",
    "Iloilo City",
    "Lapu-Lapu City",
    "Ormoc",
    "Tacloban City",
    "Toledo City",

    "Butuan",
    "Cabadbaran",
    "Cagayan de Oro",
    "Davao",
    "Digos",
    "Dipolog",
    "General Santos",
    "Gingoog City",
    "Iligan City",
    "Kidapawan",
    "Koronadal",
    "Malaybalay",
    "Pagadian",
    "Surigao City",
    "Zamboanga City"
]

filtered_df = df[df["city_name"].isin(cities)]''', language="python")
    
    st.markdown("Then, we turned the modified dataframe to a csv")

    st.code('''filtered_df.to_csv("filtered_weather_data.csv", index=False)

from google.colab import files
files.download("filtered_weather_data.csv")''', language="python")
    
    st.markdown("#### Data Cleaning")
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
            """, language="python")

    st.markdown("#### Convert datetime")
    st.code("""
        df['datetime'] = pd.to_datetime(df['datetime'])
            """, language="python")

    st.markdown("#### Create useful columns")
    st.code("""
        df['hour'] = df['datetime'].dt.hour
        df['date'] = df['datetime'].dt.date
            """, language="python")

    st.markdown("#### Define extreme heat")
    st.code("""
        df['extreme_heat'] = df['main.feels_like'] > 38
            """, language="python")
    
    text = (
    "A temperature threshold of **38°C** was selected because temperatures at or above this level are associated with significant heat stress and increased risk of heat-related illnesses, especially in tropical countries like the Philippines where humidity is high.\n Although PAGASA heat warnings are primarily based on the heat index, actual air temperatures nearing **38°C** can already produce dangerous “feels like” conditions when combined with humidity.\n The human body normally maintains an internal temperature around **37°C**.\n When environmental temperatures approach or exceed this level, the body becomes less efficient at cooling itself through sweating and evaporation. As a result, prolonged exposure may lead to dehydration, heat exhaustion, or heat stroke.\n In tropical environments, an actual temperature of: **38°C** often corresponds to a much higher heat index because high humidity reduces evaporative cooling. PAGASA classifies heat index values beginning at: **42°C** as Danger, where heat cramps and heat exhaustion become likely. Thus, using 38C as a threshold is justified because: it represents an extreme environmental temperature, it is near the body's thermal regulation limit, and under Philippine humidity conditions it frequently produces dangerous apparent temperatures."
)
    st.markdown(text)
    st.write("### Sources")
    st.markdown('''https://www.pagasa.dost.gov.ph/weather/heat-index
https://www.weather.gov/ama/heatindex''')