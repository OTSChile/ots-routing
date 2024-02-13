from flask import request, jsonify
from models.point import CustomPoint
from algorithms.distance_calculator import find_furthest_point

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