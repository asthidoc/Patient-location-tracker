import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Initialize or load data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Location", "Latitude", "Longitude", "Count"])

if "data" not in st.session_state:
    st.session_state.data = load_data()

# Header
st.title("📍 Patient Location Tracker")

# Add location section
st.write("### Add a New Location")
with st.form("add_location", clear_on_submit=True):
    location = st.text_input("Location Name")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    count = st.number_input("Number of Patients", min_value=1, step=1)

    submitted = st.form_submit_button("Add")
    if submitted:
        if location and latitude and longitude:
            new_data = {"Location": location, "Latitude": latitude, "Longitude": longitude, "Count": count}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"✅ Location '{location}' added!")
        else:
            st.error("⚠️ Please fill in all fields!")

# Data display
st.write("### Current Data")
if st.session_state.data.empty:
    st.info("No locations added yet.")
else:
    st.dataframe(st.session_state.data)

# Map section
st.write("### Patient Locations Heatmap")
if not st.session_state.data.empty:
    map_center = [st.session_state.data["Latitude"].mean(), st.session_state.data["Longitude"].mean()]
    m = folium.Map(location=map_center, zoom_start=10)
    heat_data = st.session_state.data[["Latitude", "Longitude", "Count"]].values.tolist()
    HeatMap(heat_data).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("Map will display once locations are added.")

# Export option
if not st.session_state.data.empty:
    st.download_button(
        label="📥 Download Data",
        data=st.session_state.data.to_csv(index=False),
        file_name="patient_data.csv",
        mime="text/csv",
    )
