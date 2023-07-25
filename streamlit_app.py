import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import requests

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
    page_title="Weather Forecast",
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

def getGeolocationCity(city):
    file = open("WeatherAPI_keys.json")
    json_file = json.load(file)
    # st.write(type(file), type(json_file))
    api_key = json_file["openWeather"]
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city + "&limit=5&appid=" + api_key
    response = requests.get(url).json()
    # st.write(response)
    cityName = response[0]["name"]
    latitude = round(response[0]["lat"], 2)  # rounding latitude info from API to two decimal and storing in variable
    longitude = round(response[0]["lon"], 2)  # rounding longitude info from API to two decimal and storing in variable
    # st.write(cityName)
    # st.write("The Geolocation of " + cityName + " is: " + str(latitude) + ", " + str(longitude))
    return latitude, longitude

def calculateTemperatureFahrenheit(temperatureKelvin):
    fahrenheit = temperatureKelvin * (9 / 5) - 459.67
    return fahrenheit


local_css("style/style.css")

st.title("Weather App ⛅️")
st.write("---")


add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ["Homepage", "Global Weather Data", "Preferences", "Contact Us"]
)



if add_selectbox == "Global Weather Data":

    # Reading the CSV file for the project
    GlobalWeatherData = pd.read_csv("CSV/GlobalWeatherData.CSV")
    # Displaying data
    st.dataframe(
        GlobalWeatherData
    )
    st.caption("Table with Weather information around the world.")

elif add_selectbox == "Preferences":
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

    st.header("Daily Forecast")
    t = datetime.now().strftime("%H:%M:%S")
    st.caption("Current time is: " + t)

    # Comment of Weather Emojis for adding to forecast later☀️ 🌤 ⛅️ 🌥 ☁️ 🌦 🌧 ⛈ 🌩 🌨 ❄️

    # This section is to be updated to interact with the cities API provides
    st.info("Please provide your location to receive today's forecast!")

    userCity = st.selectbox(
        'Where are you located?',
        ('','Miami', 'Orlando', 'New York', 'Los Angeles', 'Dallas'),
    )

    # Selectbox to choose temps over span of time.
    timespanselect = st.selectbox(
        ' ',
        ('Hour', 'Day', 'Week')
    )

    # Elif below sets the data to show based on selected option.
    # Replace "None" with temp data for that range of time.
    if (timespanselect == 'Hour'):
        linetempdata = None
        lineXaxis = 'Hour'
    elif (timespanselect == 'Day'):
        linetempdata = None
        lineXaxis = 'Day'
    elif (timespanselect == 'Week'):
        linetempdata = None
        lineXaxis = 'Week'

    # Line chart displays temp for selected city over a selected amount of time (Hour, Day, Week)
    tempchart = pd.DataFrame(
        data = linetempdata,
        columns = ['Temperature'])

    st.line_chart(tempchart, x = lineXaxis, y = 'Temperature', label_visibility="visible")

    if userCity != "":
        # After this, probably include logic to display the city's forecast information for the day
        st.success('Your forecast is displayed below:', icon="✅️")

        # First we need to get the Latitude and Longitude from user input/dropdown menu
        latitudeCity = getGeolocationCity(userCity)[0]
        longitudeCity = getGeolocationCity(userCity)[1]

        # Connect to OpenWeather API
        file = open("WeatherAPI_keys.json")
        json_file = json.load(file)
        api_key = json_file["openWeather"]
        url = "https://api.openweathermap.org/data/3.0/onecall?lat=" + str(latitudeCity) + "&lon=" + str(
            longitudeCity) + "&appid=" + api_key
        response = requests.get(url).json()

        # To get current temperature in Fahrenheit
        temperatureFahrenheit = round(calculateTemperatureFahrenheit(response["current"]["temp"]))
        # Get all the different daily values from API

        weatherForecast = response["daily"][0]["summary"]  # check which one we like more

        st.text_area("You selected: " + userCity,
                     "The current temperature in " + userCity + " is: " + str(temperatureFahrenheit) + " °F\n"
                     + weatherForecast + "!",disabled=True)

        # Adding the map with Geolocation
        geolocationData = {"latitude": latitudeCity, "longitude": longitudeCity}
        locationDf = pd.DataFrame(geolocationData, index=[0])
        # st.dataframe(locationDf)
        st.map(data=locationDf)

    #  THIS IS THE SAMPLE CODE FOR THE TEXT AREA FEATURE
    # txt = st.text_area('Text to analyze', '''
    #     It was the best of times, it was the worst of times, it was
    #     the age of wisdom, it was the age of foolishness, it was
    #     the epoch of belief, it was the epoch of incredulity, it
    #     was the season of Light, it was the season of Darkness, it
    #     was the spring of hope, it was the winter of despair, (...)
    #     ''')
    # st.write('Sentiment:')









