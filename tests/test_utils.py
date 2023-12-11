import unittest
from src.models.point import Point
from src.utils.data_loader import read_points_from_file

class TestUtils(unittest.TestCase):
    def test_read_points_from_file(self):
        # Ubicación de un archivo de prueba
        test_file_path = 'path/to/test_input_data.txt'

        # Crear un archivo de prueba con contenido conocido
        with open(test_file_path, 'w') as file:
            file.write('[0, 0]\n')
            file.write('[1, 1]\n')

        # Leer puntos del archivo
        points = read_points_from_file(test_file_path)

        # Comprobar que se leyeron correctamente los puntos
        self.assertEqual(len(points), 2)
        self.assertIsInstance(points[0], Point)
        self.assertEqual(points[0].x, 0)
        self.assertEqual(points[0].y, 0)
        self.assertEqual(points[1].x, 1)
        self.assertEqual(points[1].y, 1)

if __name__ == '__main__':
    unittest.main()
