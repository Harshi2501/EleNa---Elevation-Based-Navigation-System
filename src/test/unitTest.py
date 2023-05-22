import osmnx as ox
import networkx as nx
from graphTest import GraphTest
from algorithmsTest import AlgorithmsTest
import sys
sys.path.append("..")
from RoutingAlgorithms.routing_algorithms import Algorithms

class UnitTest:

    def __init__(self, elev_perc = 0.0, elev_option = "maximize"):
       # Create a graph to test different functionalities of the program
       self.graph = nx.Graph()

       # Create an Algorithms object to test routing algorithms
       self.algorithms_obj = Algorithms(self.graph, elev_perc, elev_option)

       elevations = [0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 4.0, 0.0, 0.0]

       # Add nodes to the graph
       for i in range(6):
           self.graph.add_node(i, elevation = elevations[i])

       # Add edges to the graph    
       # edges = [(0,1,5.0), (1,2,2.0), (0,3,1.414), (3,4,41.0), (4,2,1.313), (0,5,4.24), (5,2,4.04), (0,6,5.8), (6,2,9.10)]
       edges = [(0,1,3.0), (1,2,3.0), (0,3,1.414), (3,4,4.0), (4,2,1.313), (0,5,4.24), (5,2,4.24), (0,6,5.0), (6,2,5.0)]
       self.graph.add_weighted_edges_from(edges)
    
       self.source = (42.373222, -72.519852)
       self.destination = (42.375544, -72.524210)

       # Have a route to test elevation in routing algorithms
       self.route = [0, 3, 4, 2]

    def runAllTests(self):
        # Test graph generation
        graphTest = GraphTest(self.destination)
        graphTest.runAllTests()

        # Test functionalities of the routing algorithms
        algorithmsTest = AlgorithmsTest(self.algorithms_obj, self.graph, self.route)
        algorithmsTest.runAllTests()

        # Test functionalities of the front-end
        #frontEndTest = FrontEndTest()
        #frontEndTest.runAllTests()

if __name__ == "__main__":

      # Instantiate test class and call the tests
      unit_test_obj = UnitTest(0.0, "maximize")
      unit_test_obj.runAllTests()
 
