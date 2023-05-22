import osmnx as ox
from osmnx import *
import networkx as nx
from collections import deque, defaultdict
from heapq import *
import time
from RoutingAlgorithms.djikstra import Djikstra
from RoutingAlgorithms.a_star import A_star

cost_mode_0 = "no_elevation"
cost_mode_1  = "elevation_drop"
cost_mode_2 = "elevation_gain"
cost_mode_3 = "elevation_difference"

elev_type_0 = "max"
elev_type_1 = "min"


class Algorithms:
    def __init__(self, graph, elev_perc = 0.0, elev_option = "maximize"):

        self.graph = graph
        self.elev_option = elev_option
        self.elev_perc = elev_perc
        self.best_path = {}
        self.best_path["route"]= []
        self.best_path["elevation_distance"]= float("-inf")
        self.best_path["drop_dist"]= 0.0
        self.best_path["current_distance"]= 0.0

        self.start_node= None
        self.end_node =None


    def reload(self, graph):
        # Reloading with modified graph
        self.graph = graph


    
    def compute_cost(self, start, end, cost_type = cost_mode_0):
        graph = self.graph   
        if start is None or end is None:
            return 0
        if cost_type == cost_mode_0:
            try:
                return graph.edges[start, end ,0]["length"]
            except : 
                return graph.edges[start, end]["weight"]
        elif cost_type == cost_mode_3:
            return graph.nodes[end]["elevation"] - graph.nodes[start]["elevation"]
        elif cost_type == cost_mode_2:
            return max(0.0, graph.nodes[end]["elevation"] - graph.nodes[start]["elevation"])
        elif cost_type == cost_mode_1:
            return max(0.0, graph.nodes[start]["elevation"] - graph.nodes[end]["elevation"])
        else:
            return abs(graph.nodes[start]["elevation"] - graph.nodes[end]["elevation"])



    def get_Elevation(self, route, cost_type = "cost_mode_3"):
        # For a particular route, the function returrns the total or piecewise cost.
        total = 0
        diff=0
        for i in range(len(route)-1):
            if cost_type == cost_mode_3:
                diff = self.compute_cost(route[i],route[i+1],cost_mode_3)	
            elif cost_type == cost_mode_2:
                diff = self.compute_cost(route[i],route[i+1],cost_mode_2)
            elif cost_type == cost_mode_1:
                diff = self.compute_cost(route[i],route[i+1],cost_mode_1)
            elif cost_type == cost_mode_0:
                diff = self.compute_cost(route[i],route[i+1],cost_mode_0)
            total += diff
        return total

    





   


    def compare(self, graph, shortestPathStats):

        if (self.elev_option == elev_type_0 and self.best_path["elevation_distance"] == float('-inf')) or (self.elev_option ==elev_type_1 and self.best_path["drop_dist"] == float('-inf')):            

            return shortestPathStats, self.best_path
        
        self.best_path["route"] = [[graph.nodes[route_node]['x'],graph.nodes[route_node]['y']] for route_node in self.best_path["route"]]

        # If computed path does not match the requirements
        if((self.elev_option == elev_type_0 and self.best_path["elevation_distance"] < shortestPathStats["elevation_distance"]) or (self.elev_option ==elev_type_1 and self.best_path["elevation_distance"] > shortestPathStats["elevation_distance"])):
            self.best_path = shortestPathStats
        
        return shortestPathStats, self.best_path


   



    def get_shortest_path(self, spt, ept, elev_perc, elev_option = "maximize", log=True):
        
        # Computes Shortest Path
        graph = self.graph
        self.elev_perc = elev_perc/100.0
        self.elev_option = elev_option
        self.start_node, self.end_node = None, None

        self.start_node, d1 = ox.nearest_nodes(graph, X=spt[1], Y=spt[0], return_dist=True)
        self.end_node, d2 = ox.nearest_nodes(graph, X=ept[1], Y=ept[0], return_dist=True) 
        # returns distance based shortest path
        self.shortest_route = nx.shortest_path(graph, source=self.start_node, target=self.end_node, weight='length')
        
        self.shortest_dist  = sum(ox.utils_graph.get_route_edge_attributes(graph, self.shortest_route, 'length'))
        
        shortest_route_latlong = [[graph.nodes[route_node]['x'],graph.nodes[route_node]['y']] for route_node in self.shortest_route] 
        
        shortestPathStats = [shortest_route_latlong, self.shortest_dist, \
                            self.get_Elevation(self.shortest_route, cost_mode_2), self.get_Elevation(self.shortest_route, cost_mode_1)]


        shortestPathStats_copy = {}

        shortestPathStats_copy["route"] = shortestPathStats[0]
        shortestPathStats_copy["current_distance"] =shortestPathStats[1]
        shortestPathStats_copy["elevation_distance"]=shortestPathStats[2]
        shortestPathStats_copy["drop_dist"]=shortestPathStats[3]
        
        shortestPathStats = shortestPathStats_copy
        if(elev_perc == 0):
            return shortestPathStats, shortestPathStats

        shortest_dist = self.shortest_dist

        djikstra = Djikstra(graph, shortest_dist,self.start_node, self.end_node, elev_perc, elev_option)
        
        init = True
        start_time = time.time()
        djikstra.dijkstra_path()
        djik_path = djikstra.get_best_path()
        end_time = time.time()
     
        if log:
            print()
            print("Statics - Dijkstra's route")
            print(djik_path["elevation_distance"])
            print(djik_path["drop_dist"])
            print(djik_path["current_distance"])
            print("--- Time taken = %s seconds ---" % (end_time - start_time))


        a_str = A_star(graph, shortest_dist,self.start_node, self.end_node, elev_perc, elev_option)

        # self.best = [route[:], curr_dist, elevation_dist, dropDist]
        
        init = True
        start_time = time.time()
        a_str.a_star_path()
        a_str_path = a_str.get_best_path()
        end_time = time.time()
     
        if log:
            print()
            print("Statics - A Star's route")
            print(a_str_path["elevation_distance"])
            print(a_str_path["drop_dist"])
            print(a_str_path["current_distance"])
            print("--- Time taken = %s seconds ---" % (end_time - start_time))
   


        if self.elev_option == elev_type_0:
            if (djik_path["elevation_distance"] > a_str_path["elevation_distance"]) or (djik_path["elevation_distance"] == a_str_path["elevation_distance"] and djik_path["current_distance"] < a_str_path["current_distance"]):
                self.best_path = djik_path
                if log:
                    print("The Dijkstra algorithm computes the best possible route")
                    print()
            else:
                self.best_path = a_str_path
                if log:
                    print("The A star algorithm computes the best possible route")
                    print()
        else:
            if (djik_path["elevation_distance"] < a_str_path["elevation_distance"]) or (djik_path["elevation_distance"] == a_str_path["elevation_distance"] and djik_path["current_distance"] < a_str_path["current_distance"]):
                self.best_path = djik_path
                if log:
                    print("The Dijkstra algorithm computes the best possible route")
                    print()
            else:
                self.best_path = a_str_path
                if log:
                    print("The A star algorithm computes the best possible route")
                    print()

        return self.compare(graph, shortestPathStats)
