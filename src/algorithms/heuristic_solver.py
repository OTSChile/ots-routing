import random
import math
import json

def read_points_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    start_point = tuple(data['startPoint'])
    delivery_points = [tuple(point) for point in data['deliveryPoints']]
    final_point = tuple(data['finalPoint'])
    
    return start_point, delivery_points, final_point

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def total_distance(route):
    return sum(calculate_distance(route[i], route[i+1]) for i in range(len(route) - 1))

def simulated_annealing(points, start_temp, alpha, num_iterations):
    current_temp = start_temp
    current_route = points[:]
    current_distance = total_distance(current_route)

    for i in range(num_iterations):
        # Disminuir la temperatura
        current_temp *= alpha

        # Intercambiar dos puntos aleatorios en la ruta
        idx1, idx2 = random.sample(range(len(points)), 2)
        new_route = current_route[:]
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]

        new_distance = total_distance(new_route)

        # Decide si aceptar la nueva ruta
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / current_temp):
            current_route, current_distance = new_route, new_distance

    return current_route, current_distance

# Usar la función
start_point, delivery_points, final_point = read_points_from_file('../data/input_data.txt')

# Crear una lista plana de puntos que incluya el punto de inicio, los puntos de entrega y el punto final
all_points = [start_point] + delivery_points + [final_point]

# Llamar a simulated_annealing con la lista de puntos completa
optimal_route, optimal_distance = simulated_annealing(all_points, start_temp=10000, alpha=0.995, num_iterations=10000)

print("Ruta óptima:", optimal_route)
print("Distancia óptima:", optimal_distance)
