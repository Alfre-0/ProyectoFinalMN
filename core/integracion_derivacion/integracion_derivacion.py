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
    parabolas: list[dict] = None


def _parse_function(expression_str: str):
    x = sp.Symbol("x")
    try:
        sanitized = expression_str.replace("^", "**")
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = standard_transformations + (implicit_multiplication_application,)
        expr = parse_expr(sanitized, transformations=transformations)
        
        # Validar variables permitidas
        allowed_symbols = {x}
        extra_symbols = expr.free_symbols - allowed_symbols
        if extra_symbols:
            names = ", ".join(str(s) for s in extra_symbols)
            raise ValueError(f"Variable(s) no permitida(s): {names}. Use únicamente 'x'.")

        raw_func = sp.lambdify(x, expr, modules=["numpy"])

        # Wrapper que protege contra OverflowError y valores no finitos
        def safe_func(x_val):
            try:
                return float(raw_func(x_val))
            except (OverflowError, FloatingPointError, ZeroDivisionError):
                return float('nan')

        return safe_func, expr
    except Exception as error:
        if isinstance(error, ValueError):
            raise error
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

    # Construir parábolas de interpolación verdaderas para la gráfica
    parabolas = []
    for i in range(0, n_intervals, 2):
        x0 = a + i * dx
        x1 = a + (i + 1) * dx
        x2 = a + (i + 2) * dx
        y0, y1, y2 = float(func(x0)), float(func(x1)), float(func(x2))

        # Evitar divisiones por cero por flotantes
        d0 = (x0 - x1) * (x0 - x2)
        d1 = (x1 - x0) * (x1 - x2)
        d2 = (x2 - x0) * (x2 - x1)

        px = np.linspace(x0, x2, 25).tolist()
        py = []
        for xv in px:
            val = 0.0
            if d0 != 0: val += y0 * (xv - x1) * (xv - x2) / d0
            if d1 != 0: val += y1 * (xv - x0) * (xv - x2) / d1
            if d2 != 0: val += y2 * (xv - x0) * (xv - x1) / d2
            py.append(val)
        
        parabolas.append({"x": px, "y": py})

    steps.append(f"\nResultado: Int f(x)dx = {total:.10f}")

    margin = abs(b - a) * 0.1 if a != b else 1.0
    x_plot = np.linspace(a - margin, b + margin, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    return IntegrationResult(
        value=round(total, 10), table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=f"Int [{a},{b}] f(x)dx = {total:.10f}",
        parabolas=parabolas
    )


# ── Derivación Numérica (Diferencias Finitas) ─────────────────────

@dataclass(frozen=True)
class DerivationRow:
    node: str
    x: float
    fx: float


@dataclass(frozen=True)
class DerivationResult:
    value: float
    table: list[DerivationRow]
    procedure_steps: list[str]
    x_plot: list[float]
    y_plot: list[float]
    x_tangent: list[float] | None = None
    y_tangent: list[float] | None = None
    message: str = ""


def diferencias_finitas(func_str: str, x0: float, h: float,
                        order: int, direction: str) -> DerivationResult:
    """Aproximación de la 1ra o 2da derivada de f(x) en x0 usando Diferencias Finitas."""
    if h <= 0:
        raise ValueError("El paso h debe ser positivo y mayor que cero.")

    func, expr = _parse_function(func_str)
    direction = direction.lower().strip()

    # Puntos necesarios dependiendo del orden y la dirección
    # f(x0) siempre se evalúa
    fx0 = float(func(x0))
    table = []

    steps = [
        f"Función f(x) = {str(expr).replace('**', '^')}",
        f"Punto de evaluación x₀ = {x0}",
        f"Punto f(x₀) = {fx0:.8f}",
        f"Paso h = {h}",
        f"Orden de la derivada: {order}ª derivada",
        f"Dirección de diferencias: {direction.capitalize()}",
        "",
    ]

    # Evaluaciones
    nodes_eval = {}
    
    if order == 1:
        if direction == "adelante":
            # f'(x) ≈ (f(x0+h) - f(x0)) / h
            fx_plus_h = float(func(x0 + h))
            nodes_eval["x₀"] = (x0, fx0)
            nodes_eval["x₀ + h"] = (x0 + h, fx_plus_h)
            
            value = (fx_plus_h - fx0) / h
            
            formula_str = "f'(x₀) ≈ [f(x₀ + h) - f(x₀)] / h"
            calc_str = f"f'({x0}) ≈ [{fx_plus_h:.8f} - {fx0:.8f}] / {h} = {value:.10f}"
            
        elif direction == "atrás":
            # f'(x) ≈ (f(x0) - f(x0-h)) / h
            fx_minus_h = float(func(x0 - h))
            nodes_eval["x₀ - h"] = (x0 - h, fx_minus_h)
            nodes_eval["x₀"] = (x0, fx0)
            
            value = (fx0 - fx_minus_h) / h
            
            formula_str = "f'(x₀) ≈ [f(x₀) - f(x₀ - h)] / h"
            calc_str = f"f'({x0}) ≈ [{fx0:.8f} - {fx_minus_h:.8f}] / {h} = {value:.10f}"
            
        else:  # central
            # f'(x) ≈ (f(x0+h) - f(x0-h)) / 2h
            fx_plus_h = float(func(x0 + h))
            fx_minus_h = float(func(x0 - h))
            nodes_eval["x₀ - h"] = (x0 - h, fx_minus_h)
            nodes_eval["x₀"] = (x0, fx0)
            nodes_eval["x₀ + h"] = (x0 + h, fx_plus_h)
            
            value = (fx_plus_h - fx_minus_h) / (2 * h)
            
            formula_str = "f'(x₀) ≈ [f(x₀ + h) - f(x₀ - h)] / (2h)"
            calc_str = f"f'({x0}) ≈ [{fx_plus_h:.8f} - {fx_minus_h:.8f}] / {2*h} = {value:.10f}"
            
    elif order == 2:
        if direction == "adelante":
            # f''(x) ≈ (f(x0+2h) - 2f(x0+h) + f(x0)) / h^2
            fx_plus_h = float(func(x0 + h))
            fx_plus_2h = float(func(x0 + 2 * h))
            nodes_eval["x₀"] = (x0, fx0)
            nodes_eval["x₀ + h"] = (x0 + h, fx_plus_h)
            nodes_eval["x₀ + 2h"] = (x0 + 2 * h, fx_plus_2h)
            
            value = (fx_plus_2h - 2 * fx_plus_h + fx0) / (h ** 2)
            
            formula_str = "f''(x₀) ≈ [f(x₀ + 2h) - 2f(x₀ + h) + f(x₀)] / h²"
            calc_str = f"f''({x0}) ≈ [{fx_plus_2h:.8f} - 2*({fx_plus_h:.8f}) + {fx0:.8f}] / {h**2} = {value:.10f}"
            
        elif direction == "atrás":
            # f''(x) ≈ (f(x0) - 2f(x0-h) + f(x0-2h)) / h^2
            fx_minus_h = float(func(x0 - h))
            fx_minus_2h = float(func(x0 - 2 * h))
            nodes_eval["x₀ - 2h"] = (x0 - 2 * h, fx_minus_2h)
            nodes_eval["x₀ - h"] = (x0 - h, fx_minus_h)
            nodes_eval["x₀"] = (x0, fx0)
            
            value = (fx0 - 2 * fx_minus_h + fx_minus_2h) / (h ** 2)
            
            formula_str = "f''(x₀) ≈ [f(x₀) - 2f(x₀ - h) + f(x₀ - 2h)] / h²"
            calc_str = f"f''({x0}) ≈ [{fx0:.8f} - 2*({fx_minus_h:.8f}) + {fx_minus_2h:.8f}] / {h**2} = {value:.10f}"
            
        else:  # central
            # f''(x) ≈ (f(x0+h) - 2f(x0) + f(x0-h)) / h^2
            fx_plus_h = float(func(x0 + h))
            fx_minus_h = float(func(x0 - h))
            nodes_eval["x₀ - h"] = (x0 - h, fx_minus_h)
            nodes_eval["x₀"] = (x0, fx0)
            nodes_eval["x₀ + h"] = (x0 + h, fx_plus_h)
            
            value = (fx_plus_h - 2 * fx0 + fx_minus_h) / (h ** 2)
            
            formula_str = "f''(x₀) ≈ [f(x₀ + h) - 2f(x₀) + f(x₀ - h)] / h²"
            calc_str = f"f''({x0}) ≈ [{fx_plus_h:.8f} - 2*({fx0:.8f}) + {fx_minus_h:.8f}] / {h**2} = {value:.10f}"
    else:
        raise ValueError("El orden de la derivada debe ser 1 (Primera) o 2 (Segunda).")

    # Guardar pasos en procedure_steps
    steps.append("Fórmula utilizada:")
    steps.append(f"  {formula_str}")
    steps.append("")
    steps.append("Valores calculados:")
    for lbl, (xv, yv) in sorted(nodes_eval.items(), key=lambda t: t[1][0]):
        steps.append(f"  f({lbl}) = f({xv:.4f}) = {yv:.8f}")
        table.append(DerivationRow(node=lbl, x=round(xv, 8), fx=round(yv, 8)))

    steps.append("")
    steps.append("Sustitución y cálculo:")
    steps.append(f"  {calc_str}")

    # Coordenadas de graficación
    margin = 5.0 * h
    x_plot = np.linspace(x0 - margin, x0 + margin, 200).tolist()
    y_plot = [float(func(xv)) for xv in x_plot]

    # Calcular recta tangente o secante para graficar (solo primera derivada)
    x_tangent, y_tangent = None, None
    if order == 1:
        x_tangent = np.linspace(x0 - 2 * h, x0 + 2 * h, 10).tolist()
        y_tangent = [fx0 + value * (xv - x0) for xv in x_tangent]

    sign = "'" if order == 1 else "''"
    return DerivationResult(
        value=round(value, 10), table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        x_tangent=x_tangent, y_tangent=y_tangent,
        message=f"f{sign}({x0}) ≈ {value:.10f}"
    )
