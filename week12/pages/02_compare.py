import streamlit as st
import plotly.express as px

from utils import load_data, sidebar_filters

df, p95 = load_data()
filtered = sidebar_filters(df, p95)

st.header("What explains the price differences?")
st.caption("Compare prices across room types and neighbourhoods.")

tab1, tab2 = st.tabs(["Room Types", "Neighbourhoods"])

with tab1:
    # BBD CATEGORICAL colour
    fig1 = px.box(
        filtered,
        x="room_type",
        y="price",
        color="room_type",
        title="Entire homes generally cost more than private or shared rooms"
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12)
    )

    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    avg = (
        filtered.groupby("neighbourhood", as_index=False)["price"]
        .mean()
        .sort_values("price")
    )

    # BBD SEQUENTIAL colour
    fig2 = px.bar(
        avg,
        x="price",
        y="neighbourhood",
        orientation="h",
        color="price",
        color_continuous_scale="Blues",
        title="Average Airbnb prices vary by neighbourhood"
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12)
    )

    st.plotly_chart(fig2, use_container_width=True)