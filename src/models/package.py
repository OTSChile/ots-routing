import json

class Paquete:
    def __init__(self, id: str, peso: float, volumen: float, bultos: int, direccion_destino: str, identificador_adicional: str):
        self.id = id
        self.peso = peso
        self.volumen = volumen
        self.bultos = bultos
        self.direccion_destino = direccion_destino
        self.identificador_adicional = identificador_adicional
        # Puedes añadir más atributos si son necesarios

    def __repr__(self):
        return f"Paquete(ID: {self.id}, Peso: {self.peso}, Volumen: {self.volumen}, Bultos: {self.bultos}, Direccion: {self.direccion_destino}, Identificador: {self.identificador_adicional})"

    def to_dict(self):
        """Convierte el objeto Paquete en un diccionario."""
        return {
            'id': self.id,
            'peso': self.peso,
            'volumen': self.volumen,
            'bultos': self.bultos,
            'direccion_destino': self.direccion_destino,
            'identificador_adicional': self.identificador_adicional
            # Incluir otros atributos aquí si es necesario
        }

    def to_list(self):
        """Convierte el objeto Paquete en una lista."""
        return [self.id, self.peso, self.volumen, self.bultos, self.direccion_destino, self.identificador_adicional]
        # Incluir otros atributos en la lista si es necesario

def parse_paquete_from_string(paquete_str: str) -> Paquete:
    """Convierte una cadena de texto en formato '[id, peso, volumen, bultos, direccion_destino]' a un objeto Paquete."""
    id, peso, volumen, bultos, direccion_destino, identificador_adicional = eval(paquete_str)
    return Paquete(id, peso, volumen, bultos, direccion_destino, identificador_adicional)

def read_paquetes_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    paquetes = [Paquete(*paquete) for paquete in data['paquetes']]
    
    return paquetes
