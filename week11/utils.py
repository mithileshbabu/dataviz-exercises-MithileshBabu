import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_gapminder():
    path = Path(__file__).parent.parent / "data" / "gapminder.csv"
    df = pd.read_csv(path)
    return df