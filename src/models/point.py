import json

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other_point) -> float:
        """Calcula la distancia Euclidiana entre este punto y otro."""
        return ((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2) ** 0.5


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