from utils.data_loader import read_points_from_file
from algorithms.exact_solver import held_karp
from algorithms.heuristic_solver import simulated_annealing
    
def main():
    # Cargar los puntos desde un archivo
    start_point, delivery_points, final_point = read_points_from_file('../data/input_data.txt')
    points = read_points_from_file('../data/input_data.txt')

    # Resolver el problema usando el solucionador exacto
    optimal_distance_exact, optimal_path_exact = held_karp(start_point, delivery_points, final_point)
    print("Solución Exacta:")
    print("Distancia óptima:", optimal_distance_exact)
    print("Ruta óptima:", optimal_path_exact)

    # Resolver el problema usando el solucionador heurístico
    optimal_route_heuristic, optimal_distance_heuristic = simulated_annealing(points, start_temp=10000, alpha=0.995, num_iterations=10000)
    print("\nSolución Heurística:")
    print("Distancia óptima:", optimal_distance_heuristic)
    print("Ruta óptima:", optimal_route_heuristic)

if __name__ == "__main__":
    main()
