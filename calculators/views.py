"""
Calculators app views.
Each solver accepts POST data, calls the math engine, and returns the result.
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from . import math_engine


# ───────────────────────────────────────────────
# Helper: parse a JSON-encoded 2-D list safely
# ───────────────────────────────────────────────
def _parse_matrix(raw_str):
    """Parse JSON string → list of lists of float, raise ValueError on failure."""
    data = json.loads(raw_str)
    if not isinstance(data, list):
        raise ValueError("Expected a list.")
    return data


def _parse_vector(raw_str):
    """Parse JSON string → flat list of float."""
    data = json.loads(raw_str)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        # Flatten if nested
        return [item for row in data for item in row]
    return data


# ───────────────────────────────────────────────
# Matrix Calculator
# ───────────────────────────────────────────────
def matrix_calculator(request):
    """
    Matrix Calculator page.
    Supports: add, subtract, multiply, transpose, determinant,
              rank, inverse, adjoint, eigenvalues.
    """
    result_data = None

    if request.method == 'POST':
        operation = request.POST.get('operation', 'add')
        try:
            matrix_a = _parse_matrix(request.POST.get('matrix_a', '[]'))
            matrix_b_raw = request.POST.get('matrix_b', '[]')
            matrix_b = _parse_matrix(matrix_b_raw) if matrix_b_raw.strip() not in ('', '[]', 'null') else []

            SINGLE_MATRIX_OPS = {'transpose', 'determinant', 'rank', 'inverse', 'adjoint', 'eigenvalues'}

            if operation == 'add':
                result_data = math_engine.solve_matrix_addition(matrix_a, matrix_b)
            elif operation == 'subtract':
                result_data = math_engine.solve_matrix_subtraction(matrix_a, matrix_b)
            elif operation == 'multiply':
                result_data = math_engine.solve_matrix_multiplication(matrix_a, matrix_b)
            elif operation == 'transpose':
                result_data = math_engine.solve_matrix_transpose(matrix_a)
            elif operation == 'determinant':
                result_data = math_engine.solve_matrix_determinant(matrix_a)
            elif operation == 'rank':
                result_data = math_engine.solve_matrix_rank(matrix_a)
            elif operation == 'inverse':
                result_data = math_engine.solve_matrix_inverse(matrix_a)
            elif operation == 'adjoint':
                result_data = math_engine.solve_matrix_adjoint(matrix_a)
            elif operation == 'eigenvalues':
                result_data = math_engine.solve_eigenvalues_eigenvectors(matrix_a)
            else:
                result_data = {'success': False, 'error': f'Unknown operation: {operation}'}

        except json.JSONDecodeError:
            result_data = {'success': False, 'error': 'Invalid matrix format. Please enter valid numbers.'}
        except Exception as e:
            result_data = {'success': False, 'error': f'Calculation error: {str(e)}'}

    return render(request, 'calculators/matrix_calculator.html', {'result': result_data})


# ───────────────────────────────────────────────
# Vector Calculator
# ───────────────────────────────────────────────
def vector_calculator(request):
    """
    Vector Calculator page.
    Supports: magnitude, unit, dot, cross, angle, projection.
    """
    result_data = None

    if request.method == 'POST':
        operation = request.POST.get('operation', 'magnitude')
        try:
            vector_u = _parse_vector(request.POST.get('vector_u', '[]'))
            vector_v_raw = request.POST.get('vector_v', '[]')
            vector_v = _parse_vector(vector_v_raw) if vector_v_raw.strip() not in ('', '[]', 'null') else []

            if operation == 'magnitude':
                result_data = math_engine.solve_vector_magnitude(vector_u)
            elif operation == 'unit':
                result_data = math_engine.solve_vector_unit(vector_u)
            elif operation == 'dot':
                result_data = math_engine.solve_vector_dot_product(vector_u, vector_v)
            elif operation == 'cross':
                result_data = math_engine.solve_vector_cross_product(vector_u, vector_v)
            elif operation == 'angle':
                result_data = math_engine.solve_vector_angle(vector_u, vector_v)
            elif operation == 'projection':
                result_data = math_engine.solve_vector_projection(vector_u, vector_v)
            else:
                result_data = {'success': False, 'error': f'Unknown operation: {operation}'}

        except json.JSONDecodeError:
            result_data = {'success': False, 'error': 'Invalid vector format. Please enter valid numbers.'}
        except Exception as e:
            result_data = {'success': False, 'error': f'Calculation error: {str(e)}'}

    return render(request, 'calculators/vector_calculator.html', {'result': result_data})


# ───────────────────────────────────────────────
# Linear System Solver
# ───────────────────────────────────────────────
def system_solver(request):
    """
    Linear System Solver page.
    Supports: gaussian, gauss_jordan, inverse, lu.
    """
    result_data = None

    if request.method == 'POST':
        method = request.POST.get('method', 'gaussian')
        try:
            matrix_a = _parse_matrix(request.POST.get('matrix_a', '[]'))
            vector_b = _parse_vector(request.POST.get('vector_b', '[]'))

            if method == 'gaussian':
                result_data = math_engine.solve_system_gaussian(matrix_a, vector_b)
            elif method == 'gauss_jordan':
                result_data = math_engine.solve_system_gauss_jordan(matrix_a, vector_b)
            elif method == 'inverse':
                result_data = math_engine.solve_system_inverse_method(matrix_a, vector_b)
            elif method == 'lu':
                result_data = math_engine.solve_system_lu_decomposition(matrix_a, vector_b)
            else:
                result_data = {'success': False, 'error': f'Unknown method: {method}'}

        except json.JSONDecodeError:
            result_data = {'success': False, 'error': 'Invalid input format. Please enter valid numbers.'}
        except Exception as e:
            result_data = {'success': False, 'error': f'Solving error: {str(e)}'}

    return render(request, 'calculators/system_solver.html', {'result': result_data})


# ───────────────────────────────────────────────
# 2D Transformation Visualizer
# ───────────────────────────────────────────────
def linear_transformations(request):
    """Interactive 2D Linear Transformation Visualizer."""
    return render(request, 'calculators/transformations.html')
