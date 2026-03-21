"""
raices.py — Lógica pura para cálculo de raíces.
Retorna dataclasses inmutables con los pasos y el resultado.
NO contiene ninguna referencia a PyQt6 ni UI.
"""
from dataclasses import dataclass, field
import numpy as np
import sympy as sp


# ── Estructuras de resultado inmutables ────────────────────────────

@dataclass(frozen=True)
class BiseccionRow:
    iteration: int
    a: float
    c: float
    b: float
    fa: float
    fc: float
    fb: float
    error: float


@dataclass(frozen=True)
class NewtonRaphsonRow:
    iteration: int
    xn: float
    fxn: float
    fpxn: float
    xn1: float
    fxn1: float
    error: float


@dataclass(frozen=True)
class SecanteRow:
    iteration: int
    xn_prev: float
    xn: float
    fxn_prev: float
    fxn: float
    xn1: float
    error: float


@dataclass(frozen=True)
class RootResult:
    root: float
    iterations: int
    error: float
    converged: bool
    table: list
    procedure_steps: list[str]
    message: str = ""


# ── Utilidad para parsear funciones ────────────────────────────────

def _parse_function(expression_str: str):
    """Convierte un string a una función numérica evaluable."""
    x = sp.Symbol("x")
    try:
        expr = sp.sympify(expression_str)
        func = sp.lambdify(x, expr, modules=["numpy"])
        return func, expr
    except (sp.SympifyError, TypeError) as error:
        raise ValueError(f"No se pudo interpretar la función: {expression_str}") from error


# ── Bisección ──────────────────────────────────────────────────────

def biseccion(func_str: str, a: float, b: float,
              tolerance: float = 1e-6, max_iterations: int = 100) -> RootResult:
    """
    Método de Bisección para encontrar raíces.
    Requiere que f(a) * f(b) < 0 (cambio de signo).
    """
    func, expr = _parse_function(func_str)
    fa = float(func(a))
    fb = float(func(b))

    if fa * fb > 0:
        raise ValueError(
            f"No hay cambio de signo en [{a}, {b}]. "
            f"f({a})={fa:.6f}, f({b})={fb:.6f}. "
            "El método de Bisección requiere que f(a)·f(b) < 0."
        )

    table = []
    steps = [
        f"Función: f(x) = {expr}",
        f"Intervalo inicial: [{a}, {b}]",
        f"Tolerancia: {tolerance}",
        f"f({a}) = {fa:.6f}, f({b}) = {fb:.6f}",
        "Se verifica cambio de signo [OK]",
        "",
    ]

    error = abs(b - a)
    for i in range(1, max_iterations + 1):
        c = (a + b) / 2.0
        fc = float(func(c))
        fa_current = float(func(a))
        fb_current = float(func(b))

        row = BiseccionRow(
            iteration=i, a=round(a, 8), c=round(c, 8), b=round(b, 8),
            fa=round(fa_current, 8), fc=round(fc, 8), fb=round(fb_current, 8),
            error=round(error, 8),
        )
        table.append(row)
        steps.append(
            f"Iteración {i}: a={a:.6f}, c={c:.6f}, b={b:.6f}, "
            f"f(c)={fc:.6f}, error={error:.6e}"
        )

        if abs(fc) < tolerance or error < tolerance:
            return RootResult(
                root=round(c, 10), iterations=i, error=round(error, 10),
                converged=True, table=table, procedure_steps=steps,
                message=f"Raíz encontrada: x = {c:.10f} con error {error:.2e} en {i} iteraciones."
            )

        if fa_current * fc < 0:
            b = c
        else:
            a = c
        error = abs(b - a)

    c = (a + b) / 2.0
    return RootResult(
        root=round(c, 10), iterations=max_iterations,
        error=round(error, 10), converged=False, table=table,
        procedure_steps=steps,
        message=f"No convergió en {max_iterations} iteraciones. Última aproximación: x = {c:.10f}"
    )


# ── Newton-Raphson ─────────────────────────────────────────────────

def newton_raphson(func_str: str, deriv_str: str, x0: float,
                   tolerance: float = 1e-6, max_iterations: int = 100) -> RootResult:
    """
    Método de Newton-Raphson.
    Requiere la función y su derivada.
    """
    func, expr = _parse_function(func_str)
    deriv, deriv_expr = _parse_function(deriv_str)

    table = []
    steps = [
        f"Función: f(x) = {expr}",
        f"Derivada: f'(x) = {deriv_expr}",
        f"Valor inicial: x0 = {x0}",
        f"Tolerancia: {tolerance}",
        "",
    ]

    xn = x0
    for i in range(1, max_iterations + 1):
        fxn = float(func(xn))
        fpxn = float(deriv(xn))

        if abs(fpxn) < 1e-14:
            raise ValueError(
                f"Derivada prácticamente cero en x = {xn:.6f}. "
                "El método diverge. Intente otro valor inicial."
            )

        xn1 = xn - fxn / fpxn
        fxn1 = float(func(xn1))
        error = abs(xn1 - xn)

        row = NewtonRaphsonRow(
            iteration=i, xn=round(xn, 8), fxn=round(fxn, 8),
            fpxn=round(fpxn, 8), xn1=round(xn1, 8),
            fxn1=round(fxn1, 8), error=round(error, 8),
        )
        table.append(row)
        steps.append(
            f"Iteración {i}: x{i-1}={xn:.6f}, f(x)={fxn:.6f}, "
            f"f'(x)={fpxn:.6f}, x{i}={xn1:.6f}, error={error:.6e}"
        )

        if error < tolerance or abs(fxn1) < tolerance:
            return RootResult(
                root=round(xn1, 10), iterations=i, error=round(error, 10),
                converged=True, table=table, procedure_steps=steps,
                message=f"Raíz encontrada: x = {xn1:.10f} con error {error:.2e} en {i} iteraciones."
            )
        xn = xn1

    return RootResult(
        root=round(xn, 10), iterations=max_iterations,
        error=round(abs(float(func(xn))), 10), converged=False,
        table=table, procedure_steps=steps,
        message=f"No convergió en {max_iterations} iteraciones. Última aproximación: x = {xn:.10f}"
    )


# ── Secante ────────────────────────────────────────────────────────

def secante(func_str: str, x0: float, x1: float,
            tolerance: float = 1e-6, max_iterations: int = 100) -> RootResult:
    """Método de la Secante — no requiere derivada."""
    func, expr = _parse_function(func_str)

    if abs(x0 - x1) < 1e-14:
        raise ValueError("Los dos valores iniciales deben ser distintos.")

    table = []
    steps = [
        f"Función: f(x) = {expr}",
        f"Valores iniciales: x0 = {x0}, x1 = {x1}",
        f"Tolerancia: {tolerance}",
        "",
    ]

    for i in range(1, max_iterations + 1):
        fx0 = float(func(x0))
        fx1 = float(func(x1))
        denominator = fx1 - fx0

        if abs(denominator) < 1e-14:
            raise ValueError(
                f"f(x{i-1}) ≈ f(x{i}), el denominador es ~0. Método diverge."
            )

        x2 = x1 - fx1 * (x1 - x0) / denominator
        error = abs(x2 - x1)

        row = SecanteRow(
            iteration=i, xn_prev=round(x0, 8), xn=round(x1, 8),
            fxn_prev=round(fx0, 8), fxn=round(fx1, 8),
            xn1=round(x2, 8), error=round(error, 8),
        )
        table.append(row)
        steps.append(
            f"Iteración {i}: x(n-1)={x0:.6f}, x(n)={x1:.6f}, "
            f"f(xn-1)={fx0:.6f}, f(xn)={fx1:.6f}, x(n+1)={x2:.6f}, error={error:.6e}"
        )

        if error < tolerance:
            return RootResult(
                root=round(x2, 10), iterations=i, error=round(error, 10),
                converged=True, table=table, procedure_steps=steps,
                message=f"Raíz encontrada: x = {x2:.10f} con error {error:.2e} en {i} iteraciones."
            )
        x0, x1 = x1, x2

    return RootResult(
        root=round(x1, 10), iterations=max_iterations,
        error=round(abs(float(func(x1))), 10), converged=False,
        table=table, procedure_steps=steps,
        message=f"No convergió en {max_iterations} iteraciones. Última aproximación: x = {x1:.10f}"
    )
