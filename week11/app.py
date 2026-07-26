import streamlit as st

st.set_page_config(
    page_title="Gapminder Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Gapminder Dashboard")

st.markdown("""
### Welcome!

Use the navigation menu on the left to explore:

- 📊 Overview
- 📈 Trends
- ⚖️ Compare Countries

This dashboard uses the Gapminder dataset.
""")