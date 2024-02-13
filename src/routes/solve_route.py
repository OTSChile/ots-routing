from flask import request, jsonify
from models.point import CustomPoint  # Asegúrate de importar las dependencias necesarias
from algorithms.heuristic_solver import simulated_annealing  # Importa las funciones necesarias
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def solve_route_logic():
    logging.debug("Endpoint /solve llamado")
    data = request.get_json()
    logging.debug(f"Datos recibidos: {data}")
    start_point, delivery_points, final_point = data['startPoint'], data['deliveryPoints'], data['finalPoint']
    start_point = CustomPoint(*start_point)
    delivery_points = [CustomPoint(*point) for point in delivery_points]
    final_point = CustomPoint(*final_point)

    optimal_route_heuristic, optimal_distance_heuristic = simulated_annealing([start_point] + delivery_points + [final_point], start_temp=9999, alpha=0.998, num_iterations=9999)
    optimal_route_dict = [point.to_list() for point in optimal_route_heuristic]

    return jsonify({
        'Ruta optimizada': optimal_route_dict
    })