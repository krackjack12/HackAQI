import pandas as pd

# Load the CSV file with AQI data
aqi_data = pd.read_csv("/Users/krishjoshi/Desktop/Python/HackAQI/stopsdata_calculated.csv")

# Load the CSV file with stop data
stop_data = pd.read_csv("/Users/krishjoshi/Desktop/Python/HackAQI/GTFS/stops.csv")

# Create a dictionary mapping 'stop_name' to 'stop_id'
stop_name_to_id = stop_data.set_index('stop_name')['stop_id'].to_dict()

# Add 'stop_id' to the AQI data based on 'stop_name'
aqi_data['stop_id'] = aqi_data['stop_name'].map(stop_name_to_id)

# Save the modified AQI data to a new CSV file
aqi_data.to_csv("aqi_data_with_stop_id.csv", index=False)