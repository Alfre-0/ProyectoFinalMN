"""
integracion_derivacion.py — Lógica pura para derivación e integración numérica.
Métodos: Diferencias Finitas, Trapecio, Simpson.
"""
from dataclasses import dataclass
import numpy as np
import sympy as sp


@dataclass(frozen=True)
class DiffFinitasRow:
    index: int
    xi: float
    fxi: float
    fxi_h: float
    approximation: float
    error: float


@dataclass(frozen=True)
class TrapecioRow:
    index: int
    dx: float
    xi: float
    fxi: float
    factor: int
    partial: float


@dataclass(frozen=True)
class SimpsonRow:
    index: int
    dx: float
    xi: float
    fxi: float
    factor: int
    partial: float


@dataclass(frozen=True)
class IntegrationResult:
    value: float
    table: list
    procedure_steps: list[str]
    x_plot: list[float]
    y_plot: list[float]
    message: str = ""


def _parse_function(expression_str: str):
    x = sp.Symbol("x")
    try:
        expr = sp.sympify(expression_str)
        func = sp.lambdify(x, expr, modules=["numpy"])
        return func, expr
    except (sp.SympifyError, TypeError) as error:
        raise ValueError(f"No se pudo interpretar la función: {expression_str}") from error


# ── Diferencias Finitas ────────────────────────────────────────────

def diferencias_finitas(func_str: str, x_point: float, h: float = 0.01,
                        method: str = "central") -> IntegrationResult:
    """
    Aproximación de la derivada por diferencias finitas.
    method: 'forward', 'backward', 'central'
    """
    func, expr = _parse_function(func_str)
    x_sym = sp.Symbol("x")
    exact_deriv = sp.diff(sp.sympify(func_str), x_sym)
    exact_func = sp.lambdify(x_sym, exact_deriv, modules=["numpy"])

    steps = [
        f"Función: f(x) = {expr}",
        f"Derivada simbólica: f'(x) = {exact_deriv}",
        f"Punto de evaluación: x = {x_point}",
        f"Paso h = {h}",
        f"Tipo: {method}",
        "",
    ]

    table = []
    exact_value = float(exact_func(x_point))

    # Calcular con distintos valores de h
    h_values = [h * (2 ** i) for i in range(5, -1, -1)]
    for idx, hi in enumerate(h_values):
        fxi = float(func(x_point))
        if method == "forward":
            fxi_h = float(func(x_point + hi))
            approx = (fxi_h - fxi) / hi
        elif method == "backward":
            fxi_h = float(func(x_point - hi))
            approx = (fxi - fxi_h) / hi
        else:  # central
            f_plus = float(func(x_point + hi))
            f_minus = float(func(x_point - hi))
            fxi_h = f_plus
            approx = (f_plus - f_minus) / (2 * hi)

        error = abs(approx - exact_value)
        row = DiffFinitasRow(
            index=idx + 1, xi=round(x_point, 8), fxi=round(fxi, 8),
            fxi_h=round(fxi_h, 8), approximation=round(approx, 8),
            error=round(error, 10),
        )
        table.append(row)
        steps.append(f"h={hi:.6f}: f'({x_point}) = {approx:.8f}, error = {error:.2e}")

    best = table[-1]

    # Datos para gráfica de la función y derivada
    x_plot = np.linspace(x_point - 3, x_point + 3, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    return IntegrationResult(
        value=best.approximation, table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=(f"f'({x_point}) = {best.approximation:.10f} "
                 f"(valor exacto: {exact_value:.10f}, error: {best.error:.2e})")
    )


# ── Regla del Trapecio ────────────────────────────────────────────

def trapecio(func_str: str, a: float, b: float,
             n_intervals: int = 10) -> IntegrationResult:
    """Integración numérica por la regla del Trapecio compuesta."""
    if n_intervals < 1:
        raise ValueError("El número de subintervalos debe ser ≥ 1.")

    func, expr = _parse_function(func_str)
    dx = (b - a) / n_intervals

    steps = [
        f"Función: f(x) = {expr}",
        f"Intervalo: [{a}, {b}]",
        f"Subintervalos: n = {n_intervals}",
        f"dx = {dx:.6f}",
        "",
    ]

    table = []
    total = 0.0
    for i in range(n_intervals + 1):
        xi = a + i * dx
        fxi = float(func(xi))
        factor = 1 if (i == 0 or i == n_intervals) else 2
        partial = (dx / 2) * factor * fxi
        total += partial

        row = TrapecioRow(
            index=i, dx=round(dx, 8), xi=round(xi, 8),
            fxi=round(fxi, 8), factor=factor, partial=round(partial, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={xi:.6f}, f(x)={fxi:.6f}, factor={factor}, "
            f"parcial={partial:.6f}"
        )

    steps.append(f"\nResultado: Int f(x)dx = {total:.10f}")

    x_plot = np.linspace(a, b, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    return IntegrationResult(
        value=round(total, 10), table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"Int [{a},{b}] f(x)dx = {total:.10f}"
    )


# ── Regla de Simpson ──────────────────────────────────────────────

def simpson(func_str: str, a: float, b: float,
            n_intervals: int = 10) -> IntegrationResult:
    """Integración numérica por la regla de Simpson 1/3 compuesta."""
    if n_intervals < 2:
        raise ValueError("El número de subintervalos debe ser ≥ 2.")
    if n_intervals % 2 != 0:
        raise ValueError("El número de subintervalos debe ser par para Simpson 1/3.")

    func, expr = _parse_function(func_str)
    dx = (b - a) / n_intervals

    steps = [
        f"Función: f(x) = {expr}",
        f"Intervalo: [{a}, {b}]",
        f"Subintervalos: n = {n_intervals} (par [OK])",
        f"dx = {dx:.6f}",
        "",
    ]

    table = []
    total = 0.0
    for i in range(n_intervals + 1):
        xi = a + i * dx
        fxi = float(func(xi))
        if i == 0 or i == n_intervals:
            factor = 1
        elif i % 2 == 1:
            factor = 4
        else:
            factor = 2
        partial = (dx / 3) * factor * fxi
        total += partial

        row = SimpsonRow(
            index=i, dx=round(dx, 8), xi=round(xi, 8),
            fxi=round(fxi, 8), factor=factor, partial=round(partial, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={xi:.6f}, f(x)={fxi:.6f}, factor={factor}, "
            f"parcial={partial:.6f}"
        )

    steps.append(f"\nResultado: Int f(x)dx = {total:.10f}")

    x_plot = np.linspace(a, b, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    return IntegrationResult(
        value=round(total, 10), table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"Int [{a},{b}] f(x)dx = {total:.10f}"
    )
