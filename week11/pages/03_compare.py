import streamlit as st
import plotly.graph_objects as go
from utils import load_gapminder

df = load_gapminder()

st.header("What explains the differences between countries?")
st.caption("Compare GDP per Capita and Life Expectancy across countries.")

# Session state
if "highlight_country" not in st.session_state:
    st.session_state.highlight_country = df["Country"].iloc[0]

countries = sorted(df["Country"].unique())

st.session_state.highlight_country = st.selectbox(
    "Highlight a country",
    countries,
    index=countries.index(st.session_state.highlight_country)
)

highlight = st.session_state.highlight_country

highlight_continent = df.loc[
    df["Country"] == highlight,
    "Continent"
].values[0]

tab1, tab2 = st.tabs(
    ["GDP vs Life Expectancy", "Continent Comparison"]
)

with tab1:

    colors = [
        "#E63946" if c == highlight else "#DDDDDD"
        for c in df["Country"]
    ]

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=df["GDP_per_capita"],
            y=df["Life_expectancy"],
            mode="markers",
            marker=dict(
                color=colors,
                size=10,
                opacity=0.85
            ),
            text=df["Country"],
            hovertemplate="%{text}<extra></extra>"
        )
    )

    row = df[df["Country"] == highlight].iloc[0]

    fig1.add_annotation(
        x=row["GDP_per_capita"],
        y=row["Life_expectancy"],
        text=f"<b>{highlight}</b>",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-30
    )

    fig1.update_xaxes(
        type="log",
        title="GDP per Capita"
    )

    fig1.update_yaxes(
        title="Life Expectancy"
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig1, use_container_width=True)

with tab2:

    continent_df = (
        df[df["Continent"] == highlight_continent]
        .sort_values("Life_expectancy")
    )

    colors2 = [
        "#E63946" if c == highlight else "#2E75B6"
        for c in continent_df["Country"]
    ]

    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            x=continent_df["Life_expectancy"],
            y=continent_df["Country"],
            orientation="h",
            marker_color=colors2
        )
    )

    fig2.update_layout(
        title=f"{highlight} compared with other countries in {highlight_continent}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Life Expectancy",
        yaxis_title=""
    )

    st.plotly_chart(fig2, use_container_width=True)