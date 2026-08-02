from django.core.management.base import BaseCommand
from courses.models import Unit, Topic, Lesson
from quiz.models import Quiz, Question, Answer

class Command(BaseCommand):
    help = 'Seeds initial complete Linear Algebra curriculum for Unit 1 and Unit 2 with Quizzes and Questions.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting curriculum seeding...'))

        # Clean existing units/topics to avoid duplicate seed issues
        Unit.objects.all().delete()

        # ==========================================
        # UNIT 1: Matrix Algebra, Systems & Vectors
        # ==========================================
        u1 = Unit.objects.create(
            unit_number=1,
            title="Foundations of Matrix Algebra, Systems & Vectors",
            description="Explore fundamental matrix operations, systems of linear equations, and vector algebra in multi-dimensional space.",
            icon="bi-grid-3x3-gap-fill"
        )

        # TOPIC 1.1: Algebra of Matrices
        t1_1 = Topic.objects.create(
            unit=u1,
            title="Algebra of Matrices",
            description="Master matrix definitions, special types, algebraic operations, transpositions, and symmetry.",
            order=1
        )

        Lesson.objects.create(
            topic=t1_1,
            title="Matrix Introduction & Types of Matrices",
            order=1,
            introduction="A matrix is a rectangular array of numbers, symbols, or expressions arranged in rows and columns.",
            objectives="• Understand matrix order ($m \\times n$)\n• Recognize Row, Column, Square, Diagonal, Identity, Zero, and Triangular matrices",
            theory="""A matrix $A$ of order $m \\times n$ has $m$ rows and $n$ columns:
$$A = \\begin{bmatrix} a_{11} & a_{12} & \\dots & a_{1n} \\\\ a_{21} & a_{22} & \\dots & a_{2n} \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ a_{m1} & a_{m2} & \\dots & a_{mn} \\end{bmatrix}$$

### Special Matrix Types:
1. **Square Matrix**: $m = n$.
2. **Identity Matrix ($I$)**: Square matrix with 1s on principal diagonal and 0s elsewhere: $I_2 = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$.
3. **Diagonal Matrix**: All non-diagonal entries are 0.
4. **Symmetric Matrix**: $A^T = A$.
5. **Skew-Symmetric Matrix**: $A^T = -A$.
6. **Orthogonal Matrix**: $A^T A = A A^T = I$ (or $A^{-1} = A^T$).""",
            definitions="• **Order of Matrix**: Dimension $m \\times n$ indicating row count $m$ and column count $n$.\n• **Principal Diagonal**: Set of entries $a_{ii}$ where row index equals column index.",
            formula_cards="""{"cards": [
                {"title": "Identity Matrix Property", "formula": "A \\cdot I = I \\cdot A = A"},
                {"title": "Symmetric Condition", "formula": "A^T = A \\iff a_{ij} = a_{ji}"},
                {"title": "Orthogonal Matrix Condition", "formula": "A^T A = I \\iff A^{-1} = A^T"}
            ]}""",
            worked_examples="""Example 1: Identify if $A = \\begin{bmatrix} 0 & 2 \\\\ -2 & 0 \\end{bmatrix}$ is Skew-Symmetric.
Solution:
$A^T = \\begin{bmatrix} 0 & -2 \\\\ 2 & 0 \\end{bmatrix} = - \\begin{bmatrix} 0 & 2 \\\\ -2 & 0 \\end{bmatrix} = -A$.
Since $A^T = -A$, $A$ is Skew-Symmetric.""",
            practice_questions="1. Determine the transpose of $B = \\begin{bmatrix} 1 & 4 & 7 \\\\ 2 & 5 & 8 \\end{bmatrix}$.\n2. Prove that for any square matrix $A$, $A + A^T$ is symmetric.",
            summary="Matrices are rectangular arrays. Square matrices possess special properties including symmetry ($A^T=A$) and orthogonality ($A^T A=I$).",
            has_interactive_calculator=True,
            calculator_type="matrix"
        )

        Lesson.objects.create(
            topic=t1_1,
            title="Matrix Addition, Subtraction & Scalar Multiplication",
            order=2,
            introduction="Algebraic operations allow matrices to be added, subtracted, and scaled.",
            objectives="• Perform matrix addition and subtraction for matrices of matching dimensions\n• Compute scalar multiples $k A$",
            theory="""### 1. Matrix Addition & Subtraction
Given matrices $A, B \\in \\mathbb{R}^{m \\times n}$, their sum $C = A \\pm B$ has elements:
$$c_{ij} = a_{ij} \\pm b_{ij}$$

### 2. Scalar Multiplication
Multiplying a matrix $A$ by scalar $k \\in \\mathbb{R}$ scales every entry:
$$k A = \\begin{bmatrix} k a_{11} & k a_{12} \\\\ k a_{21} & k a_{22} \\end{bmatrix}$$""",
            definitions="• **Commutativity of Addition**: $A + B = B + A$.\n• **Associativity**: $(A + B) + C = A + (B + C)$.",
            formula_cards="""{"cards": [
                {"title": "Scalar Property", "formula": "k(A + B) = kA + kB"},
                {"title": "Transpose of Sum", "formula": "(A + B)^T = A^T + B^T"}
            ]}""",
            worked_examples="""Compute $2A - B$ for $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}, B = \\begin{bmatrix} 0 & 1 \\\\ -1 & 2 \\end{bmatrix}$.
Solution:
$2A = \\begin{bmatrix} 2 & 4 \\\\ 6 & 8 \\end{bmatrix}$.
$2A - B = \\begin{bmatrix} 2-0 & 4-1 \\\\ 6-(-1) & 8-2 \\end{bmatrix} = \\begin{bmatrix} 2 & 3 \\\\ 7 & 6 \\end{bmatrix}$.""",
            practice_questions="Calculate $3A + 2B$ when $A = \\begin{bmatrix} 5 & 1 \\\\ 2 & 0 \\end{bmatrix}$ and $B = \\begin{bmatrix} -1 & 4 \\\\ 3 & 2 \\end{bmatrix}$.",
            summary="Matrix addition is element-wise and commutative. Scalar multiplication scales all individual entries uniformly.",
            has_interactive_calculator=True,
            calculator_type="matrix"
        )

        Lesson.objects.create(
            topic=t1_1,
            title="Matrix Multiplication & Properties",
            order=3,
            introduction="Matrix multiplication represents composite linear mappings and dot products between rows and columns.",
            objectives="• Master row-column dot product multiplication\n• Understand non-commutativity ($AB \\neq BA$ in general)\n• Compute matrix transpose product rule $(AB)^T = B^T A^T$",
            theory="""If $A$ is $m \\times p$ and $B$ is $p \\times n$, the product $C = A B$ is an $m \\times n$ matrix with entries:
$$c_{ij} = \\sum_{k=1}^{p} a_{ik} b_{kj}$$

### Key Properties:
1. **Non-Commutative**: In general, $A B \\neq B A$.
2. **Associative**: $(A B) C = A (B C)$.
3. **Distributive**: $A (B + C) = A B + A C$.
4. **Transpose of Product**: $(AB)^T = B^T A^T$ (Reversal Rule).""",
            definitions="• **Inner Product Rule**: Entry $c_{ij}$ is the dot product of row $i$ of $A$ and column $j$ of $B$.",
            formula_cards="""{"cards": [
                {"title": "Product Transpose Rule", "formula": "(A \\cdot B)^T = B^T \\cdot A^T"},
                {"title": "Matrix Product Dimension", "formula": "(m \\times p) \\cdot (p \\times n) \\to (m \\times n)"}
            ]}""",
            worked_examples="""Multiply $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}$ and $B = \\begin{bmatrix} 2 & 0 \\\\ 1 & 3 \\end{bmatrix}$.
Solution:
$c_{11} = 1(2)+2(1) = 4$, $c_{12} = 1(0)+2(3) = 6$
$c_{21} = 3(2)+4(1) = 10$, $c_{22} = 3(0)+4(3) = 12$
$A B = \\begin{bmatrix} 4 & 6 \\\\ 10 & 12 \\end{bmatrix}$.""",
            practice_questions="Verify whether $A B = B A$ for $A = \\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix}$ and $B = \\begin{bmatrix} 0 & 1 \\\\ 0 & 0 \\end{bmatrix}$.",
            summary="Matrix multiplication relies on compatible inner dimensions. Product of transposes reverses order: $(AB)^T = B^T A^T$.",
            has_interactive_calculator=True,
            calculator_type="matrix"
        )

        # TOPIC 1.2: Systems of Linear Equations
        t1_2 = Topic.objects.create(
            unit=u1,
            title="Systems of Linear Equations",
            description="Methods for solving linear systems: Gaussian Elimination, Gauss-Jordan, Inverse Method, and LU Decomposition.",
            order=2
        )

        Lesson.objects.create(
            topic=t1_2,
            title="Gaussian & Gauss-Jordan Elimination",
            order=1,
            introduction="Systematic elementary row operations transform augmented matrices into Row Echelon Form (REF) or Reduced Row Echelon Form (RREF).",
            objectives="• Apply Elementary Row Operations (EROs)\n• Perform forward elimination for Gaussian Elimination\n• Reduce to RREF for Gauss-Jordan method",
            theory="""A system of linear equations $A x = b$ can be written as an augmented matrix $[A \\mid b]$.

### Elementary Row Operations (EROs):
1. **$R_i \\leftrightarrow R_j$**: Interchange two rows.
2. **$R_i \\leftarrow k R_i$ ($k \\neq 0$)**: Scale a row by a non-zero scalar.
3. **$R_i \\leftarrow R_i + k R_j$**: Add a scalar multiple of one row to another.

### Gaussian Elimination vs Gauss-Jordan:
• **Gaussian Elimination**: Reduces $[A \\mid b]$ to Row Echelon Form (REF), followed by back-substitution.
• **Gauss-Jordan Elimination**: Continues EROs until $[A \\mid b]$ reaches Reduced Row Echelon Form (RREF) $[I \\mid x]$.""",
            definitions="• **Pivot**: The first non-zero entry in a row.\n• **RREF**: Each pivot is 1, and all other entries in pivot columns are 0.",
            formula_cards="""{"cards": [
                {"title": "Augmented System", "formula": "[A \\mid b] \\xrightarrow{RREF} [I \\mid x]"},
                {"title": "Consistency Condition", "formula": "\\text{Rank}(A) = \\text{Rank}([A \\mid b])"}
            ]}""",
            worked_examples="""Solve using Gauss-Jordan:
$x + 2y = 5$
$3x + 4y = 11$
Solution:
$[A \\mid b] = \\begin{bmatrix} 1 & 2 & \\mid & 5 \\\\ 3 & 4 & \\mid & 11 \\end{bmatrix}$
$R_2 \\leftarrow R_2 - 3 R_1 \\implies \\begin{bmatrix} 1 & 2 & \\mid & 5 \\\\ 0 & -2 & \\mid & -4 \\end{bmatrix}$
$R_2 \\leftarrow R_2 / (-2) \\implies \\begin{bmatrix} 1 & 2 & \\mid & 5 \\\\ 0 & 1 & \\mid & 2 \\end{bmatrix}$
$R_1 \\leftarrow R_1 - 2 R_2 \\implies \\begin{bmatrix} 1 & 0 & \\mid & 1 \\\\ 0 & 1 & \\mid & 2 \\end{bmatrix}$
Thus $x = 1, y = 2$.""",
            practice_questions="Solve the $3 \\times 3$ system using Gaussian Elimination: $x+y+z=6, 2x-y+z=3, x-2y+3z=6$.",
            summary="Elementary row operations transform linear systems into row echelon forms to extract exact solution vectors.",
            has_interactive_calculator=True,
            calculator_type="system"
        )

        Lesson.objects.create(
            topic=t1_2,
            title="Matrix Inverse Method & LU Decomposition",
            order=2,
            introduction="Direct matrix algebraic approaches using $x = A^{-1} b$ and triangular matrix factorization $A = L U$.",
            objectives="• Solve $A x = b$ using matrix inverse $A^{-1}$\n• Factorize non-singular matrix $A$ into Lower ($L$) and Upper ($U$) triangular matrices",
            theory="""### 1. Matrix Inverse Method
For square coefficient matrix $A$ with $\\det(A) \\neq 0$:
$$x = A^{-1} b$$

### 2. LU Decomposition
Factorize matrix $A$ into lower triangular $L$ (with 1s on diagonal) and upper triangular $U$:
$$A = L \\cdot U$$
To solve $A x = b$:
1. Solve $L y = b$ for intermediate vector $y$ via **forward substitution**.
2. Solve $U x = y$ for solution vector $x$ via **back substitution**.""",
            definitions="• **Lower Triangular ($L$)**: All elements above principal diagonal are 0.\n• **Upper Triangular ($U$)**: All elements below principal diagonal are 0.",
            formula_cards="""{"cards": [
                {"title": "LU System Solution", "formula": "A = L U \\implies L y = b \\text{ then } U x = y"},
                {"title": "Matrix Inverse Solution", "formula": "x = A^{-1} b"}
            ]}""",
            worked_examples="""Given $A = L U = \\begin{bmatrix} 1 & 0 \\\\ 2 & 1 \\end{bmatrix} \\begin{bmatrix} 3 & 1 \\\\ 0 & 4 \\end{bmatrix}$ and $b = \\begin{bmatrix} 5 \\\\ 14 \\end{bmatrix}$. Solve $A x = b$.
Step 1: Solve $L y = b$:
$y_1 = 5$
$2y_1 + y_2 = 14 \\implies 2(5) + y_2 = 14 \\implies y_2 = 4$. So $y = \\begin{bmatrix} 5 \\\\ 4 \\end{bmatrix}$.
Step 2: Solve $U x = y$:
$4 x_2 = 4 \\implies x_2 = 1$
$3 x_1 + 1(1) = 5 \\implies 3 x_1 = 4 \\implies x_1 = 4/3$.
Solution $x = \\begin{bmatrix} 4/3 \\\\ 1 \\end{bmatrix}$.""",
            practice_questions="Decompose $A = \\begin{bmatrix} 2 & 4 \\\\ 1 & 7 \\end{bmatrix}$ into $L U$ form.",
            summary="LU decomposition splits heavy matrix operations into efficient forward and backward triangular system substitutions.",
            has_interactive_calculator=True,
            calculator_type="system"
        )

        # TOPIC 1.3: Vectors
        t1_3 = Topic.objects.create(
            unit=u1,
            title="Vectors & Vector Spaces",
            description="Vector fundamentals: dot product, cross product, angle calculation, and projections.",
            order=3
        )

        Lesson.objects.create(
            topic=t1_3,
            title="Vector Algebra, Dot & Cross Products",
            order=1,
            introduction="Vectors convey magnitude and direction in geometric and algebraic vector spaces.",
            objectives="• Compute Euclidean magnitude $|\\vec{v}|$\n• Calculate scalar dot product $\\vec{u} \\cdot \\vec{v}$ and vector cross product $\\vec{u} \\times \\vec{v}$\n• Compute orthogonal vector projection",
            theory="""### 1. Vector Magnitude & Dot Product
For $\\vec{u} = (u_1, u_2, u_3)$ and $\\vec{v} = (v_1, v_2, v_3)$:
$$||\\vec{u}|| = \\sqrt{u_1^2 + u_2^2 + u_3^2}$$
$$\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3 = ||\\vec{u}|| \\, ||\\vec{v}|| \\cos(\\theta)$$

### 2. Cross Product (3D Vectors)
$$\\vec{u} \\times \\vec{v} = \\begin{bmatrix} \\hat{i} & \\hat{j} & \\hat{k} \\\\ u_1 & u_2 & u_3 \\\\ v_1 & v_2 & v_3 \\end{bmatrix}$$

### 3. Vector Projection
Projection of $\\vec{u}$ onto $\\vec{v}$:
$$\\text{proj}_{\\vec{v}} \\vec{u} = \\left( \\frac{\\vec{u} \\cdot \\vec{v}}{||\\vec{v}||^2} \\right) \\vec{v}$$""",
            definitions="• **Orthogonal Vectors**: Two vectors are perpendicular if $\\vec{u} \\cdot \\vec{v} = 0$.\n• **Unit Vector**: Vector with magnitude 1: $\\hat{v} = \\vec{v} / ||\\vec{v}||$.",
            formula_cards="""{"cards": [
                {"title": "Angle Between Vectors", "formula": "\\cos(\\theta) = \\frac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\| \\|\\vec{v}\\|}"},
                {"title": "Orthogonal Projection", "formula": "\\text{proj}_{\\vec{v}} \\vec{u} = \\frac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{v}\\|^2} \\vec{v}"}
            ]}""",
            worked_examples="""Find dot product and cross product for $\\vec{u} = (1, 2, 3)$ and $\\vec{v} = (4, 5, 6)$.
Dot Product: $1(4)+2(5)+3(6) = 4 + 10 + 18 = 32$.
Cross Product:
$\\hat{i}(2\\cdot6 - 3\\cdot5) - \\hat{j}(1\\cdot6 - 3\\cdot4) + \\hat{k}(1\\cdot5 - 2\\cdot4) = -3\\hat{i} + 6\\hat{j} - 3\\hat{k} = (-3, 6, -3)$.""",
            practice_questions="Calculate the angle between vectors $\\vec{u} = (1, 0)$ and $\\vec{v} = (1, 1)$.",
            summary="Dot product yields scalar projection and angle; cross product produces a perpendicular vector in 3D space.",
            has_interactive_calculator=True,
            calculator_type="vector"
        )


        # ==========================================
        # UNIT 2: Transformations, Determinants & Eigenvalues
        # ==========================================
        u2 = Unit.objects.create(
            unit_number=2,
            title="Linear Transformations, Determinants & Eigenvalues",
            description="Explore spatial geometric mappings, matrix determinants, characteristic equations, and matrix diagonalization.",
            icon="bi-bounding-box-circles"
        )

        # TOPIC 2.1: Linear Transformations
        t2_1 = Topic.objects.create(
            unit=u2,
            title="Linear Transformations & 2D Geometry",
            order=1,
            description="Understand linear maps, transformation matrices, rotations, scaling, reflections, and compositions."
        )

        Lesson.objects.create(
            topic=t2_1,
            title="2D Linear Transformations & Matrices",
            order=1,
            introduction="Linear transformations map vectors between vector spaces while preserving vector addition and scalar multiplication.",
            objectives="• Construct 2D transformation matrices for Rotation, Scaling, Reflection, and Shearing\n• Compute composite transformations via matrix multiplication $T_{comp} = M_2 M_1$",
            theory="""A linear transformation $T: \\mathbb{R}^2 \\to \\mathbb{R}^2$ is represented by a $2 \\times 2$ matrix $M$:
$$T(\\vec{x}) = M \\vec{x}$$

### Standard 2D Transformation Matrices:
1. **Rotation by angle $\\theta$**:
   $$M_{rot} = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}$$
2. **Scaling ($s_x, s_y$)**:
   $$M_{scale} = \\begin{bmatrix} s_x & 0 \\\\ 0 & s_y \\end{bmatrix}$$
3. **Reflection across X-axis**:
   $$M_{refX} = \\begin{bmatrix} 1 & 0 \\\\ 0 & -1 \\end{bmatrix}$$
4. **Shear parallel to X-axis ($k$)**:
   $$M_{shearX} = \\begin{bmatrix} 1 & k \\\\ 0 & 1 \\end{bmatrix}$$""",
            definitions="• **Linearity Axioms**: $T(\\vec{u} + \\vec{v}) = T(\\vec{u}) + T(\\vec{v})$ and $T(c \\vec{v}) = c T(\\vec{v})$.\n• **Composition**: Applying $T_1$ followed by $T_2$ corresponds to matrix product $M = M_2 M_1$.",
            formula_cards="""{"cards": [
                {"title": "2D Rotation Matrix", "formula": "M(\\theta) = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}"},
                {"title": "Composite Map", "formula": "(T_2 \\circ T_1)(\\vec{v}) = M_2 \\cdot M_1 \\cdot \\vec{v}"}
            ]}""",
            worked_examples="""Rotate vector $\\vec{v} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}$ counterclockwise by $90^\\circ$ ($\\pi/2$).
Solution:
$M = \\begin{bmatrix} \\cos 90^\\circ & -\\sin 90^\\circ \\\\ \\sin 90^\\circ & \\cos 90^\\circ \\end{bmatrix} = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$
$T(\\vec{v}) = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix} \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}$.""",
            practice_questions="Find the matrix representing a reflection across the line $y = x$.",
            summary="Linear transformations map grid spaces; composition of geometric transforms equals matrix multiplication.",
            has_interactive_calculator=True,
            calculator_type="transformations"
        )

        # TOPIC 2.2: Determinants
        t2_2 = Topic.objects.create(
            unit=u2,
            title="Determinants & Inverses",
            order=2,
            description="Determinant properties, minor/cofactor expansion, adjugate matrix, and Cramer's rule."
        )

        Lesson.objects.create(
            topic=t2_2,
            title="Properties of Determinants & Adjugate Inverses",
            order=1,
            introduction="Determinants measure the geometric scaling factor of a transformation and determine invertibility.",
            objectives="• Compute determinant using cofactor expansion\n• Understand determinant algebraic properties\n• Calculate inverse using Adjugate matrix formula $A^{-1} = \\frac{1}{\\det(A)} \\text{adj}(A)$",
            theory="""### Key Properties of Determinants:
1. **Transpose**: $\\det(A^T) = \\det(A)$.
2. **Product Rule**: $\\det(A B) = \\det(A) \\cdot \\det(B)$.
3. **Inverse Rule**: $\\det(A^{-1}) = \\frac{1}{\\det(A)}$.
4. **Scalar Scaling**: For $n \\times n$ matrix $A$, $\\det(k A) = k^n \\det(A)$.
5. **Row Operations**:
   - Row swap changes determinant sign.
   - Adding a multiple of one row to another leaves determinant unchanged.

### Inverse via Adjugate Matrix:
$$A^{-1} = \\frac{1}{\\det(A)} \\text{adj}(A)$$
where $\\text{adj}(A) = C^T$, and $C_{ij} = (-1)^{i+j} M_{ij}$ is the cofactor matrix.""",
            definitions="• **Minor ($M_{ij}$)**: Determinant of $(n-1)\\times(n-1)$ submatrix formed by deleting row $i$ and column $j$.\n• **Cofactor ($C_{ij}$)**: $C_{ij} = (-1)^{i+j} M_{ij}$.",
            formula_cards="""{"cards": [
                {"title": "Determinant Product Rule", "formula": "\\det(A \\cdot B) = \\det(A) \\cdot \\det(B)"},
                {"title": "Adjugate Inverse Formula", "formula": "A^{-1} = \\frac{1}{\\det(A)} \\text{adj}(A)"}
            ]}""",
            worked_examples="""Find adjugate and inverse for $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}$.
Solution:
$\\det(A) = 1(4) - 2(3) = -2$.
Cofactors: $C_{11}=4, C_{12}=-3, C_{21}=-2, C_{22}=1$.
$\\text{adj}(A) = C^T = \\begin{bmatrix} 4 & -2 \\\\ -3 & 1 \\end{bmatrix}$.
$A^{-1} = -\\frac{1}{2} \\begin{bmatrix} 4 & -2 \\\\ -3 & 1 \\end{bmatrix} = \\begin{bmatrix} -2 & 1 \\\\ 1.5 & -0.5 \\end{bmatrix}$.""",
            practice_questions="Compute the determinant of $A = \\begin{bmatrix} 2 & 0 & 1 \\\\ 0 & 3 & 0 \\\\ 1 & 0 & 4 \\end{bmatrix}$.",
            summary="A non-zero determinant guarantees matrix invertibility; adjugate transpose formulas provide direct algebraic inverses.",
            has_interactive_calculator=True,
            calculator_type="matrix"
        )

        # TOPIC 2.3: Eigenvalues & Diagonalization
        t2_3 = Topic.objects.create(
            unit=u2,
            title="Eigenvalues, Eigenvectors & Diagonalization",
            order=3,
            description="Characteristic equations, eigenspaces, matrix power computation, and diagonalization $A = P D P^{-1}$."
        )

        Lesson.objects.create(
            topic=t2_3,
            title="Characteristic Equation & Matrix Diagonalization",
            order=1,
            introduction="Eigenvectors are non-zero vectors whose direction remains unchanged under linear transformation.",
            objectives="• Solve characteristic polynomial $\\det(A - \\lambda I) = 0$ for eigenvalues $\\lambda$\n• Find eigenvectors by solving linear system $(A - \\lambda I)\\vec{v} = 0$\n• Diagonalize matrix $A = P D P^{-1}$",
            theory="""### 1. Eigenvalue Equation
$$A \\vec{v} = \\lambda \\vec{v} \\iff (A - \\lambda I) \\vec{v} = \\vec{0}$$
For non-trivial eigenvector solutions $\\vec{v} \\neq \\vec{0}$, we must have:
$$\\det(A - \\lambda I) = 0$$

### 2. Matrix Diagonalization
If $n \\times n$ matrix $A$ has $n$ linearly independent eigenvectors $\\vec{v}_1, \\vec{v}_2, \\dots, \\vec{v}_n$ corresponding to eigenvalues $\\lambda_1, \\lambda_2, \\dots, \\lambda_n$:
$$A = P D P^{-1}$$
where:
• $P = [\\vec{v}_1 \\mid \\vec{v}_2 \\mid \\dots \\mid \\vec{v}_n]$ (Matrix of eigenvectors)
• $D = \\text{diag}(\\lambda_1, \\lambda_2, \\dots, \\lambda_n)$ (Diagonal matrix of eigenvalues)

### Power Computation Application:
$$A^k = P D^k P^{-1} = P \\begin{bmatrix} \\lambda_1^k & 0 \\\\ 0 & \\lambda_2^k \\end{bmatrix} P^{-1}$$""",
            definitions="• **Eigenspace**: Null space of $(A - \\lambda I)$ containing all eigenvectors corresponding to $\\lambda$.\n• **Diagonalizable**: Matrix $A$ is diagonalizable if it has $n$ linearly independent eigenvectors.",
            formula_cards="""{"cards": [
                {"title": "Characteristic Polynomial", "formula": "\\det(A - \\lambda I) = 0"},
                {"title": "Diagonalization Decomposition", "formula": "A = P D P^{-1} \\implies A^k = P D^k P^{-1}"}
            ]}""",
            worked_examples="""Find eigenvalues of $A = \\begin{bmatrix} 4 & 1 \\\\ 2 & 3 \\end{bmatrix}$.
Solution:
$\\det(A - \\lambda I) = \\det\\begin{bmatrix} 4-\\lambda & 1 \\\\ 2 & 3-\\lambda \\end{bmatrix} = (4-\\lambda)(3-\\lambda) - 2 = \\lambda^2 - 7\\lambda + 10 = 0$.
$(\\lambda - 5)(\\lambda - 2) = 0 \\implies \\lambda_1 = 5, \\lambda_2 = 2$.""",
            practice_questions="Find the eigenvectors corresponding to $\\lambda = 5$ for $A = \\begin{bmatrix} 4 & 1 \\\\ 2 & 3 \\end{bmatrix}$.",
            summary="Eigenvalues decompose complex linear operators into pure scaling along invariant eigenvector axes.",
            has_interactive_calculator=True,
            calculator_type="matrix"
        )


        # ==========================================
        # SEED QUIZZES AND QUESTIONS
        # ==========================================
        self.stdout.write(self.style.SUCCESS('Seeding Quizzes and Questions...'))

        q1 = Quiz.objects.create(
            topic=t1_1,
            title="Matrix Fundamentals Quiz",
            description="Test your understanding of matrix dimensions, symmetry, transpose rules, and matrix multiplication.",
            time_limit_minutes=10,
            pass_mark_percentage=60
        )

        qn1 = Question.objects.create(
            quiz=q1,
            text="If matrix $A$ has dimension $3 \\times 2$ and matrix $B$ has dimension $2 \\times 4$, what is the dimension of product $AB$?",
            explanation="When multiplying $(m \\times p) \\cdot (p \\times n)$, the resulting matrix dimension is $m \\times n$. Here $(3 \\times 2) \\cdot (2 \\times 4) \\to 3 \\times 4$.",
            marks=1
        )
        Answer.objects.create(question=qn1, text="3 x 4", is_correct=True)
        Answer.objects.create(question=qn1, text="2 x 2", is_correct=False)
        Answer.objects.create(question=qn1, text="3 x 2", is_correct=False)
        Answer.objects.create(question=qn1, text="Product is undefined", is_correct=False)

        qn2 = Question.objects.create(
            quiz=q1,
            text="Which condition defines a Symmetric Matrix?",
            explanation="A square matrix is symmetric if and only if its transpose equals itself ($A^T = A$).",
            marks=1
        )
        Answer.objects.create(question=qn2, text="A^T = A", is_correct=True)
        Answer.objects.create(question=qn2, text="A^T = -A", is_correct=False)
        Answer.objects.create(question=qn2, text="A^T = A^{-1}", is_correct=False)
        Answer.objects.create(question=qn2, text="det(A) = 0", is_correct=False)


        q2 = Quiz.objects.create(
            topic=t1_2,
            title="Linear Systems & Gaussian Elimination Quiz",
            description="Assess your knowledge of Row Echelon Form, elementary row operations, and LU decomposition.",
            time_limit_minutes=10,
            pass_mark_percentage=60
        )

        qn3 = Question.objects.create(
            quiz=q2,
            text="What is the result of solving $A x = b$ using LU decomposition?",
            explanation="LU decomposition solves $L y = b$ first using forward substitution, followed by $U x = y$ using back substitution.",
            marks=1
        )
        Answer.objects.create(question=qn3, text="Solve L y = b then U x = y", is_correct=True)
        Answer.objects.create(question=qn3, text="Solve U y = b then L x = y", is_correct=False)
        Answer.objects.create(question=qn3, text="Compute A^{-1} b directly", is_correct=False)
        Answer.objects.create(question=qn3, text="Multiply L and U matrices", is_correct=False)


        q3 = Quiz.objects.create(
            topic=t2_3,
            title="Eigenvalues & Diagonalization Quiz",
            description="Test your skills on finding eigenvalues from characteristic equations and matrix powers.",
            time_limit_minutes=15,
            pass_mark_percentage=60
        )

        qn4 = Question.objects.create(
            quiz=q3,
            text="What equation must be solved to determine the eigenvalues $\\lambda$ of a square matrix $A$?",
            explanation="Eigenvalues are roots of the characteristic polynomial equation $\\det(A - \\lambda I) = 0$.",
            marks=1
        )
        Answer.objects.create(question=qn4, text="det(A - \\lambda I) = 0", is_correct=True)
        Answer.objects.create(question=qn4, text="Ax = 0", is_correct=False)
        Answer.objects.create(question=qn4, text="trace(A) = 0", is_correct=False)
        Answer.objects.create(question=qn4, text="A^T A = I", is_correct=False)

        self.stdout.write(self.style.SUCCESS('Successfully seeded complete curriculum, topics, lessons, and quizzes!'))
