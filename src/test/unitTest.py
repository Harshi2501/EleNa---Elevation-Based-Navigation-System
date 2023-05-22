import osmnx as ox
import networkx as nx

class UnitTest:

    def __init__(self, elev_perc = 0.0, elev_option = "maximize"):
       # Create a graph to test different functionalities of the program
       graph = nx.Graph()

       # Create an Algorithms object to test routing algorithms
       algorithms_obj = Algorithms(graph, elev_perc, elev_option)

       elevations = [0.0, 0.0, 0.0, 1.0, 1.0, 3.0, 4.0, 0.0, 0.0]

       # Add nodes to the graph
       for i in range(6):
           graph.add_node(i, elevations[i])

       # Add edges to the graph    
       edges = [(0 , 1, 5.0), (1, 2, 2.0), (0, 3, 1.414), (3, 4, 41.0), (4, 2, 1.313), (0, 5, 4.24), (5, 2, 4.04), (0, 6, 5.8), (6, 2, 9.10)]
       for edge in edges:
           graph.add_weighted_edges_from(edge)


if __name__ == "__main__":
 
      # Test graph generation
      graphTest = GraphTest()
      graphTest.runAllTests()

      # Test functionalities of the routing algorithms
      algorithmsTest = AlgorithmsTest()
      algorithmsTest.runAllTests()

      # Test functionalities of the front-end
      frontEndTest = FrontEndTest()
      frontEndTest.runAllTests() 
