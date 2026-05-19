"""
edos.py — Lógica pura para resolución de ecuaciones diferenciales ordinarias.
Métodos: Euler y Runge-Kutta de 4to orden (RK4).
"""
from dataclasses import dataclass
import math
import numpy as np
import sympy as sp


# Umbral máximo absoluto de |y| antes de declarar divergencia.
# Funciones como dy/dx = 1+y² (solución = tan) explotan a infinito;
# este límite evita OverflowError de Python al intentar operar con floats enormes.
_DIVERGENCE_THRESHOLD = 1e12


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
    diverged: bool = False


def _parse_ode_function(expression_str: str):
    """Convierte un string f(x, y) en una función evaluable."""
    x_sym, y_sym = sp.symbols("x y")
    try:
        sanitized = expression_str.replace("^", "**")
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = standard_transformations + (implicit_multiplication_application,)
        expr = parse_expr(sanitized, transformations=transformations)
        
        # Validar variables permitidas
        allowed_symbols = {x_sym, y_sym}
        extra_symbols = expr.free_symbols - allowed_symbols
        if extra_symbols:
            names = ", ".join(str(s) for s in extra_symbols)
            raise ValueError(f"Variable(s) no permitida(s): {names}. Use únicamente 'x' e 'y'.")

        raw_func = sp.lambdify((x_sym, y_sym), expr, modules=["numpy"])

        # Wrapper que protege contra OverflowError y valores no finitos
        def safe_func(x_val, y_val):
            try:
                result = float(raw_func(x_val, y_val))
            except (OverflowError, FloatingPointError, ZeroDivisionError):
                return float('inf')
            if not math.isfinite(result):
                return float('inf')
            return result

        return safe_func, expr
    except Exception as error:
        if isinstance(error, ValueError):
            raise error
        raise ValueError(f"No se pudo interpretar la ecuación: {expression_str}") from error


def _is_diverged(value: float) -> bool:
    """Verifica si un valor ha superado el umbral de divergencia o es no finito."""
    if not math.isfinite(value):
        return True
    return abs(value) > _DIVERGENCE_THRESHOLD


def _safe_round(value: float, decimals: int) -> float:
    """Round que maneja inf/nan sin lanzar excepciones."""
    if not math.isfinite(value):
        return value
    return round(value, decimals)


def _safe_format(value: float, fmt: str = ".6f") -> str:
    """Formatea un float manejando inf/nan de forma legible."""
    if math.isinf(value):
        return "∞" if value > 0 else "-∞"
    if math.isnan(value):
        return "NaN"
    return f"{value:{fmt}}"


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
        f"dy/dx = {str(expr).replace('**', '^')}",
        f"Condición inicial: y({x0}) = {y0}",
        f"Intervalo: [{x0}, {x_final}]",
        f"Paso h = {h}",
        f"Número de pasos: {n_steps}",
        "",
    ]

    x_values = [x0]
    y_values = [y0]
    table = []
    diverged = False

    xi, yi = x0, y0
    for i in range(n_steps):
        fxy = func(xi, yi)

        # Detectar divergencia antes de que Python lance OverflowError
        if _is_diverged(fxy) or _is_diverged(yi):
            steps.append(
                f"⚠ DIVERGENCIA en i={i}: x={_safe_format(xi)}, "
                f"y={_safe_format(yi)}, f(x,y)={_safe_format(fxy)}"
            )
            steps.append("")
            steps.append(
                "La solución diverge (tiende a infinito) en este punto. "
                "Esto es normal para EDOs cuya solución tiene asíntotas "
                "verticales (ej: dy/dx = 1+y² → y = tan(x+C))."
            )
            steps.append(
                "Sugerencia: reduzca el intervalo [x₀, x_final] o "
                "use un paso h más pequeño."
            )
            diverged = True
            break

        yi_next = yi + h * fxy
        xi_next = xi + h
        error = abs(yi_next - yi) if i > 0 else 0.0

        row = EulerRow(
            iteration=i, xi=_safe_round(xi, 8), yi=_safe_round(yi, 8),
            fxy=_safe_round(fxy, 8), yi_next=_safe_round(yi_next, 8),
            error=_safe_round(error, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={_safe_format(xi)}, y={_safe_format(yi)}, "
            f"f(x,y)={_safe_format(fxy)}, y_next={_safe_format(yi_next)}"
        )

        xi = xi_next
        yi = yi_next
        x_values.append(_safe_round(xi, 10))
        y_values.append(_safe_round(yi, 10))

    if diverged:
        msg = (
            f"⚠ La solución diverge cerca de x = {_safe_format(xi)}. "
            f"Se completaron {len(table)} de {n_steps} pasos antes de la divergencia."
        )
    else:
        msg = f"y({x_final}) = {_safe_format(y_values[-1], '.10f')} (Euler, {n_steps} pasos)"

    return ODEResult(
        x_values=x_values, y_values=y_values, table=table,
        procedure_steps=steps, message=msg, diverged=diverged,
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
        f"dy/dx = {str(expr).replace('**', '^')}",
        f"Condición inicial: y({x0}) = {y0}",
        f"Intervalo: [{x0}, {x_final}]",
        f"Paso h = {h}",
        f"Número de pasos: {n_steps}",
        "",
    ]

    x_values = [x0]
    y_values = [y0]
    table = []
    diverged = False

    xi, yi = x0, y0
    for i in range(n_steps):
        # Verificar divergencia antes de calcular k-values
        if _is_diverged(yi):
            steps.append(
                f"⚠ DIVERGENCIA en i={i}: x={_safe_format(xi)}, "
                f"y={_safe_format(yi)}"
            )
            steps.append("")
            steps.append(
                "La solución diverge (tiende a infinito) en este punto. "
                "Esto es normal para EDOs cuya solución tiene asíntotas "
                "verticales (ej: dy/dx = 1+y² → y = tan(x+C))."
            )
            steps.append(
                "Sugerencia: reduzca el intervalo [x₀, x_final] o "
                "use un paso h más pequeño."
            )
            diverged = True
            break

        k1 = h * func(xi, yi)
        k2 = h * func(xi + h / 2, yi + k1 / 2)
        k3 = h * func(xi + h / 2, yi + k2 / 2)
        k4 = h * func(xi + h, yi + k3)

        # Verificar si algún k divergió
        if any(_is_diverged(k) for k in (k1, k2, k3, k4)):
            steps.append(
                f"⚠ DIVERGENCIA en i={i}: x={_safe_format(xi)}, "
                f"y={_safe_format(yi)}, algún k-value → ∞"
            )
            steps.append("")
            steps.append(
                "La solución diverge (tiende a infinito) en este punto. "
                "Esto es normal para EDOs cuya solución tiene asíntotas "
                "verticales (ej: dy/dx = 1+y² → y = tan(x+C))."
            )
            steps.append(
                "Sugerencia: reduzca el intervalo [x₀, x_final] o "
                "use un paso h más pequeño."
            )
            diverged = True
            break

        yi_next = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        xi_next = xi + h
        error = abs(yi_next - yi) if i > 0 else 0.0

        row = RungeKuttaRow(
            iteration=i, xi=_safe_round(xi, 8), yi=_safe_round(yi, 8),
            k1=_safe_round(k1, 8), k2=_safe_round(k2, 8),
            k3=_safe_round(k3, 8), k4=_safe_round(k4, 8),
            yi_next=_safe_round(yi_next, 8), error=_safe_round(error, 8),
        )
        table.append(row)
        steps.append(
            f"i={i}: x={_safe_format(xi)}, y={_safe_format(yi)}, "
            f"k1={_safe_format(k1)}, k2={_safe_format(k2)}, "
            f"k3={_safe_format(k3)}, k4={_safe_format(k4)}, "
            f"y_next={_safe_format(yi_next)}"
        )

        xi = xi_next
        yi = yi_next
        x_values.append(_safe_round(xi, 10))
        y_values.append(_safe_round(yi, 10))

    if diverged:
        msg = (
            f"⚠ La solución diverge cerca de x = {_safe_format(xi)}. "
            f"Se completaron {len(table)} de {n_steps} pasos antes de la divergencia."
        )
    else:
        msg = f"y({x_final}) = {_safe_format(y_values[-1], '.10f')} (RK4, {n_steps} pasos)"

    return ODEResult(
        x_values=x_values, y_values=y_values, table=table,
        procedure_steps=steps, message=msg, diverged=diverged,
    )
