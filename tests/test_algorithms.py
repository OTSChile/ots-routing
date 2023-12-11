import unittest
from src.models.point import Point
from src.algorithms.exact_solver import held_karp
from src.algorithms.heuristic_solver import simulated_annealing

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        # Ejemplo de puntos para las pruebas
        self.points = [
            Point(0, 0),
            Point(1, 0),
            Point(1, 1),
            Point(0, 1)
        ]

    def test_held_karp(self):
        # Probando el solucionador exacto
        distance, path = held_karp(self.points)
        self.assertIsInstance(distance, float)
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), len(self.points))
        # Se pueden agregar más aserciones según sea necesario

    def test_simulated_annealing(self):
        # Probando el solucionador heurístico
        route, distance = simulated_annealing(self.points, 10000, 0.995, 10000)
        self.assertIsInstance(distance, float)
        self.assertIsInstance(route, list)
        self.assertEqual(len(route), len(self.points))
        # Se pueden agregar más aserciones según sea necesario

if __name__ == '__main__':
    unittest.main()
