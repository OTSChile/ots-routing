import json
import math
import logging

class CustomPoint:
    def __init__(self, id1, id2, x: float, y: float, peso=None, volumen=None, bultos=None):
        #logging.debug(f"Creando Point con id1={id1}, id2={id2}, x={x}, y={y}, peso={peso}, volumen={volumen}, bultos={bultos}")
        self.id1 = id1
        self.id2 = id2
        self.x = x
        self.y = y
        self.peso = peso
        self.volumen = volumen
        self.bultos = bultos

    def __repr__(self):
        return f"CustomPoint({self.id1}, {self.id2}, {self.x}, {self.y}, Peso: {self.peso}, Volumen: {self.volumen}, Bultos: {self.bultos})"

    def distance_to(self, other_point) -> float:
        """Calcula la distancia entre este punto y otro usando la fórmula Haversine."""
        R = 6371.0  # Radio de la Tierra en kilómetros

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
        return {
            'id1': self.id1, 'id2': self.id2, 'x': self.x, 'y': self.y,
            'peso': self.peso, 'volumen': self.volumen, 'bultos': self.bultos
        }

    def to_list(self):
        """Convierte el objeto Point en una lista."""
        return [self.id1, self.id2, self.x, self.y, self.peso, self.volumen, self.bultos]

def parse_point_from_string(point_str: str) -> CustomPoint:
    """Convierte una cadena de texto en formato '[id1, id2, x, y, peso, volumen, bultos]' a un objeto CustomPoint."""
    data = eval(point_str)
    return CustomPoint(*data)

def read_points_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    start_point = CustomPoint(*data['startPoint'])
    delivery_points = [CustomPoint(*point) for point in data['deliveryPoints']]
    final_point = CustomPoint(*data['finalPoint'])
    
    return start_point, delivery_points, final_point