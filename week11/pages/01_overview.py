import streamlit as st
import plotly.express as px
from utils import load_gapminder

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

df = load_gapminder()

st.header("How does quality of life vary around the world?")

st.write("This page provides an overview of the Gapminder dataset.")

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Countries", df["Country"].nunique())
col2.metric("Population", f"{df['Population'].sum():,}")
col3.metric("Continents", df["Continent"].nunique())

st.divider()

fig = px.scatter(
    df,
    x="GDP_per_capita",
    y="Life_expectancy",
    size="Population",
    color="Continent",
    hover_name="Country",
    log_x=True,
    title="Countries with higher GDP per capita generally have higher life expectancy"
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial")
)

st.plotly_chart(fig, use_container_width=True)