"""
edos.py — Lógica pura para resolución de ecuaciones diferenciales ordinarias.
Métodos: Euler y Runge-Kutta de 4to orden (RK4).
"""
from dataclasses import dataclass
import numpy as np
import sympy as sp


@dataclass(frozen=True)
class EulerRow:
    iteration: int
    xi: float
    yi: float
    fxy: float
    yi_next: float
    error: float


@dataclass(frozen=True)
class RungeKuttaRow:
    iteration: int
    xi: float
    yi: float
    k1: float
    k2: float
    k3: float
    k4: float
    yi_next: float
    error: float


@dataclass(frozen=True)
class ODEResult:
    x_values: list[float]
    y_values: list[float]
    table: list
    procedure_steps: list[str]
    message: str = ""


def _parse_ode_function(expression_str: str):
    """Convierte un string f(x, y) en una función evaluable."""
    x_sym, y_sym = sp.symbols("x y")
    try:
        expr = sp.sympify(expression_str)
        func = sp.lambdify((x_sym, y_sym), expr, modules=["numpy"])
        return func, expr
    except (sp.SympifyError, TypeError) as error:
        raise ValueError(f"No se pudo interpretar la ecuación: {expression_str}") from error


# ── Método de Euler ────────────────────────────────────────────────

def euler(func_str: str, x0: float, y0: float,
          x_final: float, h: float) -> ODEResult:
    """Método de Euler para dy/dx = f(x, y) con condición inicial y(x0) = y0."""
    if h <= 0:
        raise ValueError("El paso h debe ser positivo y mayor que cero.")
    if x_final <= x0:
        raise ValueError("x_final debe ser mayor que x0.")

    func, expr = _parse_ode_function(func_str)
    n_steps = int(np.ceil((x_final - x0) / h))

    steps = [
        f"dy/dx = {expr}",
        f"Condición inicial: y({x0}) = {y0}",
        f"Intervalo: [{x0}, {x_final}]",
        f"Paso h = {h}",
        f"Número de pasos: {n_steps}",
        "",
    ]

    x_values = [x0]
    y_values = [y0]
    table = []

    xi, yi = x0, y0
    for i in range(n_steps):
        fxy = float(func(xi, yi))
        yi_next = yi + h * fxy
        xi_next = xi + h

        error = abs(yi_next - yi) if i > 0 else 0.0

        row = EulerRow(
            iteration=i, xi=round(xi, 8), yi=round(yi, 8),
            fxy=round(fxy, 8), yi_next=round(yi_next, 8),
            error=round(error, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={xi:.6f}, y={yi:.6f}, f(x,y)={fxy:.6f}, "
            f"y_next={yi_next:.6f}"
        )

        xi = xi_next
        yi = yi_next
        x_values.append(round(xi, 10))
        y_values.append(round(yi, 10))

    return ODEResult(
        x_values=x_values, y_values=y_values, table=table,
        procedure_steps=steps,
        message=f"y({x_final}) ≈ {y_values[-1]:.10f} (Euler, {n_steps} pasos)"
    )


# ── Runge-Kutta 4to Orden ─────────────────────────────────────────

def runge_kutta_4(func_str: str, x0: float, y0: float,
                  x_final: float, h: float) -> ODEResult:
    """Método de Runge-Kutta de 4to orden (RK4) para dy/dx = f(x, y)."""
    if h <= 0:
        raise ValueError("El paso h debe ser positivo y mayor que cero.")
    if x_final <= x0:
        raise ValueError("x_final debe ser mayor que x0.")

    func, expr = _parse_ode_function(func_str)
    n_steps = int(np.ceil((x_final - x0) / h))

    steps = [
        f"dy/dx = {expr}",
        f"Condición inicial: y({x0}) = {y0}",
        f"Intervalo: [{x0}, {x_final}]",
        f"Paso h = {h}",
        f"Número de pasos: {n_steps}",
        "",
    ]

    x_values = [x0]
    y_values = [y0]
    table = []

    xi, yi = x0, y0
    for i in range(n_steps):
        k1 = h * float(func(xi, yi))
        k2 = h * float(func(xi + h / 2, yi + k1 / 2))
        k3 = h * float(func(xi + h / 2, yi + k2 / 2))
        k4 = h * float(func(xi + h, yi + k3))

        yi_next = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        xi_next = xi + h
        error = abs(yi_next - yi) if i > 0 else 0.0

        row = RungeKuttaRow(
            iteration=i, xi=round(xi, 8), yi=round(yi, 8),
            k1=round(k1, 8), k2=round(k2, 8),
            k3=round(k3, 8), k4=round(k4, 8),
            yi_next=round(yi_next, 8), error=round(error, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={xi:.6f}, y={yi:.6f}, k1={k1:.6f}, k2={k2:.6f}, "
            f"k3={k3:.6f}, k4={k4:.6f}, y_next={yi_next:.6f}"
        )

        xi = xi_next
        yi = yi_next
        x_values.append(round(xi, 10))
        y_values.append(round(yi, 10))

    return ODEResult(
        x_values=x_values, y_values=y_values, table=table,
        procedure_steps=steps,
        message=f"y({x_final}) ≈ {y_values[-1]:.10f} (RK4, {n_steps} pasos)"
    )
