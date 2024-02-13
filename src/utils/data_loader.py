import json
from models.point import CustomPoint

def read_points_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    start_point = CustomPoint(*data['startPoint'])
    delivery_points = [Point(*point) for point in data['deliveryPoints']]
    final_point = CustomPoint(*data['finalPoint'])
    
    return start_point, delivery_points, final_point
