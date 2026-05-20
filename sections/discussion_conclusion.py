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
                <h1 style="font-size: 42px; color: white; margin-bottom: 0.5rem;">Discussion and Conclusion</h1>
    </div>
    """, unsafe_allow_html=True)

   
    st.markdown("#### Discussion")

    st.markdown("""
        Based on the visualizations and analyses, the findings show that heat stress is
        influenced by multiple environmental factors, particularly temperature, humidity,
        time of day, and geographic location. A strong positive relationship exits between
        actual and perceived temperature, with the latter becoming significantly higher than
        the former during hotter weather. This indicates that factors like humidity amplifies
        human heat perception and can make moderate temperatures feel hot.

        The results also show that extreme heat events occur most frequently during midday
        and early afternoon hours, reflecting daily heat patterns and identifying periods of
        greatest heat risk. Another significant factor in the differences in perceived temperatures
        is location, demonstrating that heat stress is not geographically uniform among cities.
                
        
    """)

    st.markdown("#### Conclusion")

    st.markdown("""
        Overall, the findings support all proposed hypotheses and demonstrate that perceived temperature
        is a more effective indicator of heat stress than actual air temperature alone. The machine
        learning models further reinforced these findings by predicting daily heat patterns and grouping
        cities into distinct clusters with different heat stress profiles.
                
        Citizens living in the Philippines are no stranger to occurrences of heat events. These events, while common in the country,
        pose serious risks to citizens' health. They can cause conditions like heat stress and heat stroke, aggravate chronic
        illnesses, and have an even higher risk to vulnerable groups like children or the elderly. Hence, tracking the factors that
        are associated with extreme heat events is vital to the Filipino community. Learning which cities, which times, and what factors
        are typically associated with these dangerous heat conditions can help the public better prepare for daily heat-related risks. 
    """)
   