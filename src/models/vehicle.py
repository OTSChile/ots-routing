import json

class Vehiculo:
    def __init__(self, id: str, capacidad_peso: float, capacidad_volumen: float, tipo: str, disponible: bool):
        self.id = id
        self.capacidad_peso = capacidad_peso
        self.capacidad_volumen = capacidad_volumen
        self.tipo = tipo
        self.disponible = disponible
        
        # Puedes añadir más atributos si son necesarios

    def __repr__(self):
        return f"Vehiculo(ID: {self.id}, Capacidad de Peso: {self.capacidad_peso}, Capacidad de Volumen: {self.capacidad_volumen}, Tipo vehículo: {self.tipo}, Disponibilidad para transportar: {self.disponible})"

    def to_dict(self):
        """Convierte el objeto Vehiculo en un diccionario."""
        return {
            'id': self.id,
            'capacidad_peso': self.capacidad_peso,
            'capacidad_volumen': self.capacidad_volumen,
            'disponibilidad': self.disponible,
            'tipo': self.tipo
            # Incluir otros atributos aquí si es necesario
        }

    def to_list(self):
        """Convierte el objeto Vehiculo en una lista."""
        return [self.id, self.capacidad_peso, self.capacidad_volumen, self.tipo, self.disponible]
        # Incluir otros atributos en la lista si es necesario

def parse_vehiculo_from_string(vehiculo_str: str) -> Vehiculo:
    """Convierte una cadena de texto en formato '[id, capacidad_peso, capacidad_volumen]' a un objeto Vehiculo."""
    id, capacidad_peso, capacidad_volumen, tipo, disponible = eval(vehiculo_str)
    return Vehiculo(id, capacidad_peso, capacidad_volumen, tipo, disponible)

def read_vehiculos_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    vehiculos = [Vehiculo(*vehiculo) for vehiculo in data['vehiculos']]
    
    return vehiculos
