import streamlit as st

st.set_page_config(
    page_title="London Airbnb Dashboard",
    page_icon="🏠",
    layout="wide"
)

pg = st.navigation([
    st.Page(
        "pages/01_overview.py",
        title="How do Airbnb listings compare across London?",
        icon="🏠"
    ),
    st.Page(
        "pages/02_compare.py",
        title="What explains the price differences?",
        icon="📊"
    ),
])

pg.run()