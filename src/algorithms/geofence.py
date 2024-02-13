from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from models.point import *


def are_points_within_geofence(geocerca, custom_points):
    geofence = Polygon(geocerca)
    return [(point.id1, point.id2, geofence.contains(ShapelyPoint(point.x, point.y))) for point in custom_points]


def generate_geofence_image(geocerca, point_coords, image_path):
    # Crear un polígono para la geocerca
    geofence = Polygon(geocerca)

    # Preparar datos para el trazado de la geocerca
    x, y = geofence.exterior.xy

    # Crear el gráfico
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Geocerca')

    # Procesar cada punto en el arreglo de puntos
    for point in point_coords:
        ax.scatter(point.x, point.y, color='red')  # Usar las propiedades x e y directamente

    # Configurar título y leyenda
    ax.set_title("Visualización de la Geocerca y Puntos")
    ax.legend()

    # Guardar la imagen
    plt.savefig(image_path)
    plt.close(fig)