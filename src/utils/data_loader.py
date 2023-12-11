import json
from models.point import Point

def read_points_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    start_point = Point(*data['startPoint'])
    delivery_points = [Point(*point) for point in data['deliveryPoints']]
    final_point = Point(*data['finalPoint'])
    
    return start_point, delivery_points, final_point
