from models.point import Point



def calcular_tiempo_hasta_cada_punto(ruta_optima):
    velocidad_promedio = 35
    tiempos = []
    tiempo_acumulado = 0

    for i in range(1, len(ruta_optima)):
        distancia = ruta_optima[i-1].distance_to(ruta_optima[i])
        tiempo = (distancia / velocidad_promedio) * 60  # Convertir a minutos
        tiempo_acumulado += tiempo
        horas = int(tiempo_acumulado // 60)
        minutos = int(tiempo_acumulado % 60)
        tiempos.append((horas, minutos))

    return tiempos