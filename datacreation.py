import pandas as pd

'''
# First Join
# Read the CSV files into DataFrames
data1 = pd.read_csv('GTFS/fare_rules.csv')
data2 = pd.read_csv('GTFS/routes.csv')

# Perform a left join on 'route_id'
merged_df = data1.merge(data2, on='route_id', how='left')

columns_to_remove = ['fare_id', 'agency_id','route_short_name','route_type']

# Removing irrelevant attributes
merged_df = merged_df.drop(columns=columns_to_remove)

# Display the merged DataFrame
#print(merged_df)

# Save the resulting DataFrame to a CSV file
merged_df.to_csv('route.csv', index=False)



# Second Join
# Read the CSV files into DataFrames
data1 = pd.read_csv('GTFS/stop_times.csv')
data2 = pd.read_csv('GTFS/trips.csv')

# Perform a left join on 'trip_id'
merged_df2 = data1.merge(data2, on='trip_id', how='left')

columns_to_remove2 = ['shape_id','service_id','stop_sequence']

# Removing irrelevant attributes
merged_df2 = merged_df2.drop(columns=columns_to_remove2)

# Display the merged DataFrame
#print(merged_df2)

# Save the resulting DataFrame to a CSV file
merged_df2.to_csv('trip.csv', index=False)


# Third Join
# Read the CSV files into DataFrames
data1 = pd.read_csv('route.csv')
data2 = pd.read_csv('trip.csv')

# Perform a left join on 'route_id'
merged_df2 = data1.merge(data2, on='route_id', how='left')

columns_to_remove2 = []

# Removing irrelevant attributes
merged_df2 = merged_df2.drop(columns=columns_to_remove2)

# Display the merged DataFrame
print(merged_df2)

# Save the resulting DataFrame to a CSV file
merged_df2.to_csv('data.csv', index=False)
'''

# Third Join
# Read the CSV files into DataFrames
data1 = pd.read_csv('GTFS/stop_times.csv')
data2 = pd.read_csv('GTFS/stops.csv')

# Perform a left join on 'stop_id'
merged_df2 = data1.merge(data2, on='stop_id', how='left')

columns_to_remove2 = ["arrival_time","departure_time","zone_id"]

# Removing irrelevant attributes
merged_df2 = merged_df2.drop(columns=columns_to_remove2)

# Display the merged DataFrame
print(merged_df2)

# Save the resulting DataFrame to a CSV file
merged_df2.to_csv('data.csv', index=False)