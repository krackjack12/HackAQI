import pandas as pd
import networkx as nx
import math
import pickle

# Function to load or create the graph
def load_or_create_graph():
    try:
        with open('graph.pkl', 'rb') as file:
            G = pickle.load(file)
            print("Graph loaded from file.")
    except FileNotFoundError:
        G = create_graph()
        with open('graph.pkl', 'wb') as file:
            pickle.dump(G, file)
        print("Graph created and saved to file.")
    return G

# Function to create the graph
def create_graph(num_trip_ids=10):
    print("Creating the graph...")
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

            if num_trip_ids is not None and count >= num_trip_ids:
                break  # Break the loop after adding the specified number of nodes

    # Create edges in the graph based on trip data
    trip_groups = trip_data.groupby('trip_id')
    edges_to_add = []

    count = 0
    for _, group in trip_groups:
        stops = group['stop_name'].tolist()
        for i in range(len(stops) - 1):
            source = stops[i]
            target = stops[i + 1]
            source_data = trip_data[trip_data['stop_name'] == source].iloc[0]
            target_data = trip_data[trip_data['stop_name'] == target].iloc[0]
            distance = math.sqrt((source_data['stop_lat'] - target_data['stop_lat']) ** 2 + (source_data['stop_lon'] - target_data['stop_lon']) ** 2)
            edges_to_add.append((source, target, {'distance': distance}))
            count += 1
            print("Edge Added : " + str(count))
            
            if num_trip_ids is not None and count >= num_trip_ids:
                break  # Break the loop after adding the specified number of edges

    G.add_edges_from(edges_to_add)
    print("Graph creation completed.")
    return G

# Define a function to find all stops in a path
def find_all_stops_in_path(G, path):
    stops = [node for node in path]
    return stops

# Define a function to find the shortest and cleanest path
def find_shortest_and_cleanest_path(G, source, target):
    print("Finding shortest and cleanest paths...")
    shortest_path = nx.shortest_path(G, source=source, target=target, weight='distance')
    cleanest_path = nx.shortest_path(G, source=source, target=target, weight='aqi')
    
    # Calculate the distance along the shortest path
    shortest_distance = sum(G.get_edge_data(shortest_path[i], shortest_path[i+1])['distance'] for i in range(len(shortest_path) - 1))
    
    # Calculate the distance along the cleanest path
    cleanest_distance = sum(G.get_edge_data(cleanest_path[i], cleanest_path[i+1])['distance'] for i in range(len(cleanest_path) - 1))
    
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

# Example usage
source_stop = "Narela Terminal"
target_stop = "Sec A-9 Narela"

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