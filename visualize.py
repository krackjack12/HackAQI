import streamlit as st
import folium
import networkx as nx
from streamlit_folium import folium_static
import pickle
from routegraph import find_shortest_and_cleanest_path

# Load the graph from a GPickle file using pickle
with open('graph1.pkl', 'rb') as file:
    G = pickle.load(file)

# Create a Streamlit app
st.title("Interactive Map with Cleanest Path")

# Input form to select nodes
st.sidebar.header("Select Nodes")
source_node = st.sidebar.selectbox("Source Node", list(G.nodes))
target_node = st.sidebar.selectbox("Target Node", list(G.nodes))

# Find the cleanest path
result = find_shortest_and_cleanest_path(G, source_node, target_node)
cleanest_path = result['cleanest_path']

# Create a Folium map
m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)

# Clear the map to remove any previous edges
m._repr_html_ = m.get_root().render()

# Plot nodes on the map with color coding
for node in G.nodes(data=True):
    lat = node[1]["latitude"]
    lon = node[1]["longitude"]
    aqi = node[1]["aqi"]
    if node[0] in cleanest_path:
        marker_color = "black"  # Color for nodes in the cleanest path
    else:
        marker_color = "transparent"  # Color for nodes not in the cleanest path
    folium.CircleMarker([lat, lon], radius=5, color=marker_color, fill=True, fill_color=marker_color,close=True).add_to(m)

# Plot edges on the map with color coding based on AQI range
for edge in G.edges(data=True):
    source = edge[0]
    target = edge[1]
    
    source_lat = G.nodes[source]["latitude"]
    source_lon = G.nodes[source]["longitude"]
    target_lat = G.nodes[target]["latitude"]
    target_lon = G.nodes[target]["longitude"]
    
    edge_aqi = G.nodes[target]["aqi"]

    if 0 <= edge_aqi < 50:
        edge_color = "darkgreen"  # Dark Green for Minimal impact
    elif 50 <= edge_aqi < 100:
        edge_color = "lightgreen"  # Light green for Minor breathing discomfort to sensitive people
    elif 100 <= edge_aqi < 200:
        edge_color = "yellow"  # Yellow for Breathing discomfort to the people with lungs, asthma and heart diseases
    elif 200 <= edge_aqi < 300:
        edge_color = "orange"  # Orange for Breathing discomfort to most people on prolonged exposure
    elif 200 <= edge_aqi < 300:
        edge_color = "lightred"  # Light Red for Respiratory illness on prolonged exposure
    elif 200 <= edge_aqi < 300:
        edge_color = "darkred"  # Dark Red for Affects healthy people and seriously impacts those with existing diseases
    else:
        edge_color = "white" # For no range

    folium.PolyLine([(source_lat, source_lon), (target_lat, target_lon)], color=edge_color).add_to(m)

# Display the Folium map
folium_static(m)

# Clear the map to remove any previous edges
m._repr_html_ = m.get_root().render()

# Display path information for the cleanest path
st.write(f"Cleanest Path from {source_node} to {target_node}: {cleanest_path}")
st.write(f"Cleanest Distance: {result['cleanest_distance']}")
st.write(f"Average AQI for Cleanest Path: {result['avg_aqi_cleanest']}")

if 0 <= result['avg_aqi_cleanest'] < 50:
    remark = "Good"
elif 50 <= result['avg_aqi_cleanest'] < 100:
    remark = "Satisfactory"
elif 100 <= result['avg_aqi_cleanest'] < 200:
    remark = "Moderate"
elif 200 <= result['avg_aqi_cleanest'] < 300:
    remark = "Poor"
elif 200 <= result['avg_aqi_cleanest'] < 300:
    remark = "Very Poor"
elif 200 <= result['avg_aqi_cleanest'] < 300:
    remark = "Severe"
else:
    remark = "Good"

st.write(f"Overall Remark : AQI - " + remark)