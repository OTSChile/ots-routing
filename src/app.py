from flask import Flask, jsonify, request
from algorithms.point_assignment import main
from routes.solve_route import solve_route_logic
from routes.eta import calculate_time_to_points_logic
from routes.visualize_points import visualize_geofence
from routes.check_points import check_points_in_geofence
from routes.furthest_point import get_furthest_point
from routes.points_assigner import assign_points_logic
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_route():
    return solve_route_logic()
    

@app.route('/calculate-time', methods=['POST'])
def calculate_time_to_points():
    return calculate_time_to_points_logic()
    

@app.route('/visualize-geofence', methods=['POST'])
def visualize_geofence_endpoint():
    return visualize_geofence()


@app.route('/check_points_in_geofence', methods=['POST'])
def check_points():
    return check_points_in_geofence()


@app.route('/find_furthest_point', methods=['POST'])
def furthest_point():
    return get_furthest_point()

@app.route('/assign_points', methods=['POST'])
def assign_points():
    return assign_points_logic()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
