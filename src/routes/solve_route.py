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

    return optimal_route_dict

def solve_route_logic_internal(data):
    logging.debug("Función solve_route_logic_internal llamada")
    logging.debug(f"Datos recibidos: {data}")

    # Crear instancias de CustomPoint
    start_point = CustomPoint(**data['startPoint'])
    final_point = CustomPoint(**data['finalPoint'])
    delivery_points = [CustomPoint(**point) for point in data['deliveryPoints']]

    # Verificar si hay suficientes puntos para aplicar simulated annealing
    if len(delivery_points) > 0:
        optimal_route_heuristic = simulated_annealing([start_point] + delivery_points + [final_point], start_temp=9999, alpha=0.998, num_iterations=9999)
        optimal_route_dict = [point.to_list() for point in optimal_route_heuristic]
    else:
        # Si solo hay punto inicial y final, devuelve la ruta tal como está
        optimal_route_dict = [start_point.to_list(), final_point.to_list()]

    return optimal_route_dict
