from flask import request, jsonify
from algorithms.point_assignment import main

def assign_points_logic():
    data = request.get_json()
    punto_inicial = data.get('punto_inicial')  # Asegúrate de que esta estructura coincida con lo que envías
    puntos_a_visitar = data.get('puntos_a_visitar')  # Asegúrate de que esta estructura coincida con lo que envías

    if not punto_inicial or not puntos_a_visitar:
        return jsonify({"error": "Datos de entrada incompletos"}), 400

    resultado = main(punto_inicial, puntos_a_visitar)
    return jsonify(resultado)