from django.test import TestCase
from calculators import math_engine

class MathEngineTestCase(TestCase):
    """Unit tests for Algebrify mathematical solver engine."""

    def test_matrix_addition(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        res = math_engine.solve_matrix_addition(A, B)
        self.assertTrue(res['success'])

    def test_matrix_determinant(self):
        A = [[1, 2], [3, 4]]
        res = math_engine.solve_matrix_determinant(A)
        self.assertTrue(res['success'])

    def test_eigenvalues(self):
        A = [[4, 1], [2, 3]]
        res = math_engine.solve_eigenvalues_eigenvectors(A)
        self.assertTrue(res['success'])

    def test_vector_dot_product(self):
        u = [1, 2, 3]
        v = [4, 5, 6]
        res = math_engine.solve_vector_dot_product(u, v)
        self.assertTrue(res['success'])

    def test_system_gaussian(self):
        A = [[1, 2], [3, 4]]
        b = [5, 11]
        res = math_engine.solve_system_gaussian(A, b)
        self.assertTrue(res['success'])
