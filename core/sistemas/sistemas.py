"""
sistemas.py — Lógica pura para resolución de sistemas de ecuaciones lineales.
Métodos: Gauss-Seidel iterativo y Factorización LU.
"""
from dataclasses import dataclass, field
import numpy as np


@dataclass(frozen=True)
class GaussSeidelRow:
    iteration: int
    values: tuple[float, ...]
    error: float


@dataclass(frozen=True)
class LUStep:
    step: int
    operation: str
    matrix_l_snapshot: str
    matrix_u_snapshot: str
    observation: str


@dataclass(frozen=True)
class SystemResult:
    solution: list[float]
    iterations: int
    error: float
    converged: bool
    table: list
    procedure_steps: list[str]
    message: str = ""


# ── Gauss-Seidel ───────────────────────────────────────────────────

def gauss_seidel(matrix_a: list[list[float]], vector_b: list[float],
                 x0: list[float] | None = None,
                 tolerance: float = 1e-6, max_iterations: int = 100) -> SystemResult:
    """Método iterativo de Gauss-Seidel para sistemas lineales Ax = b."""
    A = np.array(matrix_a, dtype=float)
    b = np.array(vector_b, dtype=float)
    n = len(b)

    if A.shape != (n, n):
        raise ValueError(f"La matriz debe ser cuadrada {n}×{n}. Recibida: {A.shape}")

    # Verificar diagonal no nula
    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            raise ValueError(f"El elemento diagonal a[{i}][{i}] es cero. Reordene el sistema.")

    # Verificar dominancia diagonal
    is_diag_dominant = True
    for i in range(n):
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) < row_sum:
            is_diag_dominant = False
            break

    x = np.array(x0 if x0 else [0.0] * n, dtype=float)

    steps = [
        f"Sistema {n}×{n}",
        f"Tolerancia: {tolerance}",
        f"Vector inicial: {x.tolist()}",
    ]
    if not is_diag_dominant:
        steps.append("⚠ ADVERTENCIA: La matriz NO es diagonalmente dominante. "
                      "La convergencia no está garantizada.")

    table = []

    for iteration in range(1, max_iterations + 1):
        x_old = x.copy()
        for i in range(n):
            sigma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - sigma) / A[i][i]

        error = float(np.max(np.abs(x - x_old)))
        row = GaussSeidelRow(
            iteration=iteration,
            values=tuple(round(v, 8) for v in x),
            error=round(error, 8),
        )
        table.append(row)
        vals_str = ", ".join(f"x{j+1}={x[j]:.6f}" for j in range(n))
        steps.append(f"Iteración {iteration}: {vals_str}, error={error:.6e}")

        if error < tolerance:
            solution = [round(v, 10) for v in x]
            return SystemResult(
                solution=solution, iterations=iteration, error=round(error, 10),
                converged=True, table=table, procedure_steps=steps,
                message=f"Convergió en {iteration} iteraciones. Solución: {solution}"
            )

    solution = [round(v, 10) for v in x]
    return SystemResult(
        solution=solution, iterations=max_iterations,
        error=round(float(np.max(np.abs(x - np.array(x0 or [0]*n)))), 10),
        converged=False, table=table, procedure_steps=steps,
        message=f"No convergió en {max_iterations} iteraciones."
    )


# ── Factorización LU ──────────────────────────────────────────────

def factorizacion_lu(matrix_a: list[list[float]],
                     vector_b: list[float]) -> SystemResult:
    """Factorización LU (Doolittle) para resolver Ax = b."""
    A = np.array(matrix_a, dtype=float)
    b = np.array(vector_b, dtype=float)
    n = len(b)

    if A.shape != (n, n):
        raise ValueError(f"La matriz debe ser cuadrada {n}×{n}. Recibida: {A.shape}")

    L = np.eye(n)
    U = np.zeros((n, n))
    table = []
    steps = [f"Factorización LU (Doolittle) para sistema {n}×{n}", ""]
    step_count = 0

    for j in range(n):
        # Fila de U
        for i in range(j + 1):
            s = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - s

        # Columna de L
        for i in range(j + 1, n):
            s = sum(L[i][k] * U[k][j] for k in range(j))
            if abs(U[j][j]) < 1e-14:
                raise ValueError(f"Pivote U[{j}][{j}] = 0. La factorización LU no es posible sin pivoteo.")
            L[i][j] = (A[i][j] - s) / U[j][j]

        step_count += 1
        lu_step = LUStep(
            step=step_count,
            operation=f"Procesar columna {j + 1}",
            matrix_l_snapshot=_matrix_to_string(L),
            matrix_u_snapshot=_matrix_to_string(U),
            observation=f"U[{j}][{j}] = {U[j][j]:.6f}",
        )
        table.append(lu_step)
        steps.append(f"Paso {step_count}: Columna {j+1} procesada")

    # Sustitución hacia adelante: Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][k] * y[k] for k in range(i))

    steps.append("")
    steps.append("Sustitución hacia adelante (Ly = b):")
    for i in range(n):
        steps.append(f"  y{i+1} = {y[i]:.6f}")

    # Sustitución hacia atrás: Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]

    steps.append("")
    steps.append("Sustitución hacia atrás (Ux = y):")
    for i in range(n):
        steps.append(f"  x{i+1} = {x[i]:.6f}")

    solution = [round(v, 10) for v in x]
    residual = float(np.max(np.abs(A @ x - b)))

    return SystemResult(
        solution=solution, iterations=step_count, error=round(residual, 10),
        converged=True, table=table, procedure_steps=steps,
        message=f"Solución: {solution} | Residuo máximo: {residual:.2e}"
    )


def _matrix_to_string(matrix: np.ndarray) -> str:
    """Representación compacta de una matriz para la tabla."""
    rows_str = []
    for row in matrix:
        rows_str.append("[" + ", ".join(f"{v:8.4f}" for v in row) + "]")
    return "\n".join(rows_str)
