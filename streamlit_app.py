import streamlit as st
import pandas as pd
import numpy as np

# API requests (n/a)
# Basic Webpage structure (n/a)
# Incorporate interactive elements (n/a)
# 2 chart elements (n/a)
# 1 map (n/a)
# 1 button widget (n/a)
# Checkbox widget (n/a)

# Subject to change
st.set_page_config(
    page_title="Weather App Tentative Title",
    layout="wide",
    menu_items= {
        'About' : "Welcome to your Weather Application!"
    }
)

st.title("Weather App")
st.header("Daily Forecast")