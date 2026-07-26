
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌱", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌱 CO2 Emissions Explorer")
st.caption("Source: Our World in Data — ourworldindata.org/co2-emissions")

# ── TASK 1: Sidebar with 5 widgets ────────────────────────────────────────────
#   a) st.selectbox for Region (with 'All')
#   b) st.multiselect for Countries (updates based on region — chained)
#   c) st.date_input for date range (two-handle; convert years to Jan-1 dates)
#   d) st.radio for Metric: "Total CO2 (Mt)" vs "CO2 per capita"
#   e) st.checkbox labelled "Show only top emitter highlighted"
#
# Guards:
#   - empty countries → st.warning + st.stop()
#   - incomplete date_input → st.warning + st.stop()
# Convert date_input result to pd.Timestamp before filtering.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    # Region
    regions = ["All"] + sorted(df["Region"].unique())
    selected_region = st.selectbox("Region", regions)

    # Countries (chained to region)
    if selected_region == "All":
        country_list = sorted(df["Country"].unique())
    else:
        country_list = sorted(
            df[df["Region"] == selected_region]["Country"].unique()
        )

    selected_countries = st.multiselect(
        "Countries",
        country_list,
        default=country_list[:5]
    )

    if len(selected_countries) == 0:
        st.warning("Please select at least one country.")
        st.stop()

    # Date range
    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) != 2:
        st.warning("Please select a complete date range.")
        st.stop()

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    # Metric
    metric = st.radio(
        "Metric",
        ["Total CO2 (Mt)", "CO2 per capita"]
    )

    # Highlight checkbox
    highlight = st.checkbox("Show only top emitter highlighted")


filtered = df[
    (df["Country"].isin(selected_countries)) &
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
]

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]


# ── TASK 2: Filter summary caption ────────────────────────────────────────────
# Show: "X countries | Region | Date range | Metric"
# BBD rule: always show users how many records match current filters
# ─────────────────────────────────────────────────────────────────────────────
st.caption(
    f"{filtered['Country'].nunique()} countries | "
    f"{selected_region} | "
    f"{start_date.year} - {end_date.year} | "
    f"{metric}"
)


# ── TASK 3: Two charts reacting to ALL filters ────────────────────────────────
#   Left: line chart — selected metric over time, one line per country
#         If "Show only top emitter highlighted" checkbox is on:
#           - grey all lines except the highest emitter in the date range
#           - label that country at the end of its line (SWD grey-and-highlight)
#   Right: bar chart — ranking for the last year in selected date range
#
# BBD colour requirement: name the colour type in a comment next to each chart
# SWD requirements: white background, insight title, use_container_width=True
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    # Line chart
    metric_col = "CO2_Mt" if metric == "Total CO2 (Mt)" else "CO2_per_capita"

    # COLOUR TYPE: highlight
    if highlight:
        totals = filtered.groupby("Country")[metric_col].sum()
        top_country = totals.idxmax()

        fig_line = px.line(
            filtered,
            x="Date",
            y=metric_col,
            color="Country",
            color_discrete_map={
                c: ("royalblue" if c == top_country else "lightgray")
                for c in filtered["Country"].unique()
            },
            title="Emission trends reveal the highest emitter over time"
        )
    else:
        # COLOUR TYPE: categorical
        fig_line = px.line(
            filtered,
            x="Date",
            y=metric_col,
            color="Country",
            title="Emission trends over time"
        )

    fig_line.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial")
    )

    st.plotly_chart(fig_line, use_container_width=True)
    pass

with col_right:
    # Bar chart
    latest = filtered[filtered["Date"] == filtered["Date"].max()]
    latest = latest.sort_values(metric_col, ascending=False)

    # COLOUR TYPE: sequential
    fig_bar = px.bar(
        latest,
        x=metric_col,
        y="Country",
        orientation="h",
        color=metric_col,
        color_continuous_scale="Blues",
        title="Latest year ranking of emissions"
    )

    fig_bar.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial")
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    pass


# ── EXTENSION: KPI row above the charts ───────────────────────────────────────
#   - Total CO2 in last year of selected range (sum across selected countries)
#   - % change from first to last year
#   - Country with highest emissions in last year
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE (optional)