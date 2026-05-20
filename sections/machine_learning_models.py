import streamlit as st
from utils import load_data, load_january_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler


@st.cache_data
def compute_silhouette_scores(df):
    n_numbers = list(range(2,16))
    avg_scores = []
    for n_cluster in n_numbers:
        clusterer=KMeans(n_clusters=n_cluster, random_state=10, n_init='auto')
        cluster_labels = clusterer.fit_predict(df)
        silhouette_avg = silhouette_score(df, cluster_labels)
        avg_scores.append(silhouette_avg)
    return n_numbers, avg_scores

@st.cache_resource
def fit_prophet(prophet_df, periods):
    m=Prophet(
            daily_seasonality=True,
            yearly_seasonality=False,
            interval_width=0.95
        )
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=periods, freq='h')
    forecast=m.predict(future)
    return m, forecast
    
@st.cache_data
def build_city_agg(df):
    city_agg = df.groupby('city_name').agg(
        mean_temp        = ('main.temp', 'mean'),
        mean_feels_like  = ('main.feels_like', 'mean'),
        mean_humidity    = ('main.humidity', 'mean'),
        pct_extreme      = ('extreme_heat', 'mean'),
    ).reset_index()

    city_agg['humidity_gap'] = city_agg['mean_feels_like'] - city_agg['mean_temp']
    return city_agg


def main():
    st.markdown("""
    <div style="
        background-image: linear-gradient(135deg, #BA7517 0%, #D85A30 50%, #993C1D 100%);
        padding: 3px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    ">
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;"> Machine Learning Models</h1>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    january_df = load_january_data()

    st.markdown("## Machine Learning Models")
    st.markdown("Similar to the data in previous sections, these models are trained on " \
    "October to December data, which in the Philippines is a rather cool season. Hence, " \
    "these models learned patterns from a relatively mild period and not the months with" \
    " the highest mean temperatures. These prototypes demonstrate that the perceived " \
    "temperatures follow daily patterns and that cities can be clustered into distinct " \
    "heat stress profiles. Extending the dataset to cover a year would significantly " \
    "improve the model's utility for real-world heat advisory applications in the Philippines")
    st.write("### Perceived Temperature Predictor")
    city = st.selectbox("Select a city", sorted(df['city_name'].unique()))
    prophet_df = df[df['city_name'] == city][['datetime', 'main.feels_like']].rename(columns={'datetime': 'ds', 'main.feels_like': 'y'})
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds']).dt.tz_localize(None)
    prophet_df = (
    prophet_df.set_index('ds')
        .resample('h')['y']
        .mean()
        .reset_index()
        .dropna()
    )

    january_city_df = january_df[january_df['city_name'] == city][['datetime', 'main.feels_like']].rename(columns={'datetime': 'ds', 'main.feels_like': 'actual'})
    january_city_df['ds'] = pd.to_datetime(january_city_df['ds']).dt.tz_localize(None)
    january_city_df = (
    january_city_df.set_index('ds')
        .resample('h')['actual']
        .mean()
        .reset_index()
        .dropna()
    )
    with st.spinner(f"Forecasting feels-like temperature for {city}..."):
        m, forecast = fit_prophet(prophet_df, periods=744)

    forecast_future = forecast[ forecast['ds'] >= january_city_df['ds'].min()]
    comparison = forecast_future.merge(january_city_df, on="ds", how="inner")
    comparison['error'] = (comparison['actual'] - comparison['yhat'])
    comparison['mae'] = comparison['error'].abs()

    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(
        comparison['ds'],
        comparison['actual'],
        label='Actual January 2026'
    )

    ax.plot(
        comparison['ds'],
        comparison['yhat'],
        label='Predicted',
        linestyle='--'
    )

    ax.fill_between(
        comparison['ds'],
        comparison['yhat_lower'],
        comparison['yhat_upper'],
        alpha=0.2
    )

    ax.axhline(
        38,
        color='red',
        linestyle=':',
        label='Extreme Heat Threshold'
    )
    ax.set_title(f"Forecast vs Actual - {city}")
    ax.legend()
    st.pyplot(fig, clear_figure=True)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "MAE",
        f"{comparison['mae'].mean():.2f}°C"
    )

    col2.metric(
        "RMSE",
        f"{np.sqrt((comparison['error']**2).mean()):.2f}°C"
    )

    col3.metric(
        "Max Error",
        f"{comparison['mae'].max():.2f}°C"
    )

    st.dataframe(comparison[['ds', 'actual', 'yhat', 'yhat_lower', 'yhat_upper']])
    
    st.markdown("These predictions were made with the use of Prophet, a time series forecasting library developed by Meta. " \
    "Evaluated against actual January data, it demonstrates that daily perceived weather is predictable, helping normal " \
    "Filipino citizens see what time the perceived temperature typically peaks during the month of January. This helps " \
    "people know what temperature to expect in each of these cities and prepare accordingly.")

    st.write("### K-Means Clustering of Cities")
    city_agg = build_city_agg(df)

    features = ['mean_temp', 'mean_feels_like', 'mean_humidity', 'pct_extreme', 'humidity_gap']
    k_means_df= city_agg[features]
    scaler = StandardScaler()
    k_means_scaled = scaler.fit_transform(k_means_df)

    #k_means_df = k_means_df.sample(5000, random_state=10)

    
    with st.spinner("Computing silhouette scores..."):
        n_numbers, avg_scores = compute_silhouette_scores(k_means_scaled)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(n_numbers, avg_scores, marker='o', linestyle='-', color='b')
    ax.set_title("Average Silhouette Scores for Different Cluster Counts")
    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Average Silhouette Score")
    ax.grid(True)
    st.pyplot(fig)
    

    kmeans = KMeans(n_clusters = 3, random_state=10, n_init='auto')
    city_agg['Cluster']= kmeans.fit_predict(k_means_scaled)

    st.write("#### Mean values per cluster")
    st.dataframe(city_agg.groupby('Cluster')[features].mean())
    
    st.markdown("From what we can see among the 3 clusters, cluster 1 is the highest heat stress" \
    " group, with the highest mean actual and perceived temperature and frequency of extreme heat events. " \
    "Meanwhile, cluster 2 is the coolest group, with zero recorded extreme heat events and the lowest" \
    " mean actual and perceived temperature. Finaly, cluster 0 is the middle ground with moderate actual " \
    "and perceived heat and humidity.")

    st.write("#### Cities per cluster")
    st.dataframe(city_agg[['city_name', 'Cluster'] + features].sort_values('Cluster'))
    st.markdown("This list shows which cities belong to which cluster, helping ordinary Filipinos know " \
    "what to expect when visiting one of these cities, and help them prepare accordingly. This is perfect " \
    "for helping people plan outings, trips, and events during the last quarter of the year.")



