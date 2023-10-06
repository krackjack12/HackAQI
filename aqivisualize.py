import streamlit as st
import folium
import pickle
from streamlit_folium import folium_static

# Load the graph from a GPickle file using pickle
with open('graph1.pkl', 'rb') as file:
    G = pickle.load(file)

# Create a Streamlit app
st.title("Interactive Map with Node Colors Based on AQI")

# Create a Folium map
m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)

# Define a function to set node color based on AQI value
def get_node_color(aqi):
    if 0 <= aqi < 50:
        return "darkgreen"  # Dark Green for Minimal impact
    elif 50 <= aqi < 100:
        return "lightgreen"  # Light green for Minor breathing discomfort to sensitive people
    elif 100 <= aqi < 200:
        return "yellow"  # Yellow for Breathing discomfort to people with lungs, asthma, and heart diseases
    elif 200 <= aqi < 300:
        return "orange"  # Orange for Breathing discomfort to most people on prolonged exposure
    elif 300 <= aqi < 400:
        return "lightred"  # Light Red for Respiratory illness on prolonged exposure
    elif aqi >= 400:
        return "darkred"  # Dark Red for Affects healthy people and seriously impacts those with existing diseases
    else:
        return "white"  # For no range

# Plot nodes on the map with color coding based on AQI value
for node in G.nodes(data=True):
    lat = node[1]["latitude"]
    lon = node[1]["longitude"]
    aqi = node[1]["aqi"]
    
    # Get the node color based on AQI
    node_color = get_node_color(aqi)
    
    folium.CircleMarker([lat, lon], radius=5, color=node_color, fill=True, fill_color=node_color).add_to(m)

# Display the Folium map
folium_static(m)