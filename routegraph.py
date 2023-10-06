import pandas as pd
import networkx as nx
import networkx.exception as nx_exception
import math
import pickle
import logging
import matplotlib.pyplot as plt
import streamlit as st

# Logs configuration 
logging.basicConfig(filename='graph_creation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate the distance between two points using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

# Function to load or create the graph
def load_or_create_graph():
    try:
        with open('graph1.pkl', 'rb') as file:
            G = pickle.load(file)
            print("Graph loaded from file.")
            logging.info("Graph loaded from file.")
            
            '''# Create a Streamlit app
            st.title('Graph Visualization')

            # Display the graph using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 10))
            pos = nx.spring_layout(G)  # You can use different layout algorithms here
            nx.draw(G, pos, with_labels=True, node_size=30, font_size=8, font_color='black', node_color='skyblue', ax=ax)
            st.pyplot(fig)'''

    except FileNotFoundError:
        G = create_graph()
        with open('graph1.pkl', 'wb') as file:
            pickle.dump(G, file)
        print("Graph created and saved to file.")
        logging.info("Graph created and saved to file.")

    return G

# Function to create the graph
def create_graph(num_trip_ids=100):
    print("Creating the graph...")
    logging.info("Creating the graph...")

    # Load trip data
    trip_data = pd.read_csv('routesdata.csv')
    trip_data['stop_id'] = trip_data['stop_id'].astype(int)
    trip_data['stop_name'] = trip_data['stop_name'].astype(str)

    # Load AQI data
    aqi_data = pd.read_csv('stopsdata_calculated.csv')
    aqi_data['stop_name'] = aqi_data['stop_name'].astype(str)

    # Create a dictionary to map stop names to AQI values
    stop_aqi_mapping = dict(zip(aqi_data['stop_name'], aqi_data['closest_aqi']))

    # Create a graph
    G = nx.DiGraph()

    count = 0
    # Dictionary to track existing nodes
    existing_nodes = {}
    
    # Create nodes in the graph
    for _, row in trip_data.iterrows():
        stop_name = row['stop_name']
        
        # Check if the node already exists
        if stop_name not in existing_nodes:
            latitude = row['stop_lat']
            longitude = row['stop_lon']
            aqi = stop_aqi_mapping.get(stop_name, 0)  # Use 0 as default AQI if not found in AQI data
            G.add_node(stop_name, latitude=latitude, longitude=longitude, aqi=aqi)
            existing_nodes[stop_name] = True
            count += 1
            print("Node Added : " + str(count))
            logging.info("Node Added : " + str(count))


    # Create edges in the graph based on trip data
    trip_groups = trip_data.groupby('trip_id')
    edges_to_add = []

    trip_count = 0
    count = 0
    for _, group in trip_groups:
        stops = group['stop_name'].tolist()

        print(f"Number of stops in trip_id {count}: {len(stops)}")
        logging.info(f"Number of stops in trip_id {trip_count}: {len(stops)}")

        for i in range(len(stops) - 1):
            source = stops[i]
            target = stops[i + 1]

            print(f"{source} , {target}")
            logging.info(f"Edge : {source} to {target}")

            source_data = trip_data[trip_data['stop_name'] == source].iloc[0]
            target_data = trip_data[trip_data['stop_name'] == target].iloc[0]

            distance = math.sqrt((source_data['stop_lat'] - target_data['stop_lat']) ** 2 + (source_data['stop_lon'] - target_data['stop_lon']) ** 2)
            
            edges_to_add.append((source, target, {'distance': distance}))
            count += 1
            print("Edge Added : " + str(count))
            logging.info("Edge Added : " + str(count))
        
        if trip_count > num_trip_ids:
                break  # Break the loop after adding the specified number of trips
        
        trip_count += 1
        print("Number of trips completed : " + str(trip_count))
        logging.info("Number of trips completed : " + str(trip_count))


    G.add_edges_from(edges_to_add)
    print("Graph creation completed.")
    logging.info("Graph creation completed.")
    return G

# Define a function to find all stops in a path
def find_all_stops_in_path(G, path):
    stops = [node for node in path]
    return stops

# Define a function to find the shortest and cleanest path
# Algorithm used : A* algorithm -> heuristic algorithm
def find_shortest_and_cleanest_path(G, source, target):
    print("Finding shortest and cleanest paths...")
    
    try:
        # Define a custom heuristic function for A* based on AQI (lower AQI is better)
        def heuristic(node, target):
            aqi = G.nodes[node]['aqi']
            return aqi
        
        # Calculate the shortest path using A* based on distance
        shortest_path = nx.astar_path(G, source=source, target=target, heuristic=heuristic, weight='distance')
        
        # Calculate the cleanest path using A* based on AQI
        cleanest_path = nx.astar_path(G, source=source, target=target, heuristic=heuristic, weight='aqi')
        
        # Calculate the distance along the shortest path
        shortest_distance = sum(haversine(G.nodes[shortest_path[i]]['latitude'], G.nodes[shortest_path[i]]['longitude'], 
                                          G.nodes[shortest_path[i + 1]]['latitude'], G.nodes[shortest_path[i + 1]]['longitude'])
                                for i in range(len(shortest_path) - 1))
        
        # Calculate the distance along the cleanest path
        cleanest_distance = sum(haversine(G.nodes[cleanest_path[i]]['latitude'], G.nodes[cleanest_path[i]]['longitude'], 
                                          G.nodes[cleanest_path[i + 1]]['latitude'], G.nodes[cleanest_path[i + 1]]['longitude'])
                                for i in range(len(cleanest_path) - 1))
        
        avg_aqi_shortest = sum(G.nodes[node]['aqi'] for node in shortest_path) / len(shortest_path)
        avg_aqi_cleanest = sum(G.nodes[node]['aqi'] for node in cleanest_path) / len(cleanest_path)
        
        print("Paths found.")
        
        return {
            'shortest_path': shortest_path,
            'cleanest_path': cleanest_path,
            'shortest_distance': shortest_distance,
            'cleanest_distance': cleanest_distance,
            'avg_aqi_shortest': avg_aqi_shortest,
            'avg_aqi_cleanest': avg_aqi_cleanest
        }
    
    except nx.NetworkXNoPath:
        print(f"No path between {source} and {target}.")
        logging.info(f"No path between {source} and {target}.")
        # Set default values when no path is found
        return {
            'shortest_path': [],
            'cleanest_path': [],
            'shortest_distance': 0.0,  # Default to 0 distance
            'cleanest_distance': 0.0,  # Default to 0 distance
            'avg_aqi_shortest': 0.0,  # Default to 0 AQI
            'avg_aqi_cleanest': 0.0   # Default to 0 AQI
        }

# Example usage
source_stop = "Prem Bari Pull"
target_stop = "AIIMS"

# Load or create the graph
G = load_or_create_graph()

result = find_shortest_and_cleanest_path(G, source_stop, target_stop)

# Get all stops in the shortest path
shortest_stops = find_all_stops_in_path(G, result['shortest_path'])

# Get all stops in the cleanest path
cleanest_stops = find_all_stops_in_path(G, result['cleanest_path'])

print("Shortest Path Stops:", shortest_stops)
print("Cleanest Path Stops:", cleanest_stops)
print("Shortest Distance:", result['shortest_distance'])
print("Cleanest Distance:", result['cleanest_distance'])
print("Average AQI for Shortest Path:", result['avg_aqi_shortest'])
print("Average AQI for Cleanest Path:", result['avg_aqi_cleanest'])