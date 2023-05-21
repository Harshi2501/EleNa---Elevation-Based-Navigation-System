import osmnx as ox
import networkx as nx
import os
import pickle as p
from src.NetworkMetrics.config import API
import math

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
     def harvesine_distance(self, latitude1, longitude1, latitude2, longitude2):
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

    #Adds elevation data to the graph
     def add_elevation_data(self, G):
         G = ox.add_node_elevations(G, elevation_key="elevation", api_key=self.GOOGLEAPIKEY)
         #Returns the updated graph with the added elevation data
         return G
     
     
    
    
    

         
    
    
         
    




