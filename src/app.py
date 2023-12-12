from flask import Flask, jsonify, request
from algorithms.heuristic_solver import simulated_annealing
from algorithms.time_to_point import calcular_tiempo_hasta_cada_punto
from models.point import Point

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_route():
    data = request.get_json()
    start_point, delivery_points, final_point = data['startPoint'], data['deliveryPoints'], data['finalPoint']
    start_point = Point(*start_point)
    delivery_points = [Point(*point) for point in delivery_points]
    final_point = Point(*final_point)
    

    optimal_route_heuristic, optimal_distance_heuristic = simulated_annealing([start_point] + delivery_points + [final_point], start_temp=10000, alpha=0.995, num_iterations=10000)
    optimal_route_dict = [point.to_list() for point in optimal_route_heuristic]
    
    return jsonify({
        'Solucion Heuristica': {
            'Distancia': optimal_distance_heuristic,
            'Ruta sugerida': optimal_route_dict
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
