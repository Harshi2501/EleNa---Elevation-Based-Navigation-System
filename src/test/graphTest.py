import networkx as nx
import sys
sys.path.append("..")
from NetworkMetrics.graph_data_processor import graph_data_processing

class GraphTest:
   
   def __init__(self, endpoint):
      self.endpoint = endpoint

   # Test Graph generation in class 'graph_data_processing'
   def testGraphGeneration(self):
       graph_data_processing_obj = graph_data_processing()
       generated_graph = graph_data_processing_obj.generate_graph(self.endpoint)
       assert isinstance(generated_graph, nx.classes.multidigraph.MultiDiGraph)
       print("Test Graph generation passed")
 
   def runAllTests(self):
       self.testGraphGeneration()
   
