import networkx as nx
import sys
sys.path.append("..")
from NetworkMetrics.graph_data_processor import graph_data_processing
from RoutingAlgorithms.routing_algorithms import Algorithms

class AlgorithmsTest:

    def __init__(self, algorithms_obj, graph, route):
        self.algorithms_obj = algorithms_obj
        self.graph = graph   
        self.route = route 
 
    def test_compute_cost_method(self):
        # Test compute_cost method in Routing Algorithms
        node_source = 0 
        node_destination = 1 
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "no_elevation")        
        assert isinstance(cost, float)
        assert cost == 3.0

        node_source = 1
        node_destination = 0
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "no_elevation")   
        assert isinstance(cost, float)
        assert cost == 3.0

        node_source = 2
        node_destination = 6
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_drop")
        assert isinstance(cost, float)
        assert cost == 0.0

        node_source = 6
        node_destination = 2
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_drop")
        assert isinstance(cost, float)
        assert cost == 4.0

        node_source = 4
        node_destination = 1
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_gain")
        assert isinstance(cost, float)
        assert cost == 0.0

        node_source = 1
        node_destination = 4
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_gain")
        assert isinstance(cost, float)
        assert cost == 1.0

        node_source = 0
        node_destination = 3
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_difference")
        assert isinstance(cost, float)
        assert cost == 1.0
    
        node_source = 3
        node_destination = 0
        cost = self.algorithms_obj.compute_cost(node_source, node_destination, cost_type = "elevation_difference")
        assert isinstance(cost, float)
        assert cost == -1.0

        print("All compute cost tests passed")     

    def test_elevation_elevation_difference(self):
        # Test elevation method in Routing algorithms
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_difference")
        assert isinstance(total_elevation, float)
        assert total_elevation == 0.0
        print("Test - test_elevation_elevation_difference passed")

    def test_elevation_gain(self):
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_gain")
        assert isinstance(total_elevation, float)
        assert total_elevation == 1.0
        print("Test - test_elevation_gain passed")

    def test_elevation_drop(self):
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_drop")
        assert isinstance(total_elevation, float)
        assert total_elevation == 1.0
        print("Test - test_elevation_drop")

    def test_elevation_no_elevation(self): 
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "no_elevation")
        assert isinstance(total_elevation, float)
        assert total_elevation == 6.726999999999999
        print("Test - test_elevation_no_elevation passed")   
 
    def test_elevation_method(self):
       self.test_elevation_elevation_difference()
       self.test_elevation_gain()
       self.test_elevation_drop()
       self.test_elevation_no_elevation()
       print("All elevation tests passed")

    def test_shortest_path_maximize_elevation(self, generated_graph, source, destination, elev_perc):
        # Test shortest path method in routing algorithms to maximize elevation
    
        new_algorithms_obj = Algorithms(generated_graph, elev_perc = 100.0, elev_option = "max")
        shortest_path, best_path = new_algorithms_obj.get_shortest_path(source, destination, elev_perc, elev_option = "max", log = False)
        assert best_path["current_distance"] <= (1 + elev_perc/100.0)*shortest_path["current_distance"]
        assert best_path["elevation_distance"] >= shortest_path["elevation_distance"]
        print("Test - test_shortest_path_maximize_elevation passed")

    def test_shortest_path_minimize_elevation(self, generated_graph, source, destination, elev_perc):
        # Test shortest path method in routing algorithms to minimize elevation 
       
        new_algorithms_obj = Algorithms(generated_graph, elev_perc = 100.0, elev_option = "min") 
        shortest_path, best_path = new_algorithms_obj.get_shortest_path(source, destination, elev_perc, elev_option = "min", log = False)
        assert best_path["current_distance"] <= (1 + elev_perc/100.0)*shortest_path["current_distance"]
        assert best_path["elevation_distance"] <= shortest_path["elevation_distance"]
        print("Test - test_shortest_path_minimize_elevation passed")

    def test_shortest_path_method(self):
        source = (42.3762, -72.5148)
        destination = (42.3948, -72.5266)
        graph_data_processing_obj = graph_data_processing()
        generated_graph = graph_data_processing_obj.generate_graph(destination)
        assert isinstance(generated_graph, nx.classes.multidigraph.MultiDiGraph)
        elev_perc = 100.0

        self.test_shortest_path_maximize_elevation(generated_graph, source, destination, elev_perc)
        self.test_shortest_path_minimize_elevation(generated_graph, source, destination, elev_perc)
        print("All shortest path tests passed")

    def runAllTests(self):
       self.test_compute_cost_method()
       self.test_elevation_method()
       self.test_shortest_path_method()
