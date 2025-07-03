import streamlit as st
import pandas as pd
import numpy as np
import pickle
from geopy.geocoders import Nominatim
import openrouteservice
import time

def categorize_traffic(hour):
    if 7 <= hour <= 11 or 17 <= hour <= 22:
        return 'high'
    elif 12 <= hour <= 16:
        return 'medium'
    else:
        return 'low'

with open("eta_model.pkl", "rb") as f:
    model = pickle.load(f)


geolocator = Nominatim(user_agent="eta_app_bangalore", timeout=5)
api_key = st.secrets["ORS_API_KEY"]
client = openrouteservice.Client(key=api_key)  


def geocode_place(place, retries=3, delay=2):
    for attempt in range(retries):
        try:
            location = geolocator.geocode(f"{place}, Bengaluru, India")
            if location:
                return (location.longitude, location.latitude)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    return None


def get_distance_km(start_place, end_place):
    start_coords = geocode_place(start_place)
    end_coords = geocode_place(end_place)
    if start_coords and end_coords:
        try:
            route = client.directions((start_coords, end_coords), profile='driving-car')
            dist_m = route['routes'][0]['summary']['distance']
            return round(dist_m / 1000, 2)  # in km
        except Exception as e:
            print(f"ORS routing error: {e}")
            return None
    else:
        print("❌ Could not geocode one or both locations.")
        return None


st.set_page_config(page_title="Bengaluru ETA Predictor", layout="centered", page_icon="🏎")
st.image("https://i.postimg.cc/02cYyvPq/file-00000000ce9c61f5b3ed3830c39d725b.png", use_container_width=True)   # Replace with your actual image link

st.title("🗺 Bengaluru ETA Predictor")
st.markdown(" Predict your expected travel time (ETA) based on real traffic conditions in Bengaluru.")


src = st.text_input(" Pickup Location", placeholder="e.g., Indiranagar")
dest = st.text_input(" Drop-off Location", placeholder="e.g., Jayanagar")
day = st.selectbox("🗓️ Day of the Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
hour = st.slider("⏰ Time of Day (24-Hour Format)", 0, 23, 9)


st.warning("ℹ Please enter location names accurately, e.g., 'BTM Layout', 'Marathahalli', 'Majestic', etc. including city name 'Bengaluru' if needed.")


if st.button("🔮 Predict ETA"):
    if src and dest:
        with st.spinner("🔄 Calculating ETA... please wait"):
            distance = get_distance_km(src, dest)
            time.sleep(0.5)  # Optional: feel of processing

            if not distance:
                st.error("❌ Could not calculate distance. Please check your location names.")
                st.info("ℹ Try using full names like 'Whitefield' or 'BTM Layout, Bengaluru'")
            else:
                traffic_level = categorize_traffic(hour)
                input_df = pd.DataFrame({
                    'distance_travelled': [distance],
                    'day_of_week': [day],
                    'time_of_day': [hour],
                    'peak_traffic': [traffic_level]
                })

                prediction = model.predict(input_df)[0]
                st.success(f"📏 Estimated Distance: {distance} km")
                st.success(f"🕒 Predicted ETA: {prediction:.2f} minutes")
    else:
        st.error("❌ Please enter both pickup and drop-off locations.")
