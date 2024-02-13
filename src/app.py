from flask import Flask, jsonify, request, send_file
from algorithms.heuristic_solver import simulated_annealing
from algorithms.time_to_point import calcular_tiempo_desde_punto
from models.point import CustomPoint
from algorithms.geofence import *
from algorithms.distance_calculator import *
from algorithms.point_assignment import main
from static.coords import geocerca

import logging

# Configura el logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_route():
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
        'Solucion Heuristica': {
            'Distancia': optimal_distance_heuristic,
            'Ruta sugerida': optimal_route_dict
        }
    })
    

@app.route('/calculate-time', methods=['POST'])
def calculate_time_to_points():
    data = request.get_json()
    punto_x = CustomPoint(*data['start_point'])
    puntos_destino = [CustomPoint(*coords) for coords in data['map_points']]
    velocidad_promedio = data.get('velocidad_promedio', 35)  # 35 km/h por defecto si no se especifica
    tiempo_adicional_por_parada = data.get('tiempo_adicional_por_parada', 5)

    tiempos = calcular_tiempo_desde_punto(punto_x, puntos_destino, velocidad_promedio, tiempo_adicional_por_parada)
    tiempos_formato = [{'tiempo': tiempo} for tiempo in tiempos]

    return jsonify(tiempos_formato)
    

@app.route('/visualize-geofence', methods=['POST'])
def visualize_geofence():
    data = request.get_json()

    raw_point_coords = data.get('point_coords')
    processed_point_coords = []

    if raw_point_coords:
        for point in raw_point_coords:
            logging.debug(f"Procesando punto: {point}, tipo: {type(point)}")
            if isinstance(point, list) and len(point) == 4:
                processed_point_coords.append(CustomPoint(*point))
            else:
                logging.error("Formato de punto incorrecto")
                return {"error": "Formato de punto incorrecto"}, 400
    else:
        return {"error": "Coordenadas no proporcionadas"}, 400

    image_path = 'geofence_visualization.png'

    # Asumiendo que geocerca es una lista de coordenadas definida en algún lugar de tu código
    if not geocerca:
        return {"error": "Geocerca no proporcionada"}, 400

    generate_geofence_image(geocerca, processed_point_coords, image_path)

    return send_file(image_path, mimetype='image/png')


@app.route('/check_points_in_geofence', methods=['POST'])
def check_points_in_geofence():
    data = request.get_json()
    
    # Extraer la geocerca y los puntos de la solicitud
    points_to_check = data.get('points_to_check')

    if not geocerca or not points_to_check:
        return jsonify({"error": "Faltan datos de entrada"}), 400

    checkeable_points = [CustomPoint(*point) for point in points_to_check]
    # Llamar a la función para verificar los puntos
    inside_geofence = are_points_within_geofence(geocerca, checkeable_points)

    # Devolver los resultados
    return jsonify({"inside_geofence": inside_geofence})


@app.route('/find_furthest_point', methods=['POST'])
def get_furthest_point():
    data = request.get_json()

    reference_data = data.get('reference_point')
    points_data = data.get('other_points')

    if not reference_data or not points_data:
        return jsonify({"error": "Datos de entrada incompletos"}), 400

    try:
        reference_point = CustomPoint(*reference_data)
        other_points = [CustomPoint(*point) for point in points_data]

        furthest_point, max_distance = find_furthest_point(reference_point, other_points)

        return jsonify({
            "furthest_point": {
                "id1": furthest_point.id1,
                "id2": furthest_point.id2,
                "latitude": furthest_point.x,
                "longitude": furthest_point.y
            },
            "distance_km": max_distance
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assign_points', methods=['POST'])
def assign_points():
    data = request.get_json()
    punto_inicial = data.get('punto_inicial')  # Asegúrate de que esta estructura coincida con lo que envías
    puntos_a_visitar = data.get('puntos_a_visitar')  # Asegúrate de que esta estructura coincida con lo que envías

    if not punto_inicial or not puntos_a_visitar:
        return jsonify({"error": "Datos de entrada incompletos"}), 400

    resultado = main(punto_inicial, puntos_a_visitar)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
