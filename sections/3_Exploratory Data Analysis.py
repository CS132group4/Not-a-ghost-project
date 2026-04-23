import streamlit as st
from utils import load_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import shapiro, spearmanr, wilcoxon, kruskal

def main():

    st.set_page_config(page_title="Exploratory Data Analysis")

    st.sidebar.header("Exploratory Data Analysis")

    st.title("Exploratory Data Analysis")

    df = load_data()

    st.markdown("### Summary Statistics")
    st.dataframe(df.describe())

    st.markdown("#### Missing Values")
    st.write(df.isna().sum())

    st.markdown("### Understanding Distributions")
    df_num = ['main.temp','main.humidity','main.feels_like']
    st.markdown("#### Numerical Feature Summary:")
    st.write(df[df_num].describe())

    st.markdown("### Pairplot")
    pairplot = sns.pairplot(df[['main.temp','main.humidity','main.feels_like']])
    st.pyplot(pairplot)

    st.markdown("### Histograms")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))


    for ax, feat in zip(axes, df_num):
        ax.hist(df[feat], bins=30, edgecolor='white')
        ax.set_title(feat)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

    plt.suptitle('Distribution of Temperature Features')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""Based on the histograms, main.temp appears to follow a roughly bell shaped distribution with slight skewness, 
                suggesting it is close to normal but not perfect symmetric.In contrast, main.humdity shows a negatively skewed 
                distribution, with mosy values concentrated at higher lavels, indicating a clear deviation from normality. 
                Meanwhile, main.feels_like exhibits an irregular and non symmetic shape, further suggesting that it does not follow 
                a normal distribution""")

    with st.echo():
        results = []
        for feat in df_num:
            sample = df[feat].dropna()

            if len(sample) > 5000:
                sample = sample.sample(5000, random_state=42)

            stat, p_value = shapiro(sample)
            results.append((feat,stat,p_value))
    for feat,stat,p_value in results:
        st.write(f"**{feat}**")
        st.write(f"Statistic: {stat:.4f}, P-value: {p_value:.6f}")
        st.write("Result:", "Approximately Normal" if p_value > 0.05 else "Not Normal")
        
    st.markdown("### Data Visualization")
    st.markdown("#### RQ1: Actual vs Perceived Temperature")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='main.temp', y='main.feels_like', alpha=0.5, ax=ax)
    plt.plot([15,40],[15,40], linestyle='--')
    plt.title("Actual vs Perceived Temperature")
    plt.xlabel("Actual Temperature")
    plt.ylabel("Feels Like Temperature")
    st.pyplot(fig)

    st.markdown("#### RQ2: Frequency of Extreme Heat Events")
    fig, ax = plt.subplots()
    sns.countplot(data=df[df['extreme_heat']], x='hour')
    plt.title("Frequency of Extreme Heat Events")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    st.pyplot(fig)

    st.markdown("#### RQ3: Temperature and Humidity vs Heat Stress")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df,
        x='main.temp',
        y='main.humidity',
        hue='main.feels_like'
    )
    plt.title("Temperature and Humidity vs Heat Stress")
    st.pyplot(fig)

    st.markdown("#### RQ4: Heat Stress Across Cities")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.boxplot(data=df, x='city_name', y='main.feels_like')
    plt.xticks(rotation=90)
    plt.title("Heat Stress Across Cities")

    st.pyplot(fig)

    st.markdown("#### Nutshell Plot")
    fig, ax = plt.subplots(figsize=(12,8))

    # Base scatter (soft background)
    sns.scatterplot(
        data=df,
        x='main.temp',
        y='main.feels_like',
        alpha=0.12,
        color='gray',
        label='Normal Conditions'
    )

    # Highlight extreme heat
    sns.scatterplot(
        data=df[df['extreme_heat']],
        x='main.temp',
        y='main.feels_like',
        color='red',
        s=60,
        label='Extreme Heat'
    )

    # Identity line (baseline: feels_like = temp)
    x_vals = np.linspace(df['main.temp'].min(), df['main.temp'].max(), 100)
    plt.plot(x_vals, x_vals, linestyle='--', linewidth=2, label='Feels = Actual')

    # Heat stress zone
    plt.fill_between(
        x_vals,
        x_vals,
        x_vals + 5,
        color='orange',
        alpha=0.25,
        label='Heat Stress Zone (+5°C)'
    )

    # EXTREME HEAT THRESHOLD LINE
    threshold = df['main.feels_like'].quantile(0.90)

    plt.axhline(
        y=threshold,
        linestyle='-',
        linewidth=2,
        color='darkred',
        label=f'Extreme Heat Threshold ({threshold:.1f}°C)'
    )

    # Add vertical reference (optional but strong)
    plt.axvline(
        x=threshold,
        linestyle=':',
        linewidth=2,
        color='purple',
        label='Critical Temperature Level'
    )

    #  Annotation (storytelling)
    plt.text(
        0.02, 0.96,
        "Humidity amplifies heat:\nwhat you feel is often worse than reality",
        transform=plt.gca().transAxes,
        fontsize=13,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none')
    )

    # Highlight the most extreme point
    max_point = df.loc[df['main.feels_like'].idxmax()]
    plt.scatter(
        max_point['main.temp'],
        max_point['main.feels_like'],
        color='black',
        s=80,
        zorder=5
    )

    plt.annotate(
        "Peak Heat Stress",
        (max_point['main.temp'], max_point['main.feels_like']),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=10,
        arrowprops=dict(arrowstyle='->')
    )

    # Titles & labels
    plt.title("When Heat Feels Worse: Humidity Pushes Temperatures Into Dangerous Zones", fontsize=15)
    plt.xlabel("Actual Temperature (°C)")
    plt.ylabel("Feels Like Temperature (°C)")

    plt.legend()
    plt.grid(alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("### Hypothesis Testing")
    st.markdown("#### Hypothesis 1: Humidity increases heat stress")
    with st.echo():
        corr, p = spearmanr(df['main.humidity'], df['main.feels_like'])
    st.write(f"Correlation: {corr:.4f}, p-value: {p: .4f}")
    st.markdown("#### Hypothesis 2: Feels like temperature is greater than the actual temprearure")
    with st.echo():
        stat, p = wilcoxon(df['main.feels_like'], df['main.temp'])
    st.write(f"p-value: {p: .4f}")
    st.markdown("#### Hypothesis 3: Perceived temperature is a better indicator of climate extremes than air temperature alone")
    with st.echo():
        threshold = df['main.temp'].quantile(0.90)
        df['extreme'] = (df['main.temp'] >= threshold).astype(int)
        corr_temp, p_temp = spearmanr(df['main.temp'], df['extreme'])
        corr_feels, p_feels = spearmanr(df['main.feels_like'], df['extreme'])
    st.write("#### Correlation with Extreme Conditions")
    st.write(f"Temp → Corr: {corr_temp: .4f}, p-value: {p_temp: .6f}")
    st.write(f"Feels Like → Corr: {corr_feels: .4f}, p-value: {p_feels: .6f}")
    if abs(corr_feels) > abs(corr_temp):
        st.write("**Conclusion:** `feels_like` is a better indicator of climate extremes.")
    else:
        st.write("**Conclusion:** `temp` is a better indicator of climate extremes.")
    st.markdown("#### Hypothesis 4: Heat stress severity differs significantly across cities due to varying climate action")
    with st.echo():
        groups = [g['main.feels_like'].values for _, g in df.groupby('city_name')]
        stat, p = kruskal(*groups)
    st.write(f"p-value: {p: .4f}")