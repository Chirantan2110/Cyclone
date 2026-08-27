import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from PIL import Image

st.set_page_config(page_title="CycloVision AI", layout="wide")

st.title("🌀 CycloVision AI - IMD Cyclone Decision Support")
st.markdown("Automated Satellite Tracking, Intensity Classification, and Trajectory Forecast System.")

# Sidebar for inputs
st.sidebar.header("Storm Parameters")
storm_name = st.sidebar.text_input("Storm Name", "CYCLONE REMAL")
current_lat = st.sidebar.number_input("Current Latitude (°N)", value=18.5)
current_lon = st.sidebar.number_input("Current Longitude (°E)", value=88.2)
current_wind = st.sidebar.slider("Current Wind Speed (Knots)", 30, 150, 75)

# Image Upload for Classification Mock
st.sidebar.subheader("INSAT-3D Satellite Image")
uploaded_file = st.sidebar.file_uploader("Upload IR/WV Image", type=["jpg", "png", "jpeg"])

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Satellite View & Classification")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded INSAT-3D Frame", use_container_width=True)
    else:
        st.info("Upload a cloud-top thermal IR image to run AI classification.")
        # Placeholder mock classification results
    
    st.markdown("### AI Diagnostic Panel")
    st.success(f"**Detected System:** {storm_name}")
    st.metric(label="Estimated T-Number (Dvorak)", value="T 4.5", delta="+0.5 (Intensifying)")
    st.metric(label="IMD Category", value="Severe Cyclonic Storm", delta="65-90 knots")
    st.metric(label="Estimated Landfall Risk", value="High (Sundarbans Delta)", delta="Within 24 hrs")

with col2:
    st.subheader("72-Hour Trajectory Forecast (ML Model)")
    
    # Simple predictive math acting as our "ML Model" for the hackathon
    forecast_hours = [6, 12, 24, 48, 72]
    forecast_data = []
    
    lat_drift = 0.08  # Northward drift per hour
    lon_drift = 0.05  # Eastward drift per hour
    
    for h in forecast_hours:
        pred_lat = current_lat + (h * lat_drift)
        pred_lon = current_lon + (h * lon_drift)
        pred_wind = min(current_wind + (h * 0.2), 120)
        forecast_data.append({
            "Hour": f"+{h}h",
            "Latitude": round(pred_lat, 2),
            "Longitude": round(pred_lon, 2),
            "Wind (Knots)": int(pred_wind)
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    st.table(df_forecast)
    
    # Map Visualization using Pydeck
    map_data = pd.DataFrame({
        'lat': [current_lat] + [f['Latitude'] for f in forecast_data],
        'lon': [current_lon] + [f['Longitude'] for f in forecast_data],
        'name': ['Current'] + [f['Hour'] for f in forecast_data]
    })
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 200]',
        get_radius=40000,
        pickable=True,
    )
    
    view_state = pdk.ViewState(latitude=current_lat, longitude=current_lon, zoom=5, pitch=0)
    st.pydeck_chart(pdk.Deck(initial_view_state=view_state, layers=[layer], tooltip={"text": "{name}"}))