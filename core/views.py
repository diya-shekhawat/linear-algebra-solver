"""
Core views — serves the landing page of Algebrify Solver Portal.
"""
from django.shortcuts import render


# Key formulas shown on the home page
HOME_FORMULAS = [
    {
        "name": "Matrix Multiplication",
        "formula": r"c_{ij} = \sum_{k=1}^{p} a_{ik} b_{kj}",
        "note": "Row i of A dotted with column j of B."
    },
    {
        "name": "Determinant (2×2)",
        "formula": r"\det\begin{pmatrix}a&b\\c&d\end{pmatrix} = ad - bc",
        "note": "Main diagonal minus anti-diagonal product."
    },
    {
        "name": "Matrix Inverse",
        "formula": r"A^{-1} = \dfrac{1}{\det(A)}\,\text{adj}(A)",
        "note": "Exists only when det(A) ≠ 0."
    },
    {
        "name": "Eigenvalue Equation",
        "formula": r"\det(A - \lambda I) = 0",
        "note": "Solve the characteristic polynomial for λ."
    },
    {
        "name": "Dot Product",
        "formula": r"\vec{u}\cdot\vec{v} = \|\vec{u}\|\|\vec{v}\|\cos\theta",
        "note": "Gives the angle between two vectors."
    },
    {
        "name": "Cross Product Magnitude",
        "formula": r"\|\vec{u}\times\vec{v}\| = \|\vec{u}\|\|\vec{v}\|\sin\theta",
        "note": "Area of parallelogram formed by u and v."
    },
    {
        "name": "Rank-Nullity Theorem",
        "formula": r"\text{rank}(A) + \text{nullity}(A) = n",
        "note": "n = number of columns of A."
    },
    {
        "name": "Vector Projection",
        "formula": r"\text{proj}_{\vec{v}}\vec{u} = \dfrac{\vec{u}\cdot\vec{v}}{\|\vec{v}\|^2}\vec{v}",
        "note": "Component of u in the direction of v."
    },
    {
        "name": "LU Decomposition",
        "formula": r"A = LU,\; Ly = b,\; Ux = y",
        "note": "Factor A, then solve two triangular systems."
    },
]


def home(request):
    """Render the main solver portal landing page."""
    return render(request, 'core/home.html', {'formulas': HOME_FORMULAS})
