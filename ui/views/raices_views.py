"""
raices_views.py — Vistas para el módulo de cálculo de raíces.
Bisección, Newton-Raphson, Secante.
La vista es "tonta": solo dibuja campos y delega al core.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout,
)
from ui.views.base_method_view import BaseMethodView
from ui.components.math_input import MathInput
from core.raices.raices import biseccion, newton_raphson, secante
from dataclasses import asdict


class BiseccionView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Método de Bisección"

    def _get_module_name(self) -> str:
        return "Raíces"

    def _get_method_description(self) -> str:
        return ("Encuentra raíces de f(x) = 0 dividiendo sucesivamente un intervalo [a, b] "
                "donde existe un cambio de signo.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^3 - x - 2")
        self._input_func.setToolTip("Ingrese la función f(x)")

        self._input_a = QLineEdit()
        self._input_a.setPlaceholderText("Ej: 1")

        self._input_b = QLineEdit()
        self._input_b.setPlaceholderText("Ej: 2")

        self._input_tol = QLineEdit("1e-6")
        self._input_tol.setToolTip("Tolerancia para la convergencia")

        self._input_max_iter = QLineEdit("100")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("a (inicio intervalo):", self._input_a)
        layout.addRow("b (fin intervalo):", self._input_b)
        layout.addRow("Tolerancia:", self._input_tol)
        layout.addRow("Máx. iteraciones:", self._input_max_iter)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "a": self._input_a.text(),
            "b": self._input_b.text(),
            "Tolerancia": self._input_tol.text(),
            "Máx. iteraciones": self._input_max_iter.text(),
        }

    def _run_calculation(self) -> dict:
        result = biseccion(
            func_str=self._input_func.text().strip(),
            a=float(self._input_a.text()),
            b=float(self._input_b.text()),
            tolerance=float(self._input_tol.text()),
            max_iterations=int(self._input_max_iter.text()),
        )
        headers = ["No.", "a", "c = Xm", "b", "f(a)", "f(c)", "f(b)", "Error"]
        rows = [[r.iteration, r.a, r.c, r.b, r.fa, r.fc, r.fb, r.error] for r in result.table]

        import numpy as np
        from core.raices.raices import _parse_function
        func, _ = _parse_function(self._input_func.text().strip())
        a_val, b_val = float(self._input_a.text()), float(self._input_b.text())
        margin = (b_val - a_val) * 0.3
        x_plot = np.linspace(a_val - margin, b_val + margin, 300).tolist()
        y_plot = [float(func(xv)) for xv in x_plot]

        x_points_iter = [r.c for r in result.table]
        y_points_iter = [r.fc for r in result.table]

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": x_plot, "y_plot": y_plot,
            "x_points": x_points_iter, "y_points": y_points_iter,
            "highlight_x": result.root, "highlight_label": f"Raíz = {result.root:.6f}",
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x^3 - x - 2")
        self._input_a.setText("1")
        self._input_b.setText("2")
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")

    def _clear_form(self):
        self._input_func.clear()
        self._input_a.clear()
        self._input_b.clear()
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")


class NewtonRaphsonView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Método de Newton-Raphson"

    def _get_module_name(self) -> str:
        return "Raíces"

    def _get_method_description(self) -> str:
        return ("Encuentra raíces usando la derivada de f(x). Convergencia rápida "
                "pero requiere un buen valor inicial y la derivada f'(x).")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^3 - x - 2")

        self._input_deriv = MathInput()
        self._input_deriv.setPlaceholderText("Ej: 3*x^2 - 1")
        self._input_deriv.setToolTip("Derivada de f(x). Si deja vacío se calculará automáticamente.")

        self._input_x0 = QLineEdit()
        self._input_x0.setPlaceholderText("Ej: 1.5")

        self._input_tol = QLineEdit("1e-6")
        self._input_max_iter = QLineEdit("100")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("f'(x) =", self._input_deriv)
        layout.addRow("x₀ (valor inicial):", self._input_x0)
        layout.addRow("Tolerancia:", self._input_tol)
        layout.addRow("Máx. iteraciones:", self._input_max_iter)

        # Ayuda
        help_label = QLabel("💡 Si deja f'(x) vacío, se calculará simbólicamente con SymPy.")
        help_label.setObjectName("subtitle")
        help_label.setWordWrap(True)
        layout.addRow(help_label)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "f'(x)": self._input_deriv.text() or "(auto)",
            "x0": self._input_x0.text(),
            "Tolerancia": self._input_tol.text(),
            "Máx. iteraciones": self._input_max_iter.text(),
        }

    def _run_calculation(self) -> dict:
        import sympy as sp
        func_str = self._input_func.text().strip()
        deriv_str = self._input_deriv.text().strip()

        if not deriv_str:
            x_sym = sp.Symbol("x")
            deriv_str = str(sp.diff(sp.sympify(func_str.replace("^", "^")), x_sym))

        result = newton_raphson(
            func_str=func_str,
            deriv_str=deriv_str,
            x0=float(self._input_x0.text()),
            tolerance=float(self._input_tol.text()),
            max_iterations=int(self._input_max_iter.text()),
        )
        headers = ["Iteración", "xn", "f(xn)", "f'(xn)", "xn+1", "f(xn+1)", "Error"]
        rows = [[r.iteration, r.xn, r.fxn, r.fpxn, r.xn1, r.fxn1, r.error] for r in result.table]

        import numpy as np
        from core.raices.raices import _parse_function
        func, _ = _parse_function(func_str)
        center = result.root
        x_plot = np.linspace(center - 3, center + 3, 300).tolist()
        y_plot = [float(func(xv)) for xv in x_plot]

        x_points_iter = [r.xn for r in result.table]
        y_points_iter = [r.fxn for r in result.table]

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": x_plot, "y_plot": y_plot,
            "x_points": x_points_iter, "y_points": y_points_iter,
            "highlight_x": result.root, "highlight_label": f"Raíz = {result.root:.6f}",
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x^3 - x - 2")
        self._input_deriv.setText("3*x^2 - 1")
        self._input_x0.setText("1.5")
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")

    def _clear_form(self):
        self._input_func.clear()
        self._input_deriv.clear()
        self._input_x0.clear()
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")


class SecanteView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Método de la Secante"

    def _get_module_name(self) -> str:
        return "Raíces"

    def _get_method_description(self) -> str:
        return ("Similar a Newton-Raphson pero no requiere derivada. "
                "Usa dos valores iniciales para aproximar la pendiente.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^3 - x - 2")

        self._input_x0 = QLineEdit()
        self._input_x0.setPlaceholderText("Ej: 1")

        self._input_x1 = QLineEdit()
        self._input_x1.setPlaceholderText("Ej: 2")

        self._input_tol = QLineEdit("1e-6")
        self._input_max_iter = QLineEdit("100")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("x₀ (primer valor):", self._input_x0)
        layout.addRow("x₁ (segundo valor):", self._input_x1)
        layout.addRow("Tolerancia:", self._input_tol)
        layout.addRow("Máx. iteraciones:", self._input_max_iter)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "x0": self._input_x0.text(),
            "x1": self._input_x1.text(),
            "Tolerancia": self._input_tol.text(),
            "Máx. iteraciones": self._input_max_iter.text(),
        }

    def _run_calculation(self) -> dict:
        result = secante(
            func_str=self._input_func.text().strip(),
            x0=float(self._input_x0.text()),
            x1=float(self._input_x1.text()),
            tolerance=float(self._input_tol.text()),
            max_iterations=int(self._input_max_iter.text()),
        )
        headers = ["Iteración", "xn-1", "xn", "f(xn-1)", "f(xn)", "xn+1", "Error"]
        rows = [[r.iteration, r.xn_prev, r.xn, r.fxn_prev, r.fxn, r.xn1, r.error] for r in result.table]

        import numpy as np
        from core.raices.raices import _parse_function
        func, _ = _parse_function(self._input_func.text().strip())
        center = result.root
        x_plot = np.linspace(center - 3, center + 3, 300).tolist()
        y_plot = [float(func(xv)) for xv in x_plot]

        x_points_iter = [r.xn for r in result.table]
        y_points_iter = [r.fxn for r in result.table]

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": x_plot, "y_plot": y_plot,
            "x_points": x_points_iter, "y_points": y_points_iter,
            "highlight_x": result.root, "highlight_label": f"Raíz = {result.root:.6f}",
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x^3 - x - 2")
        self._input_x0.setText("1")
        self._input_x1.setText("2")
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")

    def _clear_form(self):
        self._input_func.clear()
        self._input_x0.clear()
        self._input_x1.clear()
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")
