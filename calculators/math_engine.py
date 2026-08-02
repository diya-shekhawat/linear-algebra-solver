"""
Algebrify Mathematical Solver Engine
=====================================
Provides step-by-step solutions with:
  - Formulas used
  - Detailed explanations at each step
  - LaTeX-formatted output rendered via MathJax

Solvers:
  1. Matrix Calculator  (Add, Subtract, Multiply, Transpose, Determinant,
                         Rank, Inverse, Adjoint, Eigenvalues, Eigenvectors)
  2. Vector Calculator  (Magnitude, Unit Vector, Dot Product, Cross Product,
                         Angle, Projection)
  3. Linear System Solver (Gaussian Elimination, Gauss-Jordan,
                           Matrix Inverse, LU Decomposition)
"""

import numpy as np
import sympy as sp
from fractions import Fraction

# ─────────────────────────────────────────────
# Helper: pretty-print a matrix/list as LaTeX
# ─────────────────────────────────────────────

def _fmt(v):
    """Format a scalar value for LaTeX display."""
    if isinstance(v, (sp.Basic,)):
        return sp.latex(v)
    try:
        f = Fraction(v).limit_denominator(1000)
        if f.denominator == 1:
            return str(f.numerator)
        return r"\dfrac{" + str(f.numerator) + "}{" + str(f.denominator) + "}"
    except Exception:
        if isinstance(v, float):
            return f"{v:.4g}"
        return str(v)


def mat_latex(M):
    """Convert 2-D list / np.array / sympy Matrix to bmatrix LaTeX."""
    if hasattr(M, 'tolist'):          # numpy
        M = M.tolist()
    elif hasattr(M, '__iter__') and hasattr(M, 'shape'):
        M = list(M)

    if isinstance(M, sp.Matrix):
        rows = []
        for i in range(M.rows):
            rows.append(" & ".join([sp.latex(M[i, j]) for j in range(M.cols)]))
        return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"

    rows = []
    for row in M:
        if hasattr(row, '__iter__') and not isinstance(row, str):
            rows.append(" & ".join([_fmt(v) for v in row]))
        else:
            rows.append(_fmt(row))
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def vec_latex(v):
    """Convert 1-D list / array to column bmatrix LaTeX."""
    if hasattr(v, 'tolist'):
        v = v.tolist()
    items = [_fmt(x) for x in v]
    return r"\begin{bmatrix}" + r" \\ ".join(items) + r"\end{bmatrix}"


def _step(title, formula, latex_expr, explanation):
    """Create a solution step dictionary."""
    return {
        "title":       title,
        "formula":     formula,
        "latex":       latex_expr,
        "explanation": explanation,
    }


# ═══════════════════════════════════════════════
# 1. MATRIX CALCULATOR
# ═══════════════════════════════════════════════

def solve_matrix_addition(A, B):
    """
    Matrix Addition: C = A + B
    Formula: c_{ij} = a_{ij} + b_{ij}
    """
    steps = []
    try:
        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float)
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix values: {e}"}

    steps.append(_step(
        "Given Matrices",
        r"A \text{ and } B",
        rf"A = {mat_latex(A)}, \quad B = {mat_latex(B)}",
        "We are given two matrices. For addition, both matrices must have the same dimensions (same number of rows and columns)."
    ))

    if A.shape != B.shape:
        return {"success": False, "error":
                f"Matrix A is {A.shape[0]}×{A.shape[1]} but Matrix B is {B.shape[0]}×{B.shape[1]}. "
                "Both matrices must have identical dimensions for addition."}

    m, n = A.shape
    steps.append(_step(
        "Dimension Check",
        r"A_{m \times n} + B_{m \times n} = C_{m \times n}",
        rf"\text{{Both matrices are }} {m} \times {n}. \text{{ Result will be }} {m} \times {n}.",
        "Matrix addition is defined only when both matrices have the same order (m × n)."
    ))

    # Element-wise display
    rows_latex = []
    for i in range(m):
        cells = []
        for j in range(n):
            cells.append(rf"({_fmt(A[i,j])}) + ({_fmt(B[i,j])})")
        rows_latex.append(" & ".join(cells))
    element_latex = r"\begin{bmatrix}" + r" \\ ".join(rows_latex) + r"\end{bmatrix}"

    steps.append(_step(
        "Element-Wise Addition",
        r"c_{ij} = a_{ij} + b_{ij}",
        rf"C = {element_latex}",
        "Add each corresponding element: the entry in row i, column j of C equals the sum of the entries at position (i, j) in A and B."
    ))

    C = A + B
    steps.append(_step(
        "Final Result",
        r"C = A + B",
        rf"C = {mat_latex(C)}",
        "This is the resulting sum matrix C = A + B."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(C)}


# ─────────────────────────────────────────────

def solve_matrix_subtraction(A, B):
    """Matrix Subtraction: C = A - B"""
    steps = []
    try:
        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float)
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix values: {e}"}

    steps.append(_step(
        "Given Matrices",
        r"A \text{ and } B",
        rf"A = {mat_latex(A)}, \quad B = {mat_latex(B)}",
        "For subtraction, both matrices must have identical dimensions."
    ))

    if A.shape != B.shape:
        return {"success": False, "error":
                f"Dimension mismatch: A is {A.shape[0]}×{A.shape[1]}, B is {B.shape[0]}×{B.shape[1]}."}

    m, n = A.shape
    rows_latex = []
    for i in range(m):
        cells = [rf"({_fmt(A[i,j])}) - ({_fmt(B[i,j])})" for j in range(n)]
        rows_latex.append(" & ".join(cells))
    elem_latex = r"\begin{bmatrix}" + r" \\ ".join(rows_latex) + r"\end{bmatrix}"

    steps.append(_step(
        "Element-Wise Subtraction",
        r"c_{ij} = a_{ij} - b_{ij}",
        rf"C = {elem_latex}",
        "Subtract each corresponding element. Like addition, subtraction is commutative for individual elements but A − B ≠ B − A for matrices in general."
    ))

    C = A - B
    steps.append(_step(
        "Final Result",
        r"C = A - B",
        rf"C = {mat_latex(C)}",
        "The resulting difference matrix C."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(C)}


# ─────────────────────────────────────────────

def solve_matrix_multiplication(A, B):
    """
    Matrix Multiplication: C = A × B
    Formula: c_{ij} = Σ a_{ik} · b_{kj}
    """
    steps = []
    try:
        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float)
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix values: {e}"}

    steps.append(_step(
        "Given Matrices",
        r"A_{m \times p} \text{ and } B_{p \times n}",
        rf"A = {mat_latex(A)} \;({A.shape[0]}\times{A.shape[1]}), \quad B = {mat_latex(B)} \;({B.shape[0]}\times{B.shape[1]})",
        f"For matrix multiplication A × B, the number of columns in A ({A.shape[1]}) must equal the number of rows in B ({B.shape[0]})."
    ))

    if A.shape[1] != B.shape[0]:
        return {"success": False, "error":
                f"Cannot multiply: A has {A.shape[1]} columns but B has {B.shape[0]} rows. "
                "The inner dimensions must match."}

    m, p = A.shape
    _, n = B.shape

    steps.append(_step(
        "Multiplication Rule",
        r"c_{ij} = \sum_{k=1}^{p} a_{ik} \cdot b_{kj}",
        rf"\text{{Result dimension: }} {m} \times {p} \;\cdot\; {p} \times {n} = {m} \times {n}",
        "Each entry c_{ij} is the dot product of row i of A with column j of B."
    ))

    C = np.dot(A, B)

    # Show calculation for each entry (limit display for large matrices)
    if m * n <= 16:
        entry_lines = []
        for i in range(m):
            for j in range(n):
                terms = " + ".join([rf"({_fmt(A[i,k])})({_fmt(B[k,j])})" for k in range(p)])
                entry_lines.append(rf"c_{{{i+1}{j+1}}} = {terms} = {_fmt(C[i,j])}")
        steps.append(_step(
            "Dot-Product Calculations",
            r"c_{ij} = \sum_{k=1}^{p} a_{ik} b_{kj}",
            r"\\ ".join(entry_lines),
            "Each entry is computed as a row-by-column dot product."
        ))

    steps.append(_step(
        "Final Product Matrix",
        r"C = A \times B",
        rf"C = {mat_latex(C)}",
        "Note: Matrix multiplication is NOT commutative (A×B ≠ B×A in general), but it IS associative: (AB)C = A(BC)."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(C)}


# ─────────────────────────────────────────────

def solve_matrix_transpose(A):
    """
    Transpose: A^T
    Formula: (A^T)_{ij} = A_{ji}
    """
    steps = []
    try:
        A = np.array(A, dtype=float)
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix values: {e}"}

    m, n = A.shape
    steps.append(_step(
        "Original Matrix A",
        r"A \in \mathbb{R}^{m \times n}",
        rf"A = {mat_latex(A)} \quad ({m} \times {n})",
        f"The matrix A has {m} rows and {n} columns. Its transpose A^T will have {n} rows and {m} columns."
    ))

    steps.append(_step(
        "Transpose Formula",
        r"(A^T)_{ij} = A_{ji}",
        r"(A^T)_{ij} = A_{ji} \quad \text{(rows become columns, columns become rows)}",
        "To transpose a matrix, reflect it over its main diagonal: the entry in row i, column j moves to row j, column i."
    ))

    AT = A.T
    steps.append(_step(
        "Properties of Transpose",
        r"(A^T)^T = A, \quad (AB)^T = B^T A^T, \quad (A+B)^T = A^T + B^T",
        rf"A^T = {mat_latex(AT)} \quad ({n} \times {m})",
        "Key property: (A^T)^T = A. For products: (AB)^T = B^T A^T (order reverses)."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(AT)}


# ─────────────────────────────────────────────

def solve_matrix_determinant(A):
    """
    Determinant: det(A)
    Uses cofactor expansion and sympy for exact values.
    """
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix values: {e}"}

    if A_sp.rows != A_sp.cols:
        return {"success": False, "error":
                f"Determinant is only defined for square matrices. Got {A_sp.rows}×{A_sp.cols}."}

    n = A_sp.rows
    steps.append(_step(
        "Square Matrix Check",
        r"\det(A) \text{ is defined only for } n \times n \text{ matrices}",
        rf"A = {mat_latex(A_sp)} \quad ({n} \times {n})",
        f"The determinant is a scalar value computed from a square matrix. Geometrically, |det(A)| represents the scaling factor of the linear transformation."
    ))

    det_val = A_sp.det()

    if n == 1:
        steps.append(_step(
            "1×1 Determinant",
            r"\det([a]) = a",
            rf"\det(A) = {sp.latex(det_val)}",
            "The determinant of a 1×1 matrix is simply the single element."
        ))

    elif n == 2:
        a, b = A_sp[0, 0], A_sp[0, 1]
        c, d = A_sp[1, 0], A_sp[1, 1]
        steps.append(_step(
            "2×2 Determinant Formula",
            r"\det\begin{pmatrix}a & b \\ c & d\end{pmatrix} = ad - bc",
            rf"\det(A) = ({sp.latex(a)})({sp.latex(d)}) - ({sp.latex(b)})({sp.latex(c)}) = {sp.latex(a*d)} - ({sp.latex(b*c)}) = {sp.latex(det_val)}",
            "For a 2×2 matrix: subtract the product of the anti-diagonal from the product of the main diagonal."
        ))

    elif n == 3:
        steps.append(_step(
            "3×3 Cofactor Expansion (Row 1)",
            r"\det(A) = a_{11}C_{11} + a_{12}C_{12} + a_{13}C_{13}",
            rf"\det(A) = {sp.latex(A_sp[0,0])} \cdot M_{{11}} - {sp.latex(A_sp[0,1])} \cdot M_{{12}} + {sp.latex(A_sp[0,2])} \cdot M_{{13}}",
            "Expand along the first row. C_{ij} = (-1)^{i+j} M_{ij} where M_{ij} is the minor (determinant of submatrix formed by deleting row i and column j)."
        ))
        # Show each minor
        for j in range(3):
            minor = A_sp.minor_submatrix(0, j)
            minor_det = minor.det()
            sign = "+" if j % 2 == 0 else "-"
            steps.append(_step(
                f"Minor M_{{1{j+1}}} (delete row 1, col {j+1})",
                rf"M_{{1{j+1}}} = \det(\text{{submatrix}})",
                rf"M_{{1{j+1}}} = \det{mat_latex(minor)} = {sp.latex(minor_det)}",
                f"Remove row 1 and column {j+1} to get the 2×2 minor."
            ))
        steps.append(_step(
            "Evaluated Determinant",
            r"\det(A) = \sum_j (-1)^{1+j} a_{1j} M_{1j}",
            rf"\det(A) = {sp.latex(det_val)}",
            "Sum the signed products of pivot elements and their minors."
        ))

    else:
        steps.append(_step(
            f"{n}×{n} Determinant via LU/Row-Echelon",
            r"\det(A) = (-1)^s \cdot \prod_i u_{ii} \text{ where } U \text{ is upper triangular}",
            rf"\det(A) = {sp.latex(det_val)}",
            "For larger matrices the determinant is computed via Gaussian elimination. det(A) = product of pivot elements × (−1)^(number of row swaps)."
        ))

    # Geometric interpretation
    steps.append(_step(
        "Geometric Interpretation",
        r"|\det(A)| = \text{scaling factor of the linear transformation}",
        rf"\det(A) = {sp.latex(det_val)}" +
        (r" \quad \Rightarrow \text{Matrix is invertible (non-singular)}" if det_val != 0
         else r" \quad \Rightarrow \text{Matrix is singular (NOT invertible)}"),
        f"det(A) = 0 means the columns are linearly dependent (the transformation collapses space). "
        f"det(A) ≠ 0 means the matrix is invertible. Here det(A) = {sp.latex(det_val)}."
    ))

    return {"success": True, "steps": steps, "result_latex": rf"\det(A) = {sp.latex(det_val)}"}


# ─────────────────────────────────────────────

def solve_matrix_rank(A):
    """Rank via RREF."""
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix: {e}"}

    m, n = A_sp.shape
    steps.append(_step(
        "Original Matrix",
        r"\text{rank}(A) = \text{number of pivot positions in RREF}",
        rf"A = {mat_latex(A_sp)} \quad ({m} \times {n})",
        "The rank of a matrix is the dimension of its column space (= row space). It equals the number of non-zero rows in RREF."
    ))

    rref, pivots = A_sp.rref()
    rank = len(pivots)

    steps.append(_step(
        "Reduced Row Echelon Form (RREF)",
        r"\text{RREF}(A) \xrightarrow{\text{EROs}} \text{pivot positions identified}",
        rf"\text{{RREF}}(A) = {mat_latex(rref)}",
        f"Elementary Row Operations (EROs) reduce A to RREF. Pivot columns (1-indexed): {[p+1 for p in pivots]}."
    ))

    nullity = n - rank
    steps.append(_step(
        "Rank-Nullity Theorem",
        r"\text{rank}(A) + \text{nullity}(A) = n \text{ (number of columns)}",
        rf"\text{{rank}}(A) = {rank}, \quad \text{{nullity}}(A) = {n} - {rank} = {nullity}",
        f"rank = {rank} (pivot rows), nullity = {nullity} (free variables / dimension of null space)."
    ))

    return {"success": True, "steps": steps, "result_latex": rf"\text{{rank}}(A) = {rank}"}


# ─────────────────────────────────────────────

def solve_matrix_inverse(A):
    """
    Matrix Inverse: A^{-1}
    Formula: A^{-1} = (1/det(A)) * adj(A)
    """
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix: {e}"}

    if A_sp.rows != A_sp.cols:
        return {"success": False, "error": "Inverse requires a square (n×n) matrix."}

    n = A_sp.rows
    steps.append(_step(
        "Inverse Existence Condition",
        r"A^{-1} \text{ exists} \iff \det(A) \neq 0",
        rf"A = {mat_latex(A_sp)} \quad ({n} \times {n})",
        "A square matrix is invertible (non-singular) if and only if its determinant is non-zero."
    ))

    det = A_sp.det()
    steps.append(_step(
        "Compute Determinant",
        r"\det(A) \neq 0 \Rightarrow \text{invertible}",
        rf"\det(A) = {sp.latex(det)}",
        f"Since det(A) = {sp.latex(det)}, the matrix is {'invertible' if det != 0 else 'singular (NOT invertible)'}."
    ))

    if det == 0:
        return {"success": False, "error":
                f"Matrix is singular: det(A) = 0. The inverse does not exist. "
                "This means the matrix has linearly dependent rows/columns."}

    adj = A_sp.adjugate()
    steps.append(_step(
        "Adjugate (Classical Adjoint)",
        r"\text{adj}(A) = C^T \text{ where } C_{ij} = (-1)^{i+j} M_{ij}",
        rf"\text{{adj}}(A) = {mat_latex(adj)}",
        "The adjugate is the transpose of the cofactor matrix. Each cofactor C_{ij} = (−1)^{i+j} × (minor M_{ij})."
    ))

    steps.append(_step(
        "Inverse Formula",
        r"A^{-1} = \dfrac{1}{\det(A)} \cdot \text{adj}(A)",
        rf"A^{{-1}} = \dfrac{{1}}{{{sp.latex(det)}}} \cdot {mat_latex(adj)}",
        "Divide every element of the adjugate by the determinant."
    ))

    inv = A_sp.inv()
    steps.append(_step(
        "Final Inverse Matrix",
        r"A \cdot A^{-1} = A^{-1} \cdot A = I",
        rf"A^{{-1}} = {mat_latex(inv)}",
        "Verification: multiplying A by its inverse should yield the identity matrix I."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(inv)}


# ─────────────────────────────────────────────

def solve_matrix_adjoint(A):
    """Adjugate/Classical Adjoint."""
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix: {e}"}

    if A_sp.rows != A_sp.cols:
        return {"success": False, "error": "Adjoint requires a square matrix."}

    n = A_sp.rows
    steps.append(_step(
        "Adjugate Definition",
        r"\text{adj}(A) = C^T",
        rf"A = {mat_latex(A_sp)} \quad ({n} \times {n})",
        "The adjugate (also called classical adjoint) of a matrix A is the transpose of its cofactor matrix."
    ))

    C = A_sp.cofactor_matrix()
    steps.append(_step(
        "Cofactor Matrix C",
        r"C_{ij} = (-1)^{i+j} M_{ij}",
        rf"C = {mat_latex(C)}",
        "Each cofactor C_{ij} = (−1)^{i+j} times the minor M_{ij}, where M_{ij} is the determinant of the submatrix obtained by deleting row i and column j."
    ))

    adj = A_sp.adjugate()
    steps.append(_step(
        "Adjugate = Transpose of Cofactor Matrix",
        r"\text{adj}(A) = C^T",
        rf"\text{{adj}}(A) = C^T = {mat_latex(adj)}",
        "Transpose the cofactor matrix by reflecting across the main diagonal."
    ))

    det = A_sp.det()
    steps.append(_step(
        "Verification Identity",
        r"A \cdot \text{adj}(A) = \det(A) \cdot I",
        rf"A \cdot \text{{adj}}(A) = {sp.latex(det)} \cdot I",
        "This identity always holds. If det(A) ≠ 0, we can derive A^{-1} = adj(A) / det(A)."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(adj)}


# ─────────────────────────────────────────────

def solve_eigenvalues_eigenvectors(A):
    """
    Eigenvalues & Eigenvectors.
    Formula: det(A - λI) = 0, then (A - λI)v = 0
    """
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
    except Exception as e:
        return {"success": False, "error": f"Invalid matrix: {e}"}

    if A_sp.rows != A_sp.cols:
        return {"success": False, "error": "Eigenvalues require a square matrix."}

    n = A_sp.rows
    lam = sp.Symbol(r'\lambda')

    steps.append(_step(
        "Eigenvalue Equation",
        r"Av = \lambda v \iff (A - \lambda I)v = 0",
        rf"A = {mat_latex(A_sp)} \quad ({n} \times {n})",
        "An eigenvector v is a non-zero vector such that the transformation A only scales it (not rotates). λ is the scaling factor (eigenvalue)."
    ))

    AlamI = A_sp - lam * sp.eye(n)
    steps.append(_step(
        "Form A − λI",
        r"A - \lambda I",
        rf"A - \lambda I = {mat_latex(AlamI)}",
        "Subtract λ from each main-diagonal entry. We need det(A − λI) = 0 for non-trivial eigenvectors."
    ))

    char_poly = A_sp.charpoly(lam)
    char_expr = char_poly.as_expr()
    steps.append(_step(
        "Characteristic Polynomial",
        r"\det(A - \lambda I) = 0",
        rf"\det(A - \lambda I) = {sp.latex(char_expr)} = 0",
        "Expand the determinant to get the characteristic polynomial. Its roots are the eigenvalues."
    ))

    eig_data = A_sp.eigenvects()

    eig_lines = []
    for val, mult, vects in eig_data:
        v_strs = ", ".join([mat_latex(v) for v in vects])
        eig_lines.append(
            rf"\lambda = {sp.latex(val)} \;(\text{{multiplicity }} {mult}): \quad v = {v_strs}"
        )

    steps.append(_step(
        "Eigenvalues & Eigenvectors",
        r"(A - \lambda I)v = 0 \Rightarrow v \neq 0",
        r" \\ ".join(eig_lines),
        "For each eigenvalue λ, solve the homogeneous system (A − λI)v = 0 to find the eigenvectors (nullspace of A − λI)."
    ))

    # Diagonalizability check
    total_vects = sum(len(vs) for _, _, vs in eig_data)
    diag_note = (
        rf"A \text{{ is diagonalizable: }} A = PDP^{{-1}}" if total_vects == n
        else rf"A \text{{ is NOT diagonalizable (insufficient independent eigenvectors)}}"
    )
    steps.append(_step(
        "Diagonalizability",
        r"A = PDP^{-1} \text{ where } D = \text{diag}(\lambda_1, \ldots, \lambda_n)",
        diag_note,
        f"A matrix is diagonalizable iff it has n linearly independent eigenvectors. "
        f"Here we found {total_vects} independent eigenvector(s) for an {n}×{n} matrix."
    ))

    return {"success": True, "steps": steps, "result_latex": r" \\ ".join(eig_lines)}


# ═══════════════════════════════════════════════
# 2. VECTOR CALCULATOR
# ═══════════════════════════════════════════════

def solve_vector_magnitude(v):
    """||v|| = sqrt(v1^2 + v2^2 + ...)"""
    steps = []
    try:
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector: {e}"}

    if not v:
        return {"success": False, "error": "Vector cannot be empty."}

    steps.append(_step(
        "Given Vector",
        r"\vec{v} \in \mathbb{R}^n",
        rf"\vec{{v}} = {vec_latex(v)}",
        f"A vector in ℝ^{len(v)}. The magnitude (Euclidean norm) measures the length of the vector."
    ))

    sq_terms = " + ".join([rf"({_fmt(x)})^2" for x in v])
    sq_sum = sum(x**2 for x in v)
    mag = np.sqrt(sq_sum)

    steps.append(_step(
        "Euclidean Norm Formula",
        r"\|\vec{v}\| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}",
        rf"\|\vec{{v}}\| = \sqrt{{{sq_terms}}} = \sqrt{{{_fmt(sq_sum)}}} = {_fmt(mag)}",
        "Square each component, sum them, then take the square root. This is the Euclidean (L²) norm."
    ))

    return {"success": True, "steps": steps, "result_latex": rf"\|\vec{{v}}\| = {_fmt(mag)}"}


# ─────────────────────────────────────────────

def solve_vector_unit(v):
    """Unit vector: v̂ = v / ||v||"""
    steps = []
    try:
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector: {e}"}

    mag = np.linalg.norm(v)
    if mag == 0:
        return {"success": False, "error": "The zero vector has no unit vector (undefined direction)."}

    steps.append(_step(
        "Given Vector & Magnitude",
        r"\hat{v} = \dfrac{\vec{v}}{\|\vec{v}\|}",
        rf"\vec{{v}} = {vec_latex(v)}, \quad \|\vec{{v}}\| = {_fmt(mag)}",
        "The unit vector has the same direction as v but has magnitude 1. It is found by dividing each component by the magnitude."
    ))

    unit_v = [x / mag for x in v]
    comp_show = rf"\dfrac{{1}}{{{_fmt(mag)}}} {vec_latex(v)} = {vec_latex(unit_v)}"

    steps.append(_step(
        "Normalize Each Component",
        r"\hat{v}_i = \dfrac{v_i}{\|\vec{v}\|}",
        comp_show,
        "Divide every component by the magnitude."
    ))

    steps.append(_step(
        "Verification",
        r"\|\hat{v}\| = 1",
        rf"\|\hat{{v}}\| = \sqrt{{" + " + ".join([rf"({_fmt(x)})^2" for x in unit_v]) + rf"}} \approx 1",
        "A unit vector always has magnitude 1 — you can verify by computing its norm."
    ))

    return {"success": True, "steps": steps, "result_latex": vec_latex(unit_v)}


# ─────────────────────────────────────────────

def solve_vector_dot_product(u, v):
    """Dot product: u·v = Σ u_i v_i"""
    steps = []
    try:
        u = [float(x) for x in u]
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector values: {e}"}

    if len(u) != len(v):
        return {"success": False, "error":
                f"Vectors must have the same dimension. u has {len(u)} components, v has {len(v)}."}

    steps.append(_step(
        "Given Vectors",
        r"\vec{u}, \vec{v} \in \mathbb{R}^n",
        rf"\vec{{u}} = {vec_latex(u)}, \quad \vec{{v}} = {vec_latex(v)}",
        "The dot product (scalar product) takes two vectors and returns a scalar."
    ))

    terms = " + ".join([rf"({_fmt(u[i])} \cdot {_fmt(v[i])})" for i in range(len(u))])
    dot = np.dot(u, v)

    steps.append(_step(
        "Dot Product Formula",
        r"\vec{u} \cdot \vec{v} = \sum_{i=1}^{n} u_i v_i = u_1 v_1 + u_2 v_2 + \cdots",
        rf"\vec{{u}} \cdot \vec{{v}} = {terms} = {_fmt(dot)}",
        "Multiply corresponding components and sum the results."
    ))

    mag_u = np.linalg.norm(u)
    mag_v = np.linalg.norm(v)
    if mag_u > 0 and mag_v > 0:
        cos_theta = np.clip(dot / (mag_u * mag_v), -1, 1)
        theta = np.degrees(np.arccos(cos_theta))
        steps.append(_step(
            "Geometric Interpretation",
            r"\vec{u} \cdot \vec{v} = \|\vec{u}\| \|\vec{v}\| \cos\theta",
            rf"\cos\theta = \dfrac{{{_fmt(dot)}}}{{{_fmt(mag_u)} \cdot {_fmt(mag_v)}}} = {_fmt(cos_theta)} \quad \Rightarrow \quad \theta \approx {theta:.2f}^\circ",
            "The dot product equals the product of magnitudes times cosine of the angle between vectors. "
            "If dot product = 0, the vectors are orthogonal (perpendicular)."
        ))

    return {"success": True, "steps": steps, "result_latex": rf"\vec{{u}} \cdot \vec{{v}} = {_fmt(dot)}"}


# ─────────────────────────────────────────────

def solve_vector_cross_product(u, v):
    """Cross product: u × v (3D only)"""
    steps = []
    try:
        u = [float(x) for x in u]
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector values: {e}"}

    if len(u) != 3 or len(v) != 3:
        return {"success": False, "error":
                "Cross product is only defined for 3D vectors (ℝ³). "
                "Please enter exactly 3 components for each vector."}

    steps.append(_step(
        "3D Vectors",
        r"\vec{u} \times \vec{v} \in \mathbb{R}^3",
        rf"\vec{{u}} = {vec_latex(u)}, \quad \vec{{v}} = {vec_latex(v)}",
        "The cross product of two 3D vectors produces a new vector perpendicular to both."
    ))

    steps.append(_step(
        "Determinant Form",
        r"\vec{u} \times \vec{v} = \begin{vmatrix}\hat{i} & \hat{j} & \hat{k}\\ u_1 & u_2 & u_3\\ v_1 & v_2 & v_3\end{vmatrix}",
        rf"\vec{{u}} \times \vec{{v}} = \begin{{vmatrix}}\hat{{i}} & \hat{{j}} & \hat{{k}} \\ {_fmt(u[0])} & {_fmt(u[1])} & {_fmt(u[2])} \\ {_fmt(v[0])} & {_fmt(v[1])} & {_fmt(v[2])}\end{{vmatrix}}",
        "Expand along the first row using cofactors."
    ))

    i_comp = u[1]*v[2] - u[2]*v[1]
    j_comp = u[2]*v[0] - u[0]*v[2]
    k_comp = u[0]*v[1] - u[1]*v[0]

    steps.append(_step(
        "Component Expansion",
        r"\vec{u} \times \vec{v} = (u_2 v_3 - u_3 v_2)\hat{i} - (u_1 v_3 - u_3 v_1)\hat{j} + (u_1 v_2 - u_2 v_1)\hat{k}",
        rf"\hat{{i}}: ({_fmt(u[1])} \cdot {_fmt(v[2])} - {_fmt(u[2])} \cdot {_fmt(v[1])}) = {_fmt(i_comp)} \\"
        rf"\hat{{j}}: -({_fmt(u[0])} \cdot {_fmt(v[2])} - {_fmt(u[2])} \cdot {_fmt(v[0])}) = {_fmt(j_comp)} \\"
        rf"\hat{{k}}: ({_fmt(u[0])} \cdot {_fmt(v[1])} - {_fmt(u[1])} \cdot {_fmt(v[0])}) = {_fmt(k_comp)}",
        "Compute each component using 2×2 determinants (minors)."
    ))

    cp = [i_comp, j_comp, k_comp]
    mag_cp = np.linalg.norm(cp)
    steps.append(_step(
        "Result & Geometric Meaning",
        r"\|\vec{u} \times \vec{v}\| = \|\vec{u}\|\|\vec{v}\|\sin\theta",
        rf"\vec{{u}} \times \vec{{v}} = {vec_latex(cp)}, \quad \|\vec{{u}} \times \vec{{v}}\| = {_fmt(mag_cp)}",
        "The result is perpendicular to both u and v. Its magnitude equals the area of the parallelogram formed by u and v."
    ))

    return {"success": True, "steps": steps, "result_latex": vec_latex(cp)}


# ─────────────────────────────────────────────

def solve_vector_angle(u, v):
    """Angle between vectors using dot product formula."""
    steps = []
    try:
        u = [float(x) for x in u]
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector values: {e}"}

    if len(u) != len(v):
        return {"success": False, "error": "Vectors must have the same dimension."}

    mag_u = np.linalg.norm(u)
    mag_v = np.linalg.norm(v)

    if mag_u == 0 or mag_v == 0:
        return {"success": False, "error": "Cannot compute angle: one or both vectors are zero vectors."}

    steps.append(_step(
        "Angle Formula",
        r"\cos\theta = \dfrac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \cdot \|\vec{v}\|}",
        rf"\vec{{u}} = {vec_latex(u)}, \quad \vec{{v}} = {vec_latex(v)}",
        "The angle θ between two non-zero vectors is found via the dot product identity."
    ))

    dot = float(np.dot(u, v))
    steps.append(_step(
        "Dot Product",
        r"\vec{u} \cdot \vec{v} = \sum u_i v_i",
        rf"\vec{{u}} \cdot \vec{{v}} = " + " + ".join([rf"({_fmt(u[i])} \cdot {_fmt(v[i])})" for i in range(len(u))]) + rf" = {_fmt(dot)}",
        "Compute the dot product as the sum of element-wise products."
    ))

    steps.append(_step(
        "Magnitudes",
        r"\|\vec{u}\| = \sqrt{\sum u_i^2}, \quad \|\vec{v}\| = \sqrt{\sum v_i^2}",
        rf"\|\vec{{u}}\| = {_fmt(mag_u)}, \quad \|\vec{{v}}\| = {_fmt(mag_v)}",
        "Compute the Euclidean norms (lengths) of both vectors."
    ))

    cos_theta = np.clip(dot / (mag_u * mag_v), -1.0, 1.0)
    theta_rad = float(np.arccos(cos_theta))
    theta_deg = float(np.degrees(theta_rad))

    steps.append(_step(
        "Compute Angle",
        r"\theta = \arccos\!\left(\dfrac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}\right)",
        rf"\cos\theta = \dfrac{{{_fmt(dot)}}}{{{_fmt(mag_u)} \times {_fmt(mag_v)}}} = {_fmt(cos_theta)} \quad \Rightarrow \quad \theta = {theta_deg:.4f}^\circ = {theta_rad:.4f} \text{{ rad}}",
        f"θ = {theta_deg:.2f}°. Special cases: θ = 0° (parallel), θ = 90° (orthogonal), θ = 180° (anti-parallel)."
    ))

    return {"success": True, "steps": steps,
            "result_latex": rf"\theta = {theta_deg:.4f}^\circ \approx {theta_rad:.4f} \text{{ rad}}"}


# ─────────────────────────────────────────────

def solve_vector_projection(u, v):
    """Projection of u onto v."""
    steps = []
    try:
        u = [float(x) for x in u]
        v = [float(x) for x in v]
    except Exception as e:
        return {"success": False, "error": f"Invalid vector values: {e}"}

    if len(u) != len(v):
        return {"success": False, "error": "Vectors must have the same dimension."}

    v_sq = sum(x**2 for x in v)
    if v_sq == 0:
        return {"success": False, "error": "Cannot project onto the zero vector."}

    steps.append(_step(
        "Projection Formula",
        r"\text{proj}_{\vec{v}} \vec{u} = \dfrac{\vec{u} \cdot \vec{v}}{\|\vec{v}\|^2} \vec{v}",
        rf"\vec{{u}} = {vec_latex(u)}, \quad \vec{{v}} = {vec_latex(v)}",
        "The vector projection of u onto v gives the component of u in the direction of v."
    ))

    dot = float(np.dot(u, v))
    steps.append(_step(
        "Compute Scalar Factor",
        r"\text{scalar} = \dfrac{\vec{u} \cdot \vec{v}}{\|\vec{v}\|^2}",
        rf"\dfrac{{\vec{{u}} \cdot \vec{{v}}}}{{\|\vec{{v}}\|^2}} = \dfrac{{{_fmt(dot)}}}{{{_fmt(v_sq)}}} = {_fmt(dot/v_sq)}",
        "This scalar factor represents how much of u lies in the direction of v."
    ))

    proj = [dot / v_sq * vi for vi in v]
    steps.append(_step(
        "Vector Projection",
        r"\text{proj}_{\vec{v}} \vec{u} = \text{scalar} \cdot \vec{v}",
        rf"\text{{proj}}_{{\vec{{v}}}} \vec{{u}} = {_fmt(dot/v_sq)} \cdot {vec_latex(v)} = {vec_latex(proj)}",
        "Multiply v by the scalar factor to get the projection vector."
    ))

    # Scalar projection
    scalar_proj = dot / np.sqrt(v_sq)
    steps.append(_step(
        "Scalar Projection (Length Along v̂)",
        r"\text{comp}_{\vec{v}} \vec{u} = \dfrac{\vec{u} \cdot \vec{v}}{\|\vec{v}\|}",
        rf"\text{{comp}}_{{\vec{{v}}}} \vec{{u}} = \dfrac{{{_fmt(dot)}}}{{{_fmt(np.sqrt(v_sq))}}} = {_fmt(scalar_proj)}",
        "The scalar projection gives the signed length of u in the direction of v."
    ))

    return {"success": True, "steps": steps, "result_latex": vec_latex(proj)}


# ═══════════════════════════════════════════════
# 3. LINEAR SYSTEM SOLVERS
# ═══════════════════════════════════════════════

def _augmented_latex(Aug):
    """Render augmented matrix [A|b] with a dividing line."""
    rows = []
    n_cols = len(Aug[0])
    for row in Aug:
        left = " & ".join([_fmt(v) for v in row[:-1]])
        right = _fmt(row[-1])
        rows.append(left + " & " + right)
    n_var = n_cols - 1
    col_spec = "c" * n_var + "|c"
    return (r"\left[\begin{array}{" + col_spec + "}" +
            r" \\ ".join(rows) +
            r"\end{array}\right]")


def solve_system_gaussian(A, b):
    """
    Gaussian Elimination (REF + back-substitution)
    Shows every row operation.
    """
    steps = []
    try:
        A = [[float(x) for x in row] for row in A]
        b = [float(x) for x in b]
    except Exception as e:
        return {"success": False, "error": f"Invalid input: {e}"}

    n = len(b)
    if any(len(row) != n for row in A):
        return {"success": False, "error": "Coefficient matrix A must be n×n for an n-variable system."}

    Aug = [A[i][:] + [b[i]] for i in range(n)]

    steps.append(_step(
        "System Setup — Augmented Matrix [A|b]",
        r"[A \mid b]",
        _augmented_latex(Aug),
        f"We represent the {n}×{n} linear system Ax = b as an augmented matrix [A|b] and apply Elementary Row Operations (EROs)."
    ))

    steps.append(_step(
        "ERO Reference",
        r"R_i \leftrightarrow R_j \quad kR_i \quad R_i + kR_j",
        r"\text{Allowed EROs: (1) Swap rows } R_i \leftrightarrow R_j \text{, (2) Scale } R_i \leftarrow k R_i \text{, (3) Replace } R_i \leftarrow R_i + k R_j",
        "These three operations preserve the solution set of the system."
    ))

    # Forward elimination
    pivot_row = 0
    for col in range(n):
        # Find pivot
        max_row = pivot_row
        for r in range(pivot_row + 1, n):
            if abs(Aug[r][col]) > abs(Aug[max_row][col]):
                max_row = r

        if abs(Aug[max_row][col]) < 1e-12:
            continue

        if max_row != pivot_row:
            Aug[pivot_row], Aug[max_row] = Aug[max_row], Aug[pivot_row]
            steps.append(_step(
                f"Row Swap: R{pivot_row+1} ↔ R{max_row+1}",
                rf"R_{pivot_row+1} \leftrightarrow R_{max_row+1}",
                _augmented_latex(Aug),
                "Swap to place the largest absolute-value entry in the pivot position (partial pivoting for numerical stability)."
            ))

        for r in range(pivot_row + 1, n):
            if abs(Aug[r][col]) < 1e-12:
                continue
            factor = Aug[r][col] / Aug[pivot_row][col]
            for c in range(n + 1):
                Aug[r][c] -= factor * Aug[pivot_row][c]
            f_str = _fmt(factor)
            steps.append(_step(
                f"Eliminate below pivot in column {col+1}: R{r+1} ← R{r+1} − ({f_str})·R{pivot_row+1}",
                rf"R_{{{r+1}}} \leftarrow R_{{{r+1}}} - ({f_str}) \cdot R_{{{pivot_row+1}}}",
                _augmented_latex(Aug),
                f"Multiply R{pivot_row+1} by {f_str} and subtract from R{r+1} to create a zero below the pivot."
            ))

        pivot_row += 1

    steps.append(_step(
        "Upper Triangular (Row Echelon) Form",
        r"[U \mid c]",
        _augmented_latex(Aug),
        "All entries below the diagonal are now zero. We proceed with back-substitution."
    ))

    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(Aug[i][i]) < 1e-12:
            if abs(Aug[i][-1]) > 1e-12:
                return {"success": False, "error": "Inconsistent system: no solution exists (0 = non-zero)."}
            continue
        s = Aug[i][-1]
        for j in range(i + 1, n):
            s -= Aug[i][j] * x[j]
        x[i] = s / Aug[i][i]

    x_latex = r" \\ ".join([rf"x_{{{i+1}}} = {_fmt(x[i])}" for i in range(n)])
    steps.append(_step(
        "Back Substitution",
        r"x_i = \dfrac{1}{u_{ii}}\!\left(c_i - \sum_{j>i} u_{ij} x_j\right)",
        x_latex,
        "Starting from the last equation, solve for each variable upward."
    ))

    result_vec = vec_latex(x)
    return {"success": True, "steps": steps, "result_latex": result_vec}


# ─────────────────────────────────────────────

def solve_system_gauss_jordan(A, b):
    """Gauss-Jordan elimination (RREF → solution directly)."""
    steps = []
    try:
        A = [[float(x) for x in row] for row in A]
        b = [float(x) for x in b]
    except Exception as e:
        return {"success": False, "error": f"Invalid input: {e}"}

    n = len(b)
    if any(len(row) != n for row in A):
        return {"success": False, "error": "Coefficient matrix must be n×n."}

    Aug = [A[i][:] + [b[i]] for i in range(n)]

    steps.append(_step(
        "System Setup — Augmented Matrix [A|b]",
        r"[A \mid b] \xrightarrow{\text{RREF}} [I \mid x]",
        _augmented_latex(Aug),
        "Gauss-Jordan extends Gaussian elimination by also eliminating entries ABOVE each pivot, producing RREF = [I|x] directly."
    ))

    for col in range(n):
        # Partial pivoting
        max_row = col
        for r in range(col + 1, n):
            if abs(Aug[r][col]) > abs(Aug[max_row][col]):
                max_row = r

        if abs(Aug[max_row][col]) < 1e-12:
            continue

        if max_row != col:
            Aug[col], Aug[max_row] = Aug[max_row], Aug[col]
            steps.append(_step(
                f"Row Swap: R{col+1} ↔ R{max_row+1}",
                rf"R_{{{col+1}}} \leftrightarrow R_{{{max_row+1}}}",
                _augmented_latex(Aug),
                "Partial pivoting for numerical stability."
            ))

        pivot = Aug[col][col]
        Aug[col] = [v / pivot for v in Aug[col]]
        steps.append(_step(
            f"Normalize Pivot Row {col+1}: R{col+1} ← R{col+1} / ({_fmt(pivot)})",
            rf"R_{{{col+1}}} \leftarrow \dfrac{{1}}{{{_fmt(pivot)}}} R_{{{col+1}}}",
            _augmented_latex(Aug),
            f"Scale R{col+1} so the pivot becomes 1."
        ))

        for r in range(n):
            if r != col and abs(Aug[r][col]) > 1e-12:
                factor = Aug[r][col]
                Aug[r] = [Aug[r][c] - factor * Aug[col][c] for c in range(n + 1)]
                steps.append(_step(
                    f"Eliminate column {col+1} in R{r+1}: R{r+1} ← R{r+1} − ({_fmt(factor)})·R{col+1}",
                    rf"R_{{{r+1}}} \leftarrow R_{{{r+1}}} - ({_fmt(factor)}) R_{{{col+1}}}",
                    _augmented_latex(Aug),
                    "Eliminate all non-pivot entries in this column (above and below)."
                ))

    steps.append(_step(
        "Reduced Row Echelon Form [I|x]",
        r"[I \mid x] \Rightarrow \text{solution is last column}",
        _augmented_latex(Aug),
        "The left side is now the identity matrix I. The right column gives the exact solution vector x."
    ))

    x = [Aug[i][-1] for i in range(n)]
    x_latex = r" \\ ".join([rf"x_{{{i+1}}} = {_fmt(x[i])}" for i in range(n)])
    steps.append(_step(
        "Solution Vector",
        r"x = A^{-1}b",
        x_latex,
        "Reading the right column of [I|x] gives the solution."
    ))

    return {"success": True, "steps": steps, "result_latex": vec_latex(x)}


# ─────────────────────────────────────────────

def solve_system_inverse_method(A, b):
    """Solve Ax = b via x = A^{-1}b."""
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
        b_sp = sp.Matrix([sp.Rational(x) for x in b])
    except Exception as e:
        return {"success": False, "error": f"Invalid input: {e}"}

    if A_sp.rows != A_sp.cols:
        return {"success": False, "error": "Matrix Inverse Method requires a square coefficient matrix."}

    n = A_sp.rows
    steps.append(_step(
        "Method: x = A⁻¹b",
        r"Ax = b \Rightarrow x = A^{-1}b",
        rf"A = {mat_latex(A_sp)}, \quad b = {mat_latex(b_sp)}",
        "If A is invertible, we can multiply both sides of Ax = b on the left by A⁻¹ to get x = A⁻¹b."
    ))

    det = A_sp.det()
    steps.append(_step(
        "Check det(A) ≠ 0",
        r"\det(A) \neq 0 \Rightarrow A^{-1} \text{ exists}",
        rf"\det(A) = {sp.latex(det)}",
        f"det(A) = {sp.latex(det)}. {'A is invertible ✓' if det != 0 else 'A is singular — inverse does not exist!'}"
    ))

    if det == 0:
        return {"success": False, "error": "det(A) = 0: matrix is singular. Cannot use inverse method. Try Gaussian Elimination instead."}

    inv = A_sp.inv()
    steps.append(_step(
        "Compute A⁻¹",
        r"A^{-1} = \dfrac{1}{\det(A)} \text{adj}(A)",
        rf"A^{{-1}} = {mat_latex(inv)}",
        "The inverse is computed as (1/det) × adjugate."
    ))

    x = inv * b_sp
    steps.append(_step(
        "Multiply x = A⁻¹b",
        r"x = A^{-1} \cdot b",
        rf"x = {mat_latex(inv)} \cdot {mat_latex(b_sp)} = {mat_latex(x)}",
        "Matrix-multiply A⁻¹ by b to obtain the solution vector x."
    ))

    x_list = [x[i] for i in range(n)]
    x_latex = r" \\ ".join([rf"x_{{{i+1}}} = {sp.latex(x_list[i])}" for i in range(n)])
    steps.append(_step(
        "Solution",
        r"x_i \text{ (exact rational solution)}",
        x_latex,
        "SymPy computes exact rational solutions."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(x)}


# ─────────────────────────────────────────────

def solve_system_lu_decomposition(A, b):
    """LU Decomposition: A = LU, then Ly=b, Ux=y."""
    steps = []
    try:
        A_sp = sp.Matrix([[sp.Rational(x) if isinstance(x, (int, float)) else x
                           for x in row] for row in A])
        b_sp = sp.Matrix([sp.Rational(x) for x in b])
    except Exception as e:
        return {"success": False, "error": f"Invalid input: {e}"}

    n = A_sp.rows
    steps.append(_step(
        "LU Decomposition Overview",
        r"A = LU \text{ where } L = \text{lower triangular}, U = \text{upper triangular}",
        rf"A = {mat_latex(A_sp)}, \quad b = {mat_latex(b_sp)}",
        "LU decomposition factors A into a lower triangular matrix L (with 1s on diagonal) and upper triangular U. "
        "Useful for solving multiple systems with the same A but different b."
    ))

    try:
        L, U, perm = A_sp.LUdecomposition()
    except Exception as e:
        return {"success": False, "error": f"LU decomposition failed: {e}"}

    steps.append(_step(
        "Factor A = LU",
        r"A = L \cdot U",
        rf"L = {mat_latex(L)}, \quad U = {mat_latex(U)}",
        "L is lower triangular with 1s on its diagonal. U is upper triangular with the pivots on its diagonal."
    ))

    steps.append(_step(
        "L × U Verification",
        r"L \cdot U = A",
        rf"L \cdot U = {mat_latex(L * U)}",
        "Verify the factorization by multiplying L and U — the product should equal A."
    ))

    # Forward substitution: Ly = b
    # perm is a list of row swaps
    b_perm = b_sp.copy()
    for i, j in enumerate(perm):
        if j != i:
            b_perm.row_swap(i, j)

    y = sp.zeros(n, 1)
    for i in range(n):
        s = b_perm[i]
        for j in range(i):
            s -= L[i, j] * y[j]
        y[i] = s / L[i, i]

    steps.append(_step(
        "Step 1 — Forward Substitution: Ly = b",
        r"Ly = b \Rightarrow y_i = b_i - \sum_{j<i} L_{ij} y_j",
        rf"y = {mat_latex(y)}",
        "Solve Ly = b from top to bottom (forward). L is lower triangular so each y_i is found directly."
    ))

    # Back substitution: Ux = y
    x = sp.zeros(n, 1)
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= U[i, j] * x[j]
        if U[i, i] == 0:
            return {"success": False, "error": "Singular matrix encountered during back substitution."}
        x[i] = s / U[i, i]

    steps.append(_step(
        "Step 2 — Back Substitution: Ux = y",
        r"Ux = y \Rightarrow x_i = \frac{1}{U_{ii}}\!\left(y_i - \sum_{j>i} U_{ij} x_j\right)",
        rf"x = {mat_latex(x)}",
        "Solve Ux = y from bottom to top (backward). U is upper triangular."
    ))

    x_latex = r" \\ ".join([rf"x_{{{i+1}}} = {sp.latex(x[i])}" for i in range(n)])
    steps.append(_step(
        "Final Solution",
        r"x \text{ (exact solution)}",
        x_latex,
        "The exact solution vector x obtained via LU decomposition."
    ))

    return {"success": True, "steps": steps, "result_latex": mat_latex(x)}
