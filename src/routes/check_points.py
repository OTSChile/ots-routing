from flask import jsonify, request
from static.coords import geocerca
from models.point import CustomPoint
from algorithms.geofence import are_points_within_geofence

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