import osmnx as osx
import networkx as ntx
from collections import defaultdict
from heapq import *
import time

cost_mode_0 = "no_elevation"
cost_mode_1  = "elevation_drop"
cost_mode_2 = "elevation_gain"
cost_mode_3 = "elevation_difference"

elev_type_0 = "maximize"
elev_type_1 = "minimize"



class routing_algorithms:

    def __init__(self, graph, elev_perc = 0.0, elev_option = "maximize" ):
        self.graph = graph
        self.elev_option = elev_option
        self.elev_perc = elev_perc
        self.best = []
        self.end_node = None
        self.start_node = None

    def refresh_graph(self, graph):
        self.graph=graph


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




    def bfs_traversal(self):
        graph = self.graph
        start_node = self.start_node
        elev_option = self.elev_option
        elev_perc = self.elev_perc
        shortest_distance = self.shortest_distance
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

            for neighbour in graph.neighbours(temp_node):
                
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




