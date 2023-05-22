

class AlgorithmsTest:

    def __init__(self, algorithms_obj, graph, route):
        self.algorithms_obj = algorithms_obj
        self.graph = graph   
        self.route = route 
  
    def test_elevation_elevation_difference(self):
        # Test elevation method in Routing algorithms
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_difference")
        assert isinstance(total_elevation, float)
        assert total_elevation == 0.0

    def test_elevation_gain(self):
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_gain")
        assert isinstance(total_elevation, float)
        assert total_elevation == 1.0

    def test_elevation_drop(self):
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "elevation_drop")
        assert isinstance(total_elevation, float)
        assert total_elevation == 1.0

    def test_elevation_no_elevation(self): 
        total_elevation = self.algorithms_obj.get_Elevation(self.route, cost_type = "no_elevation")
        assert isinstance(total_elevation, float)
        print("total_elevation: " + str(total_elevation))
        assert total_elevation == 6.726999999999999

    def runAllTests(self):
       self.test_elevation_elevation_difference()
       self.test_elevation_gain()
       self.test_elevation_drop()
       self.test_elevation_no_elevation()
