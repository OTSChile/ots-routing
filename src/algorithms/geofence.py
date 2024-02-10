from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

def check_location_in_geofence(lat, lon):
    coords = [
            (-33.43077086160599, -70.65358943339982), 
            (-33.42586179434257, -70.66844613427043), 
            (-33.42234980832767, -70.6715805748797), 
            (-33.413856129029476, -70.67935209478985),
            (-33.403032042703956, -70.68119887987973),
            (-33.39786958673203, -70.66952216368519),
            (-33.39550025505101, -70.65346641243725),
            (-33.397007069127824, -70.64281751984784),
            (-33.40123843017137, -70.63019179734725),
            (-33.4134245116657, -70.63087597921862),
            (-33.42159569083892, -70.63929113879249),
            (-33.42797349234883, -70.63963431927732),
            (-33.43420895948136, -70.63971834901717),
            (-33.43120055467563, -70.65234385048896),         
            ]

    geofence = Polygon(coords)
    location = Point(lat, lon)

    return geofence.contains(location)


def generate_geofence_image(coords, points_coords, image_path):
    # Crear un polígono para la geocerca
    geofence = Polygon(coords)

    # Preparar datos para el trazado de la geocerca
    x, y = geofence.exterior.xy

    # Crear el gráfico
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Geocerca')

    # Procesar cada punto en el arreglo de puntos
    for point_coord in points_coords:
        point = Point(point_coord)
        point_x, point_y = point.x, point.y
        ax.scatter(point_x, point_y, color='red')  # Puedes agregar una etiqueta si es necesario

    # Configurar título y leyenda
    ax.set_title("Visualización de la Geocerca y Puntos de Consulta")
    ax.legend()

    # Guardar la imagen
    plt.savefig(image_path)
    plt.close(fig)