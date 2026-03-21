"""
interpolacion.py — Lógica pura para interpolación polinómica.
Métodos de Lagrange y Newton con diferencias divididas.
"""
from dataclasses import dataclass, field
import numpy as np
import sympy as sp


@dataclass(frozen=True)
class LagrangeRow:
    i: int
    xi: float
    yi: float
    li_value: float
    term: float
    accumulated: float


@dataclass(frozen=True)
class NewtonInterpRow:
    i: int
    xi: float
    yi: float
    divided_diff: float
    coefficient: float
    accumulated: float


@dataclass(frozen=True)
class InterpolationResult:
    polynomial_str: str
    interpolated_value: float
    table: list
    procedure_steps: list[str]
    x_plot: list[float]
    y_plot: list[float]
    message: str = ""


# ── Lagrange ───────────────────────────────────────────────────────

def lagrange(x_points: list[float], y_points: list[float],
             x_eval: float) -> InterpolationResult:
    """Interpolación de Lagrange."""
    n = len(x_points)
    if n != len(y_points):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")
    if n < 2:
        raise ValueError("Se necesitan al menos 2 puntos para interpolar.")
    if len(set(x_points)) != n:
        raise ValueError("Los valores de x no deben repetirse.")

    table = []
    steps = [
        f"Puntos: {list(zip(x_points, y_points))}",
        f"Valor a interpolar: x = {x_eval}",
        f"Grado del polinomio: {n - 1}",
        "",
    ]

    accumulated = 0.0
    for i in range(n):
        li = 1.0
        for j in range(n):
            if i != j:
                li *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
        term = y_points[i] * li
        accumulated += term

        row = LagrangeRow(
            i=i, xi=round(x_points[i], 8), yi=round(y_points[i], 8),
            li_value=round(li, 8), term=round(term, 8),
            accumulated=round(accumulated, 8),
        )
        table.append(row)
        steps.append(
            f"L{i}({x_eval}) = {li:.6f}, término = {y_points[i]:.4f}×{li:.6f} = {term:.6f}, "
            f"acumulado = {accumulated:.6f}"
        )

    # Generar curva para gráfica
    x_arr = np.array(x_points, dtype=float)
    x_min, x_max = min(x_points), max(x_points)
    margin = (x_max - x_min) * 0.2 if x_max > x_min else 1.0
    x_plot = np.linspace(x_min - margin, x_max + margin, 200).tolist()
    y_plot = []
    for xv in x_plot:
        val = 0.0
        for i in range(n):
            li = 1.0
            for j in range(n):
                if i != j:
                    li *= (xv - x_points[j]) / (x_points[i] - x_points[j])
            val += y_points[i] * li
        y_plot.append(val)

    return InterpolationResult(
        polynomial_str=f"P(x) de grado {n-1} por Lagrange",
        interpolated_value=round(accumulated, 10),
        table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"P({x_eval}) ≈ {accumulated:.10f}",
    )


# ── Newton (Diferencias Divididas) ─────────────────────────────────

def newton_interpolation(x_points: list[float], y_points: list[float],
                         x_eval: float) -> InterpolationResult:
    """Interpolación de Newton con diferencias divididas."""
    n = len(x_points)
    if n != len(y_points):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")
    if n < 2:
        raise ValueError("Se necesitan al menos 2 puntos para interpolar.")
    if len(set(x_points)) != n:
        raise ValueError("Los valores de x no deben repetirse.")

    # Tabla de diferencias divididas
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = (
                (diff_table[i + 1][j - 1] - diff_table[i][j - 1])
                / (x_points[i + j] - x_points[i])
            )

    coefficients = diff_table[0, :].tolist()

    steps = [
        f"Puntos: {list(zip(x_points, y_points))}",
        f"Valor a interpolar: x = {x_eval}",
        "",
        "Tabla de diferencias divididas:",
    ]

    for j in range(n):
        steps.append(f"  Orden {j}: {[round(diff_table[i][j], 6) for i in range(n - j)]}")

    # Evaluar polinomio
    table = []
    result = coefficients[0]
    accumulated = result
    for i in range(n):
        coeff = coefficients[i]
        row = NewtonInterpRow(
            i=i, xi=round(x_points[i], 8), yi=round(y_points[i], 8),
            divided_diff=round(diff_table[0][i], 8) if i < n else 0.0,
            coefficient=round(coeff, 8),
            accumulated=round(accumulated, 8),
        )
        table.append(row)
        if i > 0:
            term = coeff
            for k in range(i):
                term *= (x_eval - x_points[k])
            accumulated += term
            steps.append(f"Término {i}: c{i}={coeff:.6f}, contribución={term:.6f}, acumulado={accumulated:.6f}")

    # Curva para gráfica
    x_min, x_max = min(x_points), max(x_points)
    margin = (x_max - x_min) * 0.2 if x_max > x_min else 1.0
    x_plot = np.linspace(x_min - margin, x_max + margin, 200).tolist()
    y_plot = []
    for xv in x_plot:
        val = coefficients[0]
        for i in range(1, n):
            term = coefficients[i]
            for k in range(i):
                term *= (xv - x_points[k])
            val += term
        y_plot.append(val)

    return InterpolationResult(
        polynomial_str=f"P(x) de grado {n-1} por Newton (diferencias divididas)",
        interpolated_value=round(accumulated, 10),
        table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"P({x_eval}) ≈ {accumulated:.10f}",
    )
