import streamlit as st
import plotly.express as px
from utils import load_data, sidebar_filters

df, p95 = load_data()
filtered = sidebar_filters(df, p95)

st.header("How do Airbnb listings compare across London?")
st.caption("Overview of London Airbnb listings after removing extreme price outliers.")

col1, col2, col3 = st.columns(3)

col1.metric("Listings", len(filtered))
col2.metric("Average Price", f"£{filtered['price'].mean():.0f}")
col3.metric("Neighbourhoods", filtered["neighbourhood"].nunique())

st.divider()

# BBD CATEGORICAL colour
fig = px.scatter(
    filtered,
    x="reviews_per_month",
    y="price",
    color="room_type",
    hover_name="neighbourhood",
    title="Listings with more reviews are not always the most expensive"
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12)
)

st.plotly_chart(fig, use_container_width=True)