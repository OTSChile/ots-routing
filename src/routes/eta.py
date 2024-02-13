from flask import jsonify, request
from models.point import CustomPoint
from algorithms.time_to_point import calcular_tiempo_desde_punto

def calculate_time_to_points_logic():
    data = request.get_json()
    punto_x = CustomPoint(*data['start_point'])
    puntos_destino = [CustomPoint(*coords) for coords in data['map_points']]
    velocidad_promedio = data.get('velocidad_promedio', 35)  # 35 km/h por defecto si no se especifica
    tiempo_adicional_por_parada = data.get('tiempo_adicional_por_parada', 5)

    tiempos = calcular_tiempo_desde_punto(punto_x, puntos_destino, velocidad_promedio, tiempo_adicional_por_parada)
    tiempos_formato = [{'tiempo': tiempo} for tiempo in tiempos]

    return jsonify(tiempos_formato)