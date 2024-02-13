from flask import request, send_file
from models.point import CustomPoint
from algorithms.geofence import generate_geofence_image
from algorithms.distance_calculator import *
from static.coords import geocerca

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

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