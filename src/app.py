from flask import Flask, render_template, jsonify, request
from NetworkMetrics.graph_data_processor import graph_data_processing
from RoutingAlgorithms.routing_algorithms import Algorithms


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('map.html')

def constructGraph(startpt, endpt):
    graph_abstraction = graph_data_processing()   
    graph = graph_abstraction.generate_graph(startpt, endpt) 
    return graph

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.get_json()
    
    # Perform any necessary processing or calculations with the waypoints
    print(data)

    # Instantiate Algorithms class to calculate shortest route    

    source_x = data['waypoints'][0]['lat']
    source_y = data['waypoints'][0]['lng']
    startpt = [source_x, source_y]

    destination_x = data['waypoints'][1]['lat']
    destination_y = data['waypoints'][1]['lng']
    endpt = [destination_x, destination_y]  

    graph = constructGraph(startpt, endpt)
 
    elev_perc = data['percentage']
    elev_option = data['option']

    algorithms_obj = Algorithms(graph, elev_perc, elev_option)
    shortestPathStats, best_path = algorithms_obj.get_shortest_path(startpt, endpt, elev_perc, elev_option)

    route = best_path["route"]
    elevation_dist = best_path["elevation_distance"]
    drop_dist = best_path["drop_dist"]
    curr_dist = best_path["current_distance"]

    # Send back the same waypoints in the response
    response = {'route': route,
                'elevation_dist': elevation_dist,
                'drop_dist': drop_dist,
                'curr_dist':curr_dist}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
