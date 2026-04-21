"""
interpolacion.py — Lógica pura para interpolación polinómica.
Métodos de Lagrange y Newton con diferencias divididas.
"""
from dataclasses import dataclass, field
import numpy as np
import sympy as sp
import re


def format_poly(expr, num_digits):
    """Redondea coeficientes (quita .0 inoficiosos) y formatea la expresión para la vista."""
    def format_num(n):
        r = round(float(n), num_digits)
        return int(r) if r == int(r) else r
        
    if isinstance(expr, (int, float, np.floating, np.integer)):
        return str(format_num(expr))
        
    expr = expr.xreplace({n: format_num(n) for n in expr.atoms(sp.Number)})
    s = str(expr)
    s = s.replace("**", "^")
    s = s.replace("*", "")
    return s


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
    polynomial_math: str
    interpolated_value: float | None
    table: list
    procedure_steps: list[str]
    x_plot: list[float]
    y_plot: list[float]
    message: str = ""


# ── Lagrange ───────────────────────────────────────────────────────

def lagrange(x_points: list[float], y_points: list[float],
             x_eval: float | None = None) -> InterpolationResult:
    """Interpolación de Lagrange."""
    n = len(x_points)
    if n != len(y_points):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")
    if n < 2:
        raise ValueError("Se necesitan al menos 2 puntos para interpolar.")
    if len(set(x_points)) != n:
        raise ValueError("Los valores de x no deben repetirse.")

    table = []
    x_sym = sp.Symbol('x')
    poly_expr = 0

    steps = [
        "PASO 1: Identificar los datos",
        f"Tenemos {n} puntos, por lo tanto:",
        f"  • n = {n} puntos",
        f"  • El polinomio será de grado n - 1 = {n - 1}",
    ]
    for i in range(n):
        steps.append(f"  • x_{i} = {x_points[i]},  y_{i} = {y_points[i]}")

    steps.extend([
        "",
        "PASO 2: Fórmula general del polinomio de Lagrange",
        f"Para n = {n} (grado {n-1}):",
        f"  P(x) = " + " + ".join([f"y_{i}L_{i}(x)" for i in range(n)]),
        "",
    ])

    accumulated = 0.0
    step_num = 3
    L_polys = []
    L_syms = []

    for i in range(n):
        li_val = 1.0 if x_eval is not None else None
        li_sym = 1.0
        
        num_gen = []
        den_gen = []
        num_sub = []
        den_sub = []
        den_evals = []
        den_val = 1.0

        for j in range(n):
            if i != j:
                num_gen.append(f"(x - x_{j})")
                den_gen.append(f"(x_{i} - x_{j})")
                num_sub.append(f"(x - {x_points[j]})")
                den_sub.append(f"({x_points[i]} - {x_points[j]})")
                diff = x_points[i] - x_points[j]
                den_evals.append(f"    ({x_points[i]} - {x_points[j]}) = {diff}")
                den_val *= diff

                if x_eval is not None:
                    li_val *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
                li_sym *= (x_sym - x_points[j]) / (x_points[i] - x_points[j])
        
        poly_expr += y_points[i] * li_sym
        L_syms.append(li_sym)

        # Pasos del L_i(x)
        steps.append(f"PASO {step_num}: Calcular el polinomio base L_{i}(x)")
        step_num += 1
        steps.append(f"Para i = {i}, excluimos j = {i}:")
        steps.append(f"  L_{i}(x) = {''.join(num_gen)} / {''.join(den_gen)}")
        steps.append("Sustituimos:")
        steps.append(f"  L_{i}(x) = {''.join(num_sub)} / {''.join(den_sub)}")
        steps.append("Desarrollamos el denominador:")
        steps.extend(den_evals)
        steps.append(f"    Multiplicación: {den_val}")
        
        num_sym = sp.expand(sp.prod([x_sym - x_points[j] for j in range(n) if i != j]))
        L_i_math = format_poly(num_sym, 5)
        L_i_final = f"({L_i_math}) / {den_val}"
        steps.append("Por lo tanto:")
        steps.append(f"  L_{i}(x) = {L_i_final}")
        steps.append("")
        L_polys.append(L_i_final)

        # Tablas y acumulado numérico de LagrangeRow (omita pasos numéricos en procedimiento)
        if x_eval is not None:
            term = y_points[i] * li_val
            accumulated += term
            row = LagrangeRow(
                i=i, xi=round(x_points[i], 8), yi=round(y_points[i], 8),
                li_value=round(li_val, 8), term=round(term, 8),
                accumulated=round(accumulated, 8),
            )
            table.append(row)
        else:
            row = LagrangeRow(
                i=i, xi=round(x_points[i], 8), yi=round(y_points[i], 8),
                li_value=0.0, term=0.0, accumulated=0.0,
            )
            table.append(row)

    steps.append(f"PASO {step_num}: Construir el polinomio interpolante")
    step_num += 1
    terms_sub = []
    for i in range(n):
        terms_sub.append(f"{y_points[i]} * [{L_polys[i]}]")
    steps.append(f"  P(x) = " + " + ".join(terms_sub))
    steps.append("")
    
    steps.append(f"PASO {step_num}: Desarrollar cada término")
    step_num += 1
    for i in range(n):
        term_expanded = format_poly(sp.expand(y_points[i] * L_syms[i]), 5)
        steps.append(f"Término {i+1}: {y_points[i]} * [{L_polys[i]}]")
        steps.append(f"  = {term_expanded}")
        steps.append("")

    poly_simplified = sp.simplify(poly_expr)
    poly_math_str = format_poly(poly_simplified, 5) if poly_simplified != 0 else "0"
    
    steps.append(f"PASO {step_num}: Polinomio resultante")
    steps.append(f"  P(x) = {poly_math_str}")
    
    if x_eval is not None:
        steps.append("")
        steps.append(f"PASO {step_num + 1}: Evaluar en x = {x_eval}")
        steps.append(f"  P({x_eval}) ≈ {accumulated:.6f}")

    poly_math_str = f"P(x) = {poly_math_str}"

    # Generar curva para gráfica
    x_arr = np.array(x_points, dtype=float)
    x_min, x_max = min(x_points), max(x_points)
    margin = (x_max - x_min) * 0.2 if x_max > x_min else 1.0
    x_plot = np.linspace(x_min - margin, x_max + margin, 200).tolist()
    y_plot = []
    
    poly_func = sp.lambdify(x_sym, poly_simplified, "numpy")
    for xv in x_plot:
        y_plot.append(float(poly_func(xv)))

    msg = f"P({x_eval}) ≈ {accumulated:.10f}" if x_eval is not None else "Polinomio interpolante calculado exitosamente"

    return InterpolationResult(
        polynomial_str=f"P(x) de grado {n-1} por Lagrange",
        polynomial_math=poly_math_str,
        interpolated_value=round(accumulated, 10) if x_eval is not None else None,
        table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=msg,
    )


# ── Newton (Diferencias Divididas) ─────────────────────────────────

def newton_interpolation(x_points: list[float], y_points: list[float],
                         x_eval: float | None = None) -> InterpolationResult:
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
        "PASO 1: Identificar los datos",
        f"Tenemos {n} puntos, por lo tanto:",
        f"  • n = {n} puntos",
        f"  • El polinomio será de grado n - 1 = {n - 1}",
    ]
    for i in range(n):
        steps.append(f"  • x_{i} = {x_points[i]},  y_{i} = {y_points[i]}")
    
    steps.extend([
        "",
        "PASO 2: Calcular la tabla de diferencias divididas",
    ])

    for j in range(n):
        steps.append(f"  Orden {j}: {[round(diff_table[i][j], 6) for i in range(n - j)]}")
    
    steps.append("")
    steps.append("PASO 3: Polinomio de Newton")
    steps.append("P(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) ...")

    # Evaluar polinomio simbólico
    x_sym = sp.Symbol('x')
    poly_expr = coefficients[0]
    
    table = []
    result = coefficients[0]
    accumulated = result if x_eval is not None else 0.0
    
    for i in range(n):
        coeff = coefficients[i]
        
        if i > 0:
            term_sym = coeff
            for k in range(i):
                term_sym *= (x_sym - x_points[k])
            poly_expr += term_sym
            
        row = NewtonInterpRow(
            i=i, xi=round(x_points[i], 8), yi=round(y_points[i], 8),
            divided_diff=round(diff_table[0][i], 8) if i < n else 0.0,
            coefficient=round(coeff, 8),
            accumulated=round(accumulated, 8) if x_eval is not None else 0.0,
        )
        table.append(row)
        
        if i > 0 and x_eval is not None:
            term = coeff
            for k in range(i):
                term *= (x_eval - x_points[k])
            accumulated += term

    coefs_str = " + ".join([f"{format_poly(coefficients[i], 5)}*{''.join([f'(x-{x_points[k]})' for k in range(i)])}" for i in range(n)])
    steps.append("Sustituimos coeficientes:")
    steps.append(f"  P(x) = {coefs_str.replace('+-', '- ')}")
    
    poly_simplified = sp.simplify(poly_expr)
    poly_math_str = format_poly(poly_simplified, 5) if poly_simplified != 0 else "0"
    
    steps.append("")
    steps.append("PASO 4: Polinomio resultante (desarrollado y simplificado)")
    steps.append(f"  P(x) = {poly_math_str}")

    if x_eval is not None:
        steps.append("")
        steps.append(f"PASO 5: Evaluar en x = {x_eval}")
        steps.append(f"  P({x_eval}) ≈ {accumulated:.6f}")

    poly_math_str = f"P(x) = {poly_math_str}"

    # Curva para gráfica
    x_min, x_max = min(x_points), max(x_points)
    margin = (x_max - x_min) * 0.2 if x_max > x_min else 1.0
    x_plot = np.linspace(x_min - margin, x_max + margin, 200).tolist()
    y_plot = []
    poly_func = sp.lambdify(x_sym, poly_simplified, "numpy")
    for xv in x_plot:
        y_plot.append(float(poly_func(xv)))

    msg = f"P({x_eval}) ≈ {accumulated:.10f}" if x_eval is not None else "Polinomio interpolante calculado exitosamente"

    return InterpolationResult(
        polynomial_str=f"P(x) de grado {n-1} por Newton (diferencias divididas)",
        polynomial_math=poly_math_str,
        interpolated_value=round(accumulated, 10) if x_eval is not None else None,
        table=table, procedure_steps=steps,
        x_plot=x_plot, y_plot=y_plot,
        message=msg,
    )
