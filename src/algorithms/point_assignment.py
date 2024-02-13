import json
import os
import logging
from models.point import CustomPoint
from algorithms.vehicle_filter import aplicar_reglas_vehiculo
from routes.solve_route import solve_route_logic_internal

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def leer_reglas_negocio():
    ruta_archivo = os.path.join(os.getcwd(), 'data/business_rules.json')
    with open(ruta_archivo, 'r') as file:
        return json.load(file)

def leer_vehiculos_disponibles():
    ruta_archivo = os.path.join(os.getcwd(), 'data/input_vehicles.json')
    with open(ruta_archivo, 'r') as file:
        return json.load(file)

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

def es_hora_de_optimizar(asignacion, vehiculo, puntos_no_asignados):
    return any([
        asignacion["peso_total"] >= vehiculo["capacidad_peso"],
        asignacion["volumen_total"] >= vehiculo["capacidad_volumen"],
        asignacion["bultos_total"] >= vehiculo.get("bultos_maximo", float('inf')),
        not puntos_no_asignados
    ])

def actualizar_asignacion(asignacion, punto):
    asignacion["peso_total"] += punto.peso
    asignacion["volumen_total"] += punto.volumen
    asignacion["bultos_total"] += punto.bultos
    asignacion["puntos_asignados"].append(punto.to_dict())

def reiniciar_asignacion(asignacion):
    asignacion["peso_total"] = 0
    asignacion["volumen_total"] = 0
    asignacion["bultos_total"] = 0

def construir_resultado_final(asignaciones):
    rutas_propuestas = []
    peso_total_todas_rutas = 0
    volumen_total_todas_rutas = 0
    bultos_total_todas_rutas = 0

    for vehiculo_id, asignacion in asignaciones.items():
        if vehiculo_id != "paquetes_no_asignados":
            # Agregar la ruta propuesta para cada vehículo
            ruta = {
                "IDvehiculoAsignado": vehiculo_id,
                "PesoTotalRuta": asignacion["peso_total"],
                "VolumenTotalRuta": asignacion["volumen_total"],
                "BultosTotalRuta": asignacion["bultos_total"],
                "asignacion_id": f"asignacion_{vehiculo_id}",
                "puntos_asignados": asignacion["puntos_asignados"]
            }
            rutas_propuestas.append(ruta)

            # Actualizar los totales
            peso_total_todas_rutas += asignacion["peso_total"]
            volumen_total_todas_rutas += asignacion["volumen_total"]
            bultos_total_todas_rutas += asignacion["bultos_total"]

    resultado_final = {
        "PesoTotalTodasLasRutas": peso_total_todas_rutas,
        "VolumenTotalTodasLasRutas": volumen_total_todas_rutas,
        "TotalBultosTodasLasRutas": bultos_total_todas_rutas,
        "rutas_propuestas": rutas_propuestas
    }

    if "paquetes_no_asignados" in asignaciones:
        resultado_final["paquetes_no_asignados"] = asignaciones["paquetes_no_asignados"]

    return resultado_final


def agregar_ruta_propuesta(asignacion, rutas_propuestas, vehiculo_id, peso_total_todas_rutas, volumen_total_todas_rutas, bultos_total_todas_rutas):
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
        "asignacion_id": f"asignacion_{vehiculo_id}",
        "puntos_asignados": puntos_asignados
    }
    rutas_propuestas.append(ruta)


def optimizar_ruta(ruta):
    try:
        if len(ruta['puntos_asignados']) < 2:
            # Manejar el caso en que no hay suficientes puntos para optimizar
            return ruta['puntos_asignados']

        datos_solicitud = {
            'startPoint': ruta['puntos_asignados'][0],
            'deliveryPoints': ruta['puntos_asignados'][1:-1],
            'finalPoint': ruta['puntos_asignados'][-1]
        }

        ruta_optimizada = solve_route_logic_internal(datos_solicitud)
        return ruta_optimizada
    except Exception as e:
        logging.error(f"Error en optimizar_ruta {ruta}: {e}")
        # Manejar el error o devolver un valor predeterminado
        return ruta  # Devuelve la ruta sin optimizar en caso de error
    
def asignar_puntos_a_vehiculos(punto_inicial, puntos, vehiculos, reglas):
    logging.debug("asignar_puntos_a_vehiculos")
    try:
        vehiculos_con_reglas = [aplicar_reglas_vehiculo(vehiculo, reglas) for vehiculo in vehiculos if vehiculo.get("disponible", True)]
        asignaciones = {vehiculo["id"]: {"peso_total": 0, "volumen_total": 0, "bultos_total": 0, "puntos_asignados": []} for vehiculo in vehiculos_con_reglas}
        puntos_no_asignados = puntos.copy()

        for vehiculo in vehiculos_con_reglas:
            asignacion_actual = asignaciones[vehiculo["id"]]
            puntos_asignados_en_este_ciclo = []

            for punto in puntos_no_asignados:
                if cumple_capacidad(vehiculo, asignacion_actual, punto):
                    actualizar_asignacion(asignacion_actual, punto)
                    puntos_asignados_en_este_ciclo.append(punto)

                    if es_hora_de_optimizar(asignacion_actual, vehiculo, puntos_no_asignados):
                        asignacion_actual["puntos_asignados"] = optimizar_ruta(asignacion_actual["puntos_asignados"])
                        reiniciar_asignacion(asignacion_actual)

            puntos_no_asignados = [p for p in puntos_no_asignados if p not in puntos_asignados_en_este_ciclo]
            if not puntos_no_asignados:
                break

        if puntos_no_asignados:
            asignaciones["paquetes_no_asignados"] = puntos_no_asignados

        respuesta = construir_resultado_final(asignaciones)
        return respuesta
    except Exception as e:
        logging.error(f"Error general en asignar_puntos_a_vehiculos: {e}")
        return None

def cumple_capacidad(vehiculo, asignacion, punto):
    return (vehiculo["capacidad_peso"] - asignacion["peso_total"] >= punto.peso and
            vehiculo["capacidad_volumen"] - asignacion["volumen_total"] >= punto.volumen and
            vehiculo.get("bultos_maximo", float('inf')) - asignacion["bultos_total"] >= punto.bultos)

