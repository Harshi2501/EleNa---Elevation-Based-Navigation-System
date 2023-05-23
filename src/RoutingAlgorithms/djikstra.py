import osmnx as ox
import networkx as nx
from collections import deque, defaultdict
from heapq import *
import time

cost_mode_0 = "no_elevation"
cost_mode_1  = "elevation_drop"
cost_mode_2 = "elevation_gain"
cost_mode_3 = "elevation_difference"

elev_type_0 = "max"
elev_type_1 = "min"

class Djikstra:
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
                return graph.edges[start, end]["weight"]
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

    """
    This function returns the nodes involved in the path from the starting point to the destination
    """

    def get_route(self, parent, end):
        path = []
        path.append(end)
        while parent[path[-1]]!=-1:
            path.append(parent[path[-1]])
        return path[::-1]
    
    """
    This function computes the path using bfs traversal
    """

    def bfs_traversal(self):
        graph = self.graph
        start_node = self.start_node
        elev_option = self.elev_option
        elev_perc = self.elev_perc
        shortest_distance = self.shortest_dist
        end_node = self.end_node
        start_node=self.start_node
        
        bfs_heap = [(0.0, 0.0, start_node)]

        visited = set()

        known = {start_node: 0}
        
        #stores information about previous node
        parent = defaultdict(int)
        parent[start_node]=-1

        while bfs_heap:
            temp_known, temp_dist, temp_node = heappop(bfs_heap)

            if temp_node in visited:
                continue

            visited.add(temp_node)

            if temp_node==end_node:
                break

            for neighbour in graph.neighbors(temp_node):
                
                if neighbour in visited:
                    continue

                p = known.get(neighbour, None)
                temp_distance = self.compute_cost(temp_node, neighbour, cost_mode_0)

                if elev_option==elev_type_0:
                    if elev_perc <= 0.5:
                        next_node_cost = temp_known+(temp_distance * 0.1 + self.compute_cost(temp_node, neighbour, cost_mode_1))
                    else:
                        next_node_cost = (temp_distance*0.1 - self.compute_cost(temp_node, neighbour, cost_mode_3))
                else:
                        next_node_cost = temp_known+(temp_distance * 0.1 + self.compute_cost(temp_node, neighbour, cost_mode_2))
                

                new_dist = temp_dist + temp_distance

                if new_dist <= shortest_distance*(1.0+elev_perc) and (p is None or next_node_cost < p):
                    parent[neighbour] = temp_node
                    known[neighbour] = next_node_cost
                    heappush(bfs_heap, (next_node_cost, new_dist, neighbour))

        if not temp_dist:
            return
        
        return parent, end_node, temp_dist

    """
    This function computes the path using the djikstras algorithm and sets the best_path variable accordingly
    """


    def dijkstra_path(self):        
        if not (self.start_node is None or self.end_node is None):
            parent_node,end_node,curr_dist=self.bfs_traversal()
            route = self.get_route(parent_node, end_node)
            elevation_dist, drop_dist = self.get_Elevation(route, cost_mode_2), self.get_Elevation(route, cost_mode_1)
            # self.best = [route[:], curr_dist, elevation_dist, dropDist]
            self.best_path["route"]= route[:]
            self.best_path["elevation_distance"]= elevation_dist
            self.best_path["drop_dist"]= drop_dist
            self.best_path["current_distance"]= curr_dist
        return

    """
    This function returns the best path
    """

    def get_best_path(self):
        return self.best_path
