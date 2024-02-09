from models.point import Point

def calcular_tiempo_desde_punto(punto_x, puntos_destino, velocidad_promedio, tiempo_adicional_por_parada):
    """
    Calcula el tiempo estimado desde un punto X hasta cada punto en una lista de destinos,
    añadiendo un tiempo adicional en cada parada.

    :param punto_x: Punto de origen (Point).
    :param puntos_destino: Lista de puntos de destino (Point).
    :param velocidad_promedio: Velocidad promedio de viaje en km/h.
    :param tiempo_adicional_por_parada: Tiempo adicional en cada parada (en minutos).
    :return: Lista de tiempos estimados para llegar a cada punto de destino desde punto X,
             con el tiempo adicional incluido.
    """
    tiempos = []
    tiempo_acumulado = 0  # Inicia el tiempo acumulado

    try:
        for punto in puntos_destino:
            distancia = punto_x.distance_to(punto)
            tiempo_viaje = (distancia / velocidad_promedio) * 60  # Convertir a minutos
            tiempo_acumulado += tiempo_viaje + tiempo_adicional_por_parada  # Suma el tiempo de viaje y el adicional
            horas = int(tiempo_acumulado // 60)
            minutos = int(tiempo_acumulado % 60)
            tiempos.append(f"{horas:02d}:{minutos:02d}")  # Formato hh:mm
    except TypeError as e:
        print(f"Error en el tipo de datos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

    return tiempos