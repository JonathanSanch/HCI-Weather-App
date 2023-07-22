import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# API requests (n/a)
# Basic Webpage structure (n/a)
# Incorporate interactive elements (n/a)
# 2 chart elements (n/a)
# 1 map (n/a)
# 1 button widget (n/a)
# Checkbox widget (n/a)
# Going to have 'about' section, 'home', and 'settings'
# About

# Subject to change
st.set_page_config(
    page_title="Weather App Tentative Title",
    page_icon = "⛅️",
    layout="wide",
    menu_items= {
        'About' : "Welcome to your Weather Application!",
        'Get help' : "https://docs.streamlit.io/",
        'Report a bug' : "https://github.com/JonathanSanch/HCI-Weather-App"
    }
)

# Injecting the CSS for the form
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

st.title("Weather App ⛅️")
st.write("---")


add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ["Homepage", "Preferences", "Contact Us"]
)

if add_selectbox == "Preferences":
    st.header("Preferences")

# ---- CONTACT ----
elif add_selectbox == "Contact Us":
    with st.container():
        st.header("Contact Us")
        left, right = st.columns(2)
        with left:
            contact_form = """
            <form action="https://formsubmit.co/jonsanchezcs@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """

            st.markdown(contact_form, unsafe_allow_html=True)
        with right:
            st.empty()

        st.text("")
        agree = st.checkbox('I agree to possibly receive a response email')

        if agree:
            st.write('Thank you for your feedback!')


else:
    st.sidebar.success("Please provide your location to receive today's forecast!")
    st.header("Daily Forecast")
    t = datetime.now().strftime("%H:%M:%S")
    st.caption("Current time is: " + t)

    # Comment of Weather Emojis for adding to forecast later☀️ 🌤 ⛅️ 🌥 ☁️ 🌦 🌧 ⛈ 🌩 🌨 ❄️

    # This section is to be updated to interact with the cities API provides
    st.info('You must select a city in order to receive a forecast.', icon="ℹ️")
    option = st.selectbox(
        'Where are you located?',
        ('','Miami', 'Orlando', 'New York', 'Los Angeles', 'Dallas')
    )

    # After this, probably include logic to display the city's forecast information for the day
    st.write('You selected:', option)











