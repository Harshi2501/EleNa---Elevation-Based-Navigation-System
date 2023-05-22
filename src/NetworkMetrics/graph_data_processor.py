import osmnx as ox
import networkx as nx
import os
import pickle as p
from NetworkMetrics.config import API
import math
from shapely.geometry import Point

class graph_data_processing:
     def __init__(self):
        print("Model initialization")        
        self.GOOGLEAPIKEY=API["googleapikey"]   
        graph_path = "./graph.p"   
        #checks if the graph.p file exists in the current directory using os.path.exists  
        if os.path.exists(graph_path):
            '''If the file exists, it is opened in binary mode using open and p.load is used to deserialize 
            the pickled object into self.G'''
            self.G = p.load( open( graph_path, "rb" ) )
            #self.init is set to True to indicate that the graph is ready for use.
            self.init = True
            print("The graph is now ready to use.")
        else:
            self.init = False
    
    #Calculating the distance between the given latitudes and longitudes using harvesine formula
     def haversine_distance(self, latitude1, longitude1, latitude2, longitude2):
         # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(latitude1)
        lon1_rad = math.radians(longitude1)
        lat2_rad = math.radians(latitude2)
        lon2_rad = math.radians(longitude2)
        # Earth's radius in kilometers
        earth_radius = 6371

        diff_lat = lat2_rad - lat1_rad 
        diff_long = lon2_rad-lon1_rad

        value = math.sin(diff_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(diff_long/2)**2
        temp_value = 2 * math.atan2(math.sqrt(value), math.sqrt(1-value))
        
        final_value = earth_radius*temp_value

        #Distance in meters
        final_value_meters = final_value *1000
        return final_value_meters

    #Adds elevation data to the graph
     def add_elevation_data(self, G):
         G = ox.add_node_elevations_google(G, api_key=self.GOOGLEAPIKEY)
         #Returns the updated graph with the added elevation data
         return G
     
     #Calculates distance between a given edge node to all other nodes in the graph
     def dist_calc(self, G, e_node):
          #creating a copy of the original graph G using G.copy() to avoid modifying the original graph.
          G_copy = G.copy()  

          for node in G_copy.nodes():
            latitude2 = G_copy.nodes[node]['y']
            longitude2 = G_copy.nodes[node]['x']
            distance = self.haversine_distance(e_node["y"], e_node["x"], latitude2, longitude2)
            # Setting 'dist_from_dest' attribute for each node
            nx.set_node_attributes(G_copy, {node: {'dist_from_dest': distance}})  

          return G_copy
     
     def add_dist(self,G,endpoint):
        # Adding dist between final destination and all nodes
        e_node=G.nodes[ox.nearest_nodes(G, X= endpoint[1], Y=endpoint[0], return_dist=False)]            
        return self.dist_calc(G,e_node)    

    #Generates a graph and elevation data based on a specified starting point and endpoint.
     def generate_graph(self, endpoint):
         start_latitude = 42.384803
         start_longitude = -72.529262
         if not self.init:
             print("Loading graph")
             start = (start_latitude, start_longitude)

             '''Calls the graph_from_point function from the osmnx library to generate 
             a graph based on the starting point, with a specified distance and network type.'''
             self.G = ox.graph_from_point(center_point=start, dist=20000, network_type='walk')

             #Calls the add_elevation_data function to add elevation data to the graph.
             self.G = self.add_elevation_data(self.G)
             with open("graph.p", "wb") as f:
                p.dump(self.G, f)            
            #Updates the self.init variable to True to indicate that the graph has been initialized.
             self.init = True
             print("Graph saved")
         '''Calls the add_dist function to add distance 
        information between the endpoint and all nodes in the graph'''
         self.G = self.add_dist(self.G, endpoint)
         return self.G
     


     



     
    
    
    

    
    
    
         
    




