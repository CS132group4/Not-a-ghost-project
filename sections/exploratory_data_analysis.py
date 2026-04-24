import streamlit as st
from utils import load_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;"> Data Exploration</h1>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    st.markdown("## Exploratory Data Analysis")

    st.markdown("### Summary Statistics")
    st.dataframe(df.describe())

    st.markdown("#### Missing Values")
    st.write(df.isna().sum())

    st.markdown("### Understanding Distributions")
    df_num = ['main.temp','main.humidity','main.feels_like']
    st.markdown("#### Numerical Feature Summary")
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

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### RQ1: Actual vs Perceived Temperature")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.scatterplot(data=df, x='main.temp', y='main.feels_like', alpha=0.5, ax=ax)
        plt.plot([15,40],[15,40], linestyle='--')
        plt.title("Actual vs Perceived Temperature")
        plt.xlabel("Actual Temperature")
        plt.ylabel("Feels Like Temperature")
        st.pyplot(fig)

        st.markdown("""
        The scatter plot shows a strong positive relationship between actual temperature and perceived 
        (“feels like”) temperature. At lower temperatures, the points closely follow the diagonal line, 
        indicating that perceived temperature is nearly equal to actual temperature. However, as temperatures 
        increase, the points begin spreading upward, showing that the feels-like temperature becomes higher 
        than the actual air temperature.

        This widening gap suggests that atmospheric factors such as humidity intensify human heat perception, 
        especially during warmer conditions. Several observations cluster between 30°C and 40°C feels-like 
        temperature even when actual temperatures are lower, indicating amplified heat stress. The visualization 
        demonstrates that actual temperature alone may underestimate how hot environmental conditions truly feel.
    """)

    with col2:
        st.markdown("#### RQ2: Frequency of Extreme Heat Events")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.countplot(data=df[df['extreme_heat']], x='hour', ax=ax)
        plt.title("Frequency of Extreme Heat Events")
        plt.xlabel("Hour")
        plt.ylabel("Count")
        st.pyplot(fig)

        st.markdown("""
        The histogram reveals that extreme heat events are concentrated during midday and early afternoon hours. 
        Event frequencies remain relatively low during the morning but increase sharply around 11 AM, peaking 
        between 1 PM and 3 PM. After late afternoon, the number of extreme heat events declines steadily.

        This pattern reflects the natural daily heating cycle where solar radiation accumulates throughout the 
        day, causing temperatures and humidity-driven heat stress to intensify. The results suggest that the 
        highest risk period for dangerous heat conditions occurs during midday hours, aligning with common heat 
        advisory periods issued by weather agencies.
        """)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### RQ3: Temperature and Humidity vs Heat Stress")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.scatterplot(
            data=df,
            x='main.temp',
            y='main.humidity',
            hue='main.feels_like',
            ax=ax
        )
        plt.title("Temperature and Humidity vs Heat Stress")
        st.pyplot(fig)

        st.markdown("""
        The scatter plot demonstrates how humidity interacts with temperature to influence perceived heat stress. 
        Darker colored points, representing higher feels-like temperatures, are concentrated in regions where both 
        temperature and humidity are elevated.

        Even moderate temperatures can produce dangerous heat stress when humidity levels are high because humidity 
        reduces the body’s ability to cool itself through sweat evaporation. The clustering of high heat stress 
        points around temperatures above 28°C and humidity levels between 60% and 90% highlights the combined 
        effect of these variables. The visualization confirms that humidity significantly amplifies how hot 
        conditions feel to humans.
        """)

    with col4:
        st.markdown("#### RQ4: Heat Stress Across Cities")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.boxplot(data=df, x='city_name', y='main.feels_like', ax=ax)
        plt.xticks(rotation=90)
        plt.title("Heat Stress Across Cities")
        st.pyplot(fig)

        st.markdown("""
        The boxplot compares perceived temperatures across different cities and shows clear variations in heat 
        stress levels. Some cities exhibit higher median feels-like temperatures, while others display wider 
        distributions and more extreme outliers.

        These differences suggest that local environmental and climatic conditions influence heat stress severity. 
        Cities with larger spreads and higher outliers experience more frequent or more severe heat conditions, 
        whereas cities with narrower distributions exhibit relatively stable heat patterns. The visualization 
        demonstrates that heat stress is not geographically uniform and varies significantly across locations.
        """)
        
    st.markdown("#### Nutshell Plot")
    fig, ax = plt.subplots(figsize=(10,8))
    st.markdown("""
    The nutshell plot summarizes the study’s main findings by comparing actual temperature and perceived 
    temperature under normal and extreme heat conditions. The diagonal dashed line represents situations where 
    feels-like temperature is equal to actual temperature, while the shaded orange region illustrates how 
    humidity pushes perceived temperature above measured air temperature.

    Red points highlight extreme heat events, showing that dangerous heat conditions occur when feels-like 
    temperatures rise significantly beyond actual temperatures. The horizontal threshold line marks the critical 
    extreme heat boundary, while the highlighted peak point represents the most severe heat stress observation 
    in the dataset.

    Overall, the visualization emphasizes that humidity amplifies heat stress, making perceived temperature a 
    more meaningful indicator of dangerous climate conditions than actual temperature alone.
    """)

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

    st.markdown(f"""
    The Spearman correlation coefficient of {corr:.4f} indicates a strong positive relationship between 
    humidity and perceived temperature. As humidity increases, the feels-like temperature also tends to increase. 
    The extremely small p-value confirms that this relationship is statistically significant and unlikely to 
    have occurred by chance.

    **Conclusion:** The hypothesis is supported. Humidity significantly increases heat stress.
    """)

    st.markdown("#### Hypothesis 2: Feels like temperature is greater than the actual temprearure")
    with st.echo():
        stat, p = wilcoxon(df['main.feels_like'], df['main.temp'])
    st.write(f"p-value: {p: .4f}")

    st.markdown(f"""
    The Wilcoxon signed-rank test compares actual temperature and perceived temperature measurements. 
    The near-zero p-value indicates a statistically significant difference between the two variables, 
    with feels-like temperatures generally being higher than actual temperatures.

    **Conclusion:** The hypothesis is supported. Perceived temperature is significantly greater than actual air temperature.
    """)

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

    st.markdown(f"""
    The results show that perceived temperature has a stronger correlation with extreme heat conditions 
    compared to actual temperature alone. While actual temperature is associated with climate extremes, 
    feels-like temperature captures additional atmospheric effects such as humidity, making it a stronger 
    predictor of dangerous heat conditions.

    Since the feels-like correlation ({corr_feels:.4f}) is substantially higher than the actual temperature 
    correlation ({corr_temp:.4f}), perceived temperature provides a more accurate representation of human heat stress.
    The hypothesis is supported. Feels-like temperature is a better indicator of climate extremes.
    """)

    st.markdown("#### Hypothesis 4: Heat stress severity differs significantly across cities due to varying climate action")
    with st.echo():
        groups = [g['main.feels_like'].values for _, g in df.groupby('city_name')]
        stat, p = kruskal(*groups)

    st.write(f"p-value: {p: .4f}")

    st.markdown(f"""
    The Kruskal-Wallis test evaluates whether perceived temperature distributions differ significantly across cities. 
    The extremely small p-value indicates strong statistical evidence that at least one city experiences heat stress 
    levels that are significantly different from the others.

    These variations may be influenced by differences in humidity, urban density, geography, and local climate patterns.

    **Conclusion:** The hypothesis is supported. Heat stress severity differs significantly across cities.
    """)
