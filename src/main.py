import logging
from datetime import datetime
from algorithms.heuristic_solver import simulated_annealing
from utils.data_loader import read_points_from_file

# Configurar el logging para mostrar mensajes en el nivel DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Cargar los puntos desde un archivo
    start_point, delivery_points, final_point = read_points_from_file('../data/input_data.txt')

    # Preparar todos los puntos para la solución heurística, incluyendo el punto de inicio, puntos de entrega, y punto final
    all_points = [start_point] + delivery_points + [final_point]

    # Registrar tiempo de inicio del solucionador heurístico
    start_time_heuristic = datetime.now()
    logging.debug(f"Inicio del solucionador heurístico: {start_time_heuristic}")

    # Resolver el problema usando el solucionador heurístico
    optimal_route_heuristic, optimal_distance_heuristic = simulated_annealing(all_points, start_temp=10000, alpha=0.995, num_iterations=10000)
    
    # Registrar tiempo de término del solucionador heurístico
    end_time_heuristic = datetime.now()
    logging.debug(f"Término del solucionador heurístico: {end_time_heuristic}")
    logging.debug(f"Duración del solucionador heurístico: {end_time_heuristic - start_time_heuristic}")

    print("\nSolución Heurística:")
    print("Distancia óptima:", optimal_distance_heuristic)
    print("Ruta óptima:", [repr(point) for point in optimal_route_heuristic])

if __name__ == "__main__":
    main()