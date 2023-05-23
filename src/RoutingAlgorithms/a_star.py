import osmnx as ox
import networkx as nx
from collections import deque, defaultdict
from heapq import *
import time

"""
This class is used to identify the shortest path using the a* algorithm
"""


cost_mode_0 = "no_elevation"
cost_mode_1  = "elevation_drop"
cost_mode_2 = "elevation_gain"
cost_mode_3 = "elevation_difference"

elev_type_0 = "max"
elev_type_1 = "min"

class A_star:
    def __init__(self, graph, shortest_dist,  start_node, end_node, elev_perc = 0.0, elev_option = elev_type_0):
        self.graph = graph
        self.elev_option = elev_option
        self.elev_perc = elev_perc
        # self.best = [[], 0.0, float('-inf'), 0.0]
        self.best_path = {}
        self.best_path["route"]= []
        self.best_path["elevation_distance"]= float("-inf")
        self.best_path["drop_dist"]= 0.0
        self.best_path["current_distance"]= 0.0
        self.start_node= start_node
        self.end_node =end_node
        self.shortest_dist=shortest_dist

    """
    This function calculates the cost from the starting point to the destination depending on the cost mode in terms on elevation gain, drop and differnence
    """

    def compute_cost(self, start, end, cost_type = cost_mode_0):
        graph = self.graph   
        if start is None or end is None:
            return 0
        if cost_type == cost_mode_0:
            try:
                return graph.edges[start, end ,0]["length"]
            except : 
                return 0
        elif cost_type == cost_mode_3:
            return graph.nodes[end]["elevation"] - graph.nodes[start]["elevation"]
        elif cost_type == cost_mode_2:
            return max(0.0, graph.nodes[end]["elevation"] - graph.nodes[start]["elevation"])
        elif cost_type == cost_mode_1:
            return max(0.0, graph.nodes[start]["elevation"] - graph.nodes[end]["elevation"])
        else:
            return abs(graph.nodes[start]["elevation"] - graph.nodes[end]["elevation"])
   
    """
    This function calculates the elevation for a route depending on the cost mode in terms on elevation gain, drop and differnence
    """

    def get_Elevation(self, route, cost_type = cost_mode_3):
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
    
    """
    This function returns the nodes involved in the path from the starting point to the destination
    """

    def get_route_a_star(self, nodes, curr_node):
        if not nodes or not curr_node:
            return 
        path = [curr_node]
        while curr_node in nodes:
            curr_node = nodes[curr_node]
            path.append(curr_node)
        
        return path

    """
    This function sets the initial cost to infinity for all nodes except the first node
    """


    def compute_initial_cost_a_star(self, graph):
        cost = {}

        for node in graph.nodes():
            cost[node] = float("inf")
        
        cost[self.start_node] = 0

        return cost
    
    """
    This function computes the path using the a* algorithm and sets the best_path variable accordingly
    """
    
    def a_star_path(self):
        if self.start_node is None or self.end_node is None:
            return
        visited = set()
        unvisited = set()

        updated_weights = {}
        lcn = {}

        graph = self.graph
        shortest_dist = self.shortest_dist
        elev_perc = self.elev_perc
        elev_option = self.elev_option
        start_node = self.start_node
        end_node = self.end_node

        unvisited.add(start_node)

        graph_weights = self.compute_initial_cost_a_star(graph)
        heuristics_graph_weights = self.compute_initial_cost_a_star(graph)

        updated_weights[start_node] = graph.nodes[start_node]['dist_from_dest']*0.1

        while len(unvisited) :
            curr_node = min([(node,updated_weights[node]) for node in unvisited], key=lambda t: t[1])[0]            
            if curr_node == end_node:
                route=self.get_route_a_star(lcn, curr_node)
                elevation_dist = self.get_Elevation(route, cost_mode_0)
                drop_dist = self.get_Elevation(route, cost_mode_2)
                curr_dist = self.get_Elevation(route, cost_mode_1)
                
                self.best_path["route"]= route[:]
                self.best_path["elevation_distance"]= elevation_dist
                self.best_path["drop_dist"]= drop_dist
                self.best_path["current_distance"]= curr_dist

                return


            unvisited.remove(curr_node)
            visited.add(curr_node)
            
            # new_cost, new_cost_heuristics = 0.0,0.0
            for neighbour in graph.neighbors(curr_node):
                if neighbour in visited:
                    continue
                if elev_option == elev_type_1:
                    new_cost = graph_weights[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_2)
                elif elev_option == elev_type_0:
                    new_cost = graph_weights[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_1)

                new_cost_heuristics = heuristics_graph_weights[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_0)

                if neighbour not in unvisited and new_cost_heuristics<=(1+elev_perc)*shortest_dist:
                    unvisited.add(neighbour)
                else: 
                    if (new_cost >= graph_weights[neighbour]) or (new_cost_heuristics>=(1+elev_perc)*shortest_dist):
                        continue 

                lcn[neighbour] = curr_node
                graph_weights[neighbour] = new_cost
                heuristics_graph_weights[neighbour] = new_cost_heuristics
                updated_weights[neighbour] = graph_weights[neighbour] + graph.nodes[neighbour]['dist_from_dest']*0.1


    """
    This function returns the best path
    """
    def get_best_path(self):
        return self.best_path
