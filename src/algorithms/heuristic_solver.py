import random
import math
import logging
from models.point import Point, read_points_from_file

# Configura el logging para mostrar mensajes debug
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def total_distance(route):
    """Calcula la distancia total de una ruta de puntos utilizando Haversine."""
    return sum(point.distance_to(next_point) for point, next_point in zip(route, route[1:]))

def simulated_annealing(all_points, start_temp, alpha, num_iterations):
    current_temp = start_temp
    current_route = all_points[:]
    current_distance = total_distance(current_route)


    for i in range(num_iterations):
        # Disminuir la temperatura
        current_temp *= alpha

        # Intercambiar dos puntos aleatorios en la ruta
        idx1, idx2 = random.sample(range(1, len(all_points) - 1), 2)  # Excluye el inicio y el final para intercambio
        new_route = current_route[:]
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]

        new_distance = total_distance(new_route)

        # Decide si aceptar la nueva ruta
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / current_temp):
            current_route, current_distance = new_route, new_distance


    return current_route, current_distance
