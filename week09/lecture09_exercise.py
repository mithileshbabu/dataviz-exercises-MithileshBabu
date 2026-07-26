"""
Lecture 9 Exercise — World Happiness Dashboard
================================================
Run with: streamlit run lecture09_exercise.py

Dashboard purpose (REQUIRED — write this before any code):
# PURPOSE: [one sentence: audience + what they can do with this dashboard]

BBD colour rule: name the colour type you use in a comment next to each chart:
# COLOUR TYPE: sequential / diverging / categorical / highlight
"""

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.set_page_config(page_title="World Happiness Dashboard", page_icon="🌍", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Title and caption
# ─────────────────────────────────────────────────────────────────────────────
st.title("🌍 World Happiness Dashboard")

st.caption(
    "Explore global happiness scores by region and compare countries using interactive visualizations."
)
# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: Sidebar filters
#   - st.selectbox for Region ('All' option)
#   - st.slider for top N countries (5-30, default 15)
# Filter the dataframe. Store as `filtered`.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    regions = ["All"] + sorted(df["Region"].unique().tolist())

    selected_region = st.selectbox(
        "Select Region",
        regions
    )

    top_n = st.slider(
        "Top N Countries",
        min_value=5,
        max_value=30,
        value=15
    )
if selected_region == "All":
    filtered = df.copy()
else:
    filtered = df[df["Region"] == selected_region]

filtered = filtered.sort_values("Score", ascending=False).head(top_n)


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: KPI row — 3 st.metric() cards
#   1. Number of countries shown
#   2. Average score (with delta vs global average)
#   3. Happiest country in current selection
# ─────────────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

global_avg = df["Score"].mean()
avg_score = filtered["Score"].mean()

with col1:
    st.metric(
        "Countries Shown",
        len(filtered)
    )

with col2:
    st.metric(
        "Average Score",
        f"{avg_score:.2f}",
        delta=f"{avg_score - global_avg:.2f}"
    )

with col3:
    happiest_country = filtered.iloc[0]["Country"]
    st.metric(
        "Happiest Country",
        happiest_country
    )


st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Two-column layout — two charts
#   Left (wider): horizontal bar of top N countries, sorted by score
#   Right: scatter of GDP vs Score
#
# BBD colour requirement:
#   - Name the colour type you chose (sequential/diverging/categorical/highlight)
#     in a comment next to the colour argument
#   - Do NOT use red and green as the only differentiator (CVD rule)
#
# SWD requirements:
#   - White background, Arial font
#   - Bar chart x-axis starts at 0
#   - Insight title (not topic title)
#   - use_container_width=True
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    fig_bar = px.bar(
        filtered.sort_values("Score", ascending=True),
        x="Score",
        y="Country",
        orientation="h",
        color="Score",
        color_continuous_scale="Blues",  # Sequential colour scale
        title="Countries with the highest happiness scores in the selected group"
    )

    fig_bar.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial")
    )

    fig_bar.update_xaxes(range=[0, filtered["Score"].max() + 1])

    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    fig_scatter = px.scatter(
        filtered,
        x="GDP",
        y="Score",
        color="Region",  # Categorical colour scale
        hover_name="Country",
        title="Higher GDP generally corresponds to higher happiness"
    )

    fig_scatter.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial")
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# EXTENSION: Add a third chart of your choice using a DIVERGING colour scale
# (something where values go above and below a meaningful midpoint)
# Label the midpoint in an annotation.
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE (optional)
