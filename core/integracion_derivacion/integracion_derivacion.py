"""
integracion_derivacion.py — Lógica pura para derivación e integración numérica.
Métodos: Diferencias Finitas, Trapecio, Simpson.
"""
from dataclasses import dataclass
import numpy as np
import sympy as sp


@dataclass(frozen=True)
class PuntoMedioRow:
    index: int
    xi: float
    xi_plus_1: float
    x_mid: float
    f_x_mid: float
    area_i: float


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
    rectangles: list[dict] = None


def _parse_function(expression_str: str):
    x = sp.Symbol("x")
    try:
        sanitized = expression_str.replace("^", "**")
        expr = sp.sympify(sanitized)
        func = sp.lambdify(x, expr, modules=["numpy"])
        return func, expr
    except (sp.SympifyError, TypeError) as error:
        raise ValueError(f"No se pudo interpretar la función: {expression_str}") from error


# ── Regla del Punto Medio ──────────────────────────────────────────

def punto_medio(func_str: str, a: float, b: float, n_intervals: int) -> IntegrationResult:
    """Integración numérica por la regla del Punto Medio (Área bajo la curva)."""
    if n_intervals < 1:
        raise ValueError("El número de rectángulos (n) debe ser ≥ 1.")

    func, expr = _parse_function(func_str)
    dx = (b - a) / n_intervals

    steps = [
        f"Función: f(x) = {str(expr).replace('**', '^')}",
        f"Intervalo: [{a}, {b}]",
        f"Rectángulos (n): {n_intervals}",
        f"Δx = ({b} - {a}) / {n_intervals} = {dx:.6f}",
        "",
    ]

    table = []
    rectangles = []
    total_area = 0.0

    for i in range(n_intervals):
        xi = a + i * dx
        xi_plus_1 = a + (i + 1) * dx
        x_mid = (xi + xi_plus_1) / 2.0
        f_x_mid = float(func(x_mid))
        area_i = f_x_mid * dx

        total_area += area_i

        row = PuntoMedioRow(
            index=i + 1,
            xi=round(xi, 8),
            xi_plus_1=round(xi_plus_1, 8),
            x_mid=round(x_mid, 8),
            f_x_mid=round(f_x_mid, 8),
            area_i=round(area_i, 8)
        )
        table.append(row)

        rectangles.append({
            "x_left": xi,
            "x_mid": x_mid,
            "width": dx,
            "height": f_x_mid
        })

        steps.append(
            f"i={i+1}: Xi={xi:.4f}, Xi+1={xi_plus_1:.4f}, X̄={x_mid:.4f}, "
            f"f(X̄)={f_x_mid:.4f}, Área={area_i:.4f}"
        )

    steps.append("")
    steps.append(f"Resultado: Área Total ≈ {total_area:.10f}")

    margin = abs(b - a) * 0.1 if a != b else 1.0
    x_plot = np.linspace(a - margin, b + margin, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    return IntegrationResult(
        value=total_area, table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"Área Total bajo la curva ≈ {total_area:.10f}",
        rectangles=rectangles
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
        f"Función: f(x) = {str(expr).replace('**', '^')}",
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
        f"Función: f(x) = {str(expr).replace('**', '^')}",
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
