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

        if self.start_node is None or self.end_node is None:
            return False
        return True

    def get_route(self, parent_node, dest):
        path = [dest]
        curr_node = parent_node[dest]
        while curr_node!=-1:
            path.append(curr_node)
            curr_node = parent_node[curr_node]
        return list(reversed(path))


    def get_elev_cost(self, route, cost_type = cost_mode_3):
        # For a particular route, the function returrns the total or piecewise cost.
        total = 0
        elevation_cost=0
        for i in range(len(route)-1):
            if cost_type == cost_mode_3:
                elevation_cost = self.compute_cost(route[i],route[i+1],cost_mode_3)	
            elif cost_type == cost_mode_2:
                elevation_cost = self.compute_cost(route[i],route[i+1],cost_mode_2)
            elif cost_type == cost_mode_1:
                elevation_cost = self.compute_cost(route[i],route[i+1],cost_mode_1)
            elif cost_type == cost_mode_0:
                elevation_cost = self.compute_cost(route[i],route[i+1],cost_mode_0)
            total += elevation_cost
        return total



    def dijkstra_path(self):
        #Implements Dijkstra's Algorithm
        print("inside")
        if not (self.start_node is None or self.end_node is None):
            parent_node,end_node,curr_dist=self.bfs_traversal()
            route = self.get_route(parent_node, end_node)
            elevation_dist, dropDist = self.get_Elevation(route, cost_mode_2), self.get_Elevation(route, cost_mode_1)
            self.best = [route[:], curr_dist, elevation_dist, dropDist]

        return


    def get_route_a_star(self, nodes, curr_node):
        if not nodes or not curr_node:
            return 
        path = [curr_node]
        while curr_node in nodes:
            curr_node = nodes[curr_node]
            path.append(curr_node)
        
        return path

    def compute_initial_cost_a_star(self, graph):
        cost = {}

        for node in graph.nodes():
            cost[node] = float("inf")
        
        cost[self.start_node] = 0

        return cost
    
    def a_star(self):
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

        while(len(unvisited) > 0):
            curr_node = min([(node,updated_weights[node]) for node in unvisited], key=lambda t: t[1])[0]            
            if curr_node == end_node:
                path=self.get_route_a_star(lcn, curr_node)
                print(path)
                self.best = [path[:], self.get_elev_cost(path, cost_mode_0), self.get_elev_cost(path, cost_mode_2), self.get_Elevation(path, cost_mode_1)]
                return

            unvisited.remove(curr_node)
            visited.add(curr_node)
            

            for neighbour in graph.neighbours(curr_node):
                if neighbour not in visited:
                    if elev_option == elev_type_1:
                        new_cost = graph_weights[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_2)
                    elif elev_option == elev_type_1:
                        new_cost = graph_weights[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_1)
    
                    new_cost_heuristics = new_cost_heuristics[curr_node] + self.compute_cost(curr_node, neighbour, cost_mode_0)

                    if neighbour not in unvisited and new_cost<=(1+elev_perc)*shortest_dist:
                        unvisited.add(neighbour)
                    else: 
                        if (new_cost >= new_cost[neighbour]) or (new_cost>=(1+elev_perc)*shortest_dist):
                            continue 

            lcn[neighbour] = curr_node
            new_cost[neighbour] = new_cost
            new_cost_heuristics[neighbour] = new_cost_heuristics
            updated_weights[neighbour] = new_cost[neighbour] + graph.nodes[neighbour]['dist_from_dest']*0.1

