import streamlit as st
import plotly.express as px
from utils import load_gapminder

df = load_gapminder()

st.header("How do life expectancy and GDP compare across continents?")

with st.sidebar:
    st.header("Filters")

    continents = st.multiselect(
        "Continent",
        sorted(df["Continent"].unique()),
        default=sorted(df["Continent"].unique())
    )

    metric = st.radio(
        "Metric",
        ["Life Expectancy", "GDP per Capita"]
    )

if not continents:
    st.warning("Select at least one continent.")
    st.stop()

filtered = df[df["Continent"].isin(continents)]

y_col = "Life_expectancy" if metric == "Life Expectancy" else "GDP_per_capita"

avg = (
    filtered
    .groupby("Continent")[y_col]
    .mean()
    .reset_index()
)

# BBD CATEGORICAL colour
fig = px.bar(
    avg,
    x="Continent",
    y=y_col,
    color="Continent",
    title=f"Average {metric} by continent"
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12),
    yaxis=dict(gridcolor="#EEEEEE"),
    xaxis=dict(showgrid=False)
)

st.plotly_chart(fig, use_container_width=True)