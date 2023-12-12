import json
import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other_point) -> float:
        """Calcula la distancia entre este punto y otro usando la fórmula Haversine."""
        # Radio de la Tierra en kilómetros
        R = 6371.0

        lat1 = math.radians(self.x)
        lon1 = math.radians(self.y)
        lat2 = math.radians(other_point.x)
        lon2 = math.radians(other_point.y)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance
    
    def to_dict(self):
        """Convierte el objeto Point en un diccionario."""
        return {'x': self.x, 'y': self.y}
    def to_list(self):
        """Convierte el objeto Point en una lista [x, y]."""
        return [self.x, self.y]


def parse_point_from_string(point_str: str) -> Point:
    """Convierte una cadena de texto en formato '[x, y]' a un objeto Point."""
    x, y = eval(point_str)
    return Point(x, y)


def read_points_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    start_point = Point(*data['startPoint'])
    delivery_points = [Point(*point) for point in data['deliveryPoints']]
    final_point = Point(*data['finalPoint'])
    
    return start_point, delivery_points, final_point