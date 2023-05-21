from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('map.html')

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    waypoints = request.get_json()
    
    # Perform any necessary processing or calculations with the waypoints
    
    # Send back the same waypoints in the response
    response = {'coordinates': waypoints}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
