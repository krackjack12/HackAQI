import csv
import json
import pandas as pd

# Define a list to store the lat-long tuples for stops
stops_list = []

# Open the CSV file for reading
with open('/Users/krishjoshi/Desktop/Python/HackAQI/GTFS/stops.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)
    
    # Skip the header row
    next(csvreader)
    
    # Iterate over each row in the CSV
    for row in csvreader:
        # Extract latitude and longitude values from the row
        stop_lat = float(row[2])
        stop_lon = float(row[3])
        stop_name = row[4]
        
        # Append the lat-long tuple to the list
        stops_list.append((stop_lat, stop_lon,stop_name))

# Print the list of lat-long tuples
#print(stops_list)


# Define a list to store the lat-long tuples for aqi monitoring stations
aqi_list = []

# Open the JSON file for reading
with open('delhi.json', 'r') as jsonfile:
    # Load the JSON data
    data = json.load(jsonfile)
    
    # Iterate over each item in the JSON array
    for item in data:
        # Extract latitude and longitude values from each item
        lat = item["lat"]
        lon = item["long"]
        aqi = item["stationAqi"]
        stationName = item["stationName"]
        
        # Append the lat-long tuple to the list
        aqi_list.append((lat, lon, aqi, stationName))

# Print the list of lat-long tuples
#print(aqi_list)

# Create a list of dictionaries with "latitude" and "longitude" keys
stops_coordinates_dict_list = [{"latitude": lat, "longitude": lon, "type": "stops", "stop_name": stop_name} for lat, lon, stop_name in stops_list]
aqi_coordinates_dict_list = [{"latitude": lat, "longitude": lon, "type": "aqi", "aqi": aqi, "stationName": stationName} for lat, lon, aqi, stationName in aqi_list]

# Plotting these points on an interactive map using streamlit
import streamlit as st

# Create a Streamlit app
st.title("Interactive Map")

# Map showing stops data
st.map(stops_coordinates_dict_list)

# Map showing aqi data
st.map(aqi_coordinates_dict_list)

'''

# Calculating closest aqi station
import streamlit as st
from geopy.distance import geodesic

# Calculate the minimum distances and store AQI values
for stop_data in stops_coordinates_dict_list:
    stop_location = (stop_data["latitude"], stop_data["longitude"])
    min_distance = float("inf")  # Initialize with a large value
    closest_aqi = None
    
    for aqi_data in aqi_coordinates_dict_list:
        aqi_location = (aqi_data["latitude"], aqi_data["longitude"])
        distance = geodesic(stop_location, aqi_location).kilometers
        
        if distance < min_distance:
            min_distance = distance
            closest_aqi = aqi_data["aqi"]
            aqi_stationName = aqi_data["stationName"]
    
    stop_data["closest_aqi"] = closest_aqi  # Store the closest AQI value
    stop_data["aqi_stationName"] = aqi_stationName # Store the AQI station name

# print(stops_coordinates_dict_list)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(stops_coordinates_dict_list)

# Specify the path where you want to save the CSV file
csv_file_path = "stopsdata_calculated.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

# Print a message to confirm the file has been saved
print(f"Data has been saved to {csv_file_path}")

'''