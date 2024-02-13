import json
import os
from utils.data_loader import read_points_from_file
from models.point import CustomPoint
from algorithms.vehicle_filter import aplicar_reglas_vehiculo


def leer_reglas_negocio():
    ruta_archivo = os.path.join(os.getcwd(), 'data/business_rules.json')
    with open(ruta_archivo, 'r') as file:
        return json.load(file)

def leer_vehiculos_disponibles():
    ruta_archivo = os.path.join(os.getcwd(), 'data/input_vehicles.json')
    with open(ruta_archivo, 'r') as file:
        return json.load(file)


def asignar_puntos_a_vehiculos(punto_inicial, puntos, vehiculos, reglas):
    # Aplicar reglas a vehículos
    vehiculos_con_reglas = []
    for vehiculo in vehiculos:
        vehiculo_modificado = aplicar_reglas_vehiculo(vehiculo, reglas)
        if vehiculo_modificado is not None:
            vehiculos_con_reglas.append(vehiculo_modificado)

    #asignaciones = []
    asignaciones = {vehiculo["id"]: {"peso_total": 0, "volumen_total": 0, "bultos_total": 0, "puntos_asignados": []} for vehiculo in vehiculos_con_reglas}
    puntos_no_asignados = puntos.copy()
    punto_actual = punto_inicial  # Asumiendo que el primer punto es el inicial

    while puntos_no_asignados:
        # Encuentra el punto más cercano
        punto_mas_cercano = min(puntos_no_asignados, key=lambda p: CustomPoint.distance_to(punto_actual, p))
        puntos_no_asignados.remove(punto_mas_cercano)

        # Encuentra un vehículo disponible para este punto
        for vehiculo in vehiculos_con_reglas:
            asignacion_actual = asignaciones[vehiculo["id"]]
            # Verificar si el vehículo puede llevar el punto
            if (vehiculo["capacidad_peso"] - asignacion_actual["peso_total"] >= punto_mas_cercano.peso and
                vehiculo["capacidad_volumen"] - asignacion_actual["volumen_total"] >= punto_mas_cercano.volumen and
                vehiculo.get("bultos_maximo", float('inf')) - asignacion_actual["bultos_total"] >= punto_mas_cercano.bultos):
                
                # Actualizar la carga, el volumen y los bultos utilizados del vehículo
                asignacion_actual["peso_total"] += punto_mas_cercano.peso
                asignacion_actual["volumen_total"] += punto_mas_cercano.volumen
                asignacion_actual["bultos_total"] += punto_mas_cercano.bultos
                asignacion_actual["puntos_asignados"].append(punto_mas_cercano.to_dict())

                # Actualiza el punto actual al último punto asignado
                punto_actual = punto_mas_cercano
                break

    rutas_propuestas = []
    peso_total_todas_rutas = 0
    volumen_total_todas_rutas = 0
    bultos_total_todas_rutas = 0

    for vehiculo_id, asignacion in asignaciones.items():
        peso_total_ruta = asignacion["peso_total"]
        volumen_total_ruta = asignacion["volumen_total"]
        bultos_total_ruta = asignacion["bultos_total"]
        puntos_asignados = asignacion["puntos_asignados"]

        peso_total_todas_rutas += peso_total_ruta
        volumen_total_todas_rutas += volumen_total_ruta
        bultos_total_todas_rutas += bultos_total_ruta

        ruta = {
            "IDvehiculoAsignado": vehiculo_id,
            "PesoTotalRuta": peso_total_ruta,
            "VolumenTotalRuta": volumen_total_ruta,
            "BultosTotalRuta": bultos_total_ruta,
            "asignacion_id": f"asignacion_{vehiculo_id}",  # Modificar según sea necesario
            "puntos_asignados": puntos_asignados
        }

        rutas_propuestas.append(ruta)

    return {
        "PesoTotalTodasLasRutas": peso_total_todas_rutas,
        "VolumenTotalTodasLasRutas": volumen_total_todas_rutas,
        "TotalBultosTodasLasRutas": bultos_total_todas_rutas,
        "rutas_propuestas": rutas_propuestas
    }



def main(punto_inicial_data, puntos_a_visitar_data):
    reglas_negocio = leer_reglas_negocio()
    vehiculos = leer_vehiculos_disponibles()
    
    punto_inicial = CustomPoint(*punto_inicial_data)
    puntos_a_visitar = [CustomPoint(*punto) for punto in puntos_a_visitar_data]

    resultado_asignacion = asignar_puntos_a_vehiculos(punto_inicial, puntos_a_visitar, vehiculos, reglas_negocio)

    # Preparar el response
    response = {
        "status": "success",
        "data": resultado_asignacion,
        "message": "Puntos asignados correctamente."
    }

    return response