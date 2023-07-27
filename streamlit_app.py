import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import requests
import time as tm
import pydeck as pdk
import plotly.express as px

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

def calculateUVindex(index):
    if index >= 11:
        return "extreme, take full precautions."
    elif index >= 8:
        return "very high, take precautions."
    elif index >= 6:
        return "high, we recommend wearing sunscreen and staying hydrated."
    elif index >= 3:
        return "moderate, we recommend wearing sunscreen."
    else:
        return "low"

local_css("style/style.css")

st.title("Weather App ⛅️")
st.write("---")


add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ["Homepage", "Global Weather Data", "Data Display", "Contact Us"]
)



if add_selectbox == "Global Weather Data":

    # st.write("Please select a color to highlight freezing temperatures around the world.")
    color = st.color_picker('Please select a color to highlight freezing temperatures around the world.', '#ADD8E6')
    st.write('The current color is', color)

    # Reading the CSV file for the project
    GlobalWeatherData = pd.read_csv("CSV/GlobalWeatherData.CSV")
    # Displaying data
    st.dataframe(
        GlobalWeatherData.style.highlight_between(axis=1, subset=["Temperature"], color=color, right=0).format(
            precision=2, subset=["Longitude", "Latitude", "Temperature", "Humidity", "Wind", "Clouds"])
    )
    st.caption("Table with Weather information around the world.")

elif add_selectbox == "Data Display":
    st.header("Display")
    chart_data = pd.read_csv("CSV/GraphChartsData.csv")

    dataDisplay = st.radio("Choose from the following options: ",
                           options=('Temperature', 'Wind', 'Humidity'))
    # Elif below sets the data to show based on selected option.
    # Replace "None" with temp data for that range of time.
    if dataDisplay == 'Temperature':
        st.line_chart(chart_data, x='Days', y='Temperature')
        st.caption("Line chart displaying temperature overtime in Miami")
    elif dataDisplay == 'Wind':
        #Bar chart for wind
        st.bar_chart(chart_data, x="Days", y="Wind")
        st.caption("Bar chart displaying wind overtime in Miami")
    elif dataDisplay == 'Humidity':
        st.line_chart(chart_data, x='Days', y='Humidity')
        st.caption("Line chart displaying humidity overtime in Miami")

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
    cities = ('', 'Miami', 'Orlando', 'New York', 'Los Angeles', 'Dallas', 'Washington D.C', 'London', 'Madrid',
              'Buenos Aires', 'Rome', 'Caracas', 'Sao Paolo', 'Dubai', 'Moscow', 'Beijing', 'Tokyo',
              'Bogota', 'Mexico City', 'Santiago de Chile', 'Ankara', 'Brasilia', 'Toronto', 'Ottawa',
              'Stockholm', 'Zagreb', 'Athens', 'Lisbon', 'Chicago', 'Hawaii', 'San Francisco', 'San Diego',
              'Atlanta', 'Boston', 'Houston', 'Austin', 'Baltimore', 'Seattle')

    st.header("Daily Forecast")
    t = datetime.now().strftime("%H:%M:%S")
    st.caption("Current time is: " + t)

    # Comment of Weather Emojis for adding to forecast later☀️ 🌤 ⛅️ 🌥 ☁️ 🌦 🌧 ⛈ 🌩 🌨 ❄️

    # This section is to be updated to interact with the cities API provides
    st.info("Please provide your location to receive today's forecast!")

    userCity = st.selectbox(
        'Where are you located?',
        (sorted(cities)),
    )

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
        weatherForecast = response["daily"][0]["summary"]
        minTemperature = round(calculateTemperatureFahrenheit(response["daily"][0]["temp"]["min"]))
        maxTemperature = round(calculateTemperatureFahrenheit(response["daily"][0]["temp"]["max"]))
        humidity = response["daily"][0]["humidity"]
        dewPoint = round(calculateTemperatureFahrenheit(response["daily"][0]["dew_point"]))
        windSpeed = response["daily"][0]["wind_speed"]
        windDegrees = response["daily"][0]["wind_deg"]
        uvIndex = response["daily"][0]["uvi"]

        weatherForecast = response["daily"][0]["summary"]  # check which one we like more

        st.text_area("You selected: " + userCity,
                     "The current temperature in " + userCity + " is: " + str(temperatureFahrenheit) + " °F\n"
                     + weatherForecast + "!\n" +
                     "The minimum temperature for today is: " + str(minTemperature) + " °F\n" +
                     "The maximum temperature for today is: " + str(maxTemperature) + " °F\n" +
                     "The humidity for today is at: " + str(humidity) + "%\n" +
                     "The Dew Point for today is: " + str(dewPoint) + "°\n" +
                     "The wind speed for today is " + str(windSpeed) + "mph with a direction of " + str(windDegrees) +
                     "°\n" +
                     "The UV Index for today is " + str(uvIndex) + " which is considered " + calculateUVindex(uvIndex),
                     height=215, disabled=True)

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









