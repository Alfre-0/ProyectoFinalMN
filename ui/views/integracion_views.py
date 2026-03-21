"""
integracion_views.py — Vistas para derivación e integración numérica.
Diferencias Finitas, Trapecio, Simpson.
"""
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox
from ui.views.base_method_view import BaseMethodView
from core.integracion_derivacion.integracion_derivacion import (
    diferencias_finitas, trapecio, simpson,
)


class DiferenciasFinitasView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Diferencias Finitas"

    def _get_module_name(self) -> str:
        return "Derivación e Integración"

    def _get_method_description(self) -> str:
        return ("Aproxima la derivada de f(x) en un punto usando diferencias "
                "hacia adelante, hacia atrás o centrales.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = QLineEdit()
        self._input_func.setPlaceholderText("Ej: sin(x) + x**2")

        self._input_x = QLineEdit()
        self._input_x.setPlaceholderText("Ej: 1.0")

        self._input_h = QLineEdit("0.01")

        self._input_type = QComboBox()
        self._input_type.addItems(["central", "forward", "backward"])

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("Punto x:", self._input_x)
        layout.addRow("Paso h:", self._input_h)
        layout.addRow("Tipo:", self._input_type)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "x": self._input_x.text(),
            "h": self._input_h.text(),
            "Tipo": self._input_type.currentText(),
        }

    def _run_calculation(self) -> dict:
        result = diferencias_finitas(
            func_str=self._input_func.text().strip(),
            x_point=float(self._input_x.text()),
            h=float(self._input_h.text()),
            method=self._input_type.currentText(),
        )
        headers = ["No.", "xi", "f(xi)", "f(xi+h)", "Aproximación", "Error"]
        rows = [[r.index, r.xi, r.fxi, r.fxi_h, r.approximation, r.error] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("sin(x) + x**2")
        self._input_x.setText("1.0")
        self._input_h.setText("0.01")
        self._input_type.setCurrentText("central")

    def _clear_form(self):
        self._input_func.clear()
        self._input_x.clear()
        self._input_h.setText("0.01")


class TrapecioView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Regla del Trapecio"

    def _get_module_name(self) -> str:
        return "Derivación e Integración"

    def _get_method_description(self) -> str:
        return ("Aproxima la integral definida ∫f(x)dx dividiendo el intervalo "
                "en trapecios y sumando sus áreas.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = QLineEdit()
        self._input_func.setPlaceholderText("Ej: x**2")

        self._input_a = QLineEdit()
        self._input_a.setPlaceholderText("Ej: 0")

        self._input_b = QLineEdit()
        self._input_b.setPlaceholderText("Ej: 1")

        self._input_n = QLineEdit("10")
        self._input_n.setToolTip("Número de subintervalos")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("a (límite inferior):", self._input_a)
        layout.addRow("b (límite superior):", self._input_b)
        layout.addRow("n (subintervalos):", self._input_n)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "a": self._input_a.text(),
            "b": self._input_b.text(),
            "n": self._input_n.text(),
        }

    def _run_calculation(self) -> dict:
        result = trapecio(
            func_str=self._input_func.text().strip(),
            a=float(self._input_a.text()),
            b=float(self._input_b.text()),
            n_intervals=int(self._input_n.text()),
        )
        headers = ["No.", "Δx", "xi", "f(xi)", "Factor", "Δx/2·factor·f(xi)"]
        rows = [[r.index, r.dx, r.xi, r.fxi, r.factor, r.partial] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x**2")
        self._input_a.setText("0")
        self._input_b.setText("1")
        self._input_n.setText("10")

    def _clear_form(self):
        self._input_func.clear()
        self._input_a.clear()
        self._input_b.clear()
        self._input_n.setText("10")


class SimpsonView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Regla de Simpson 1/3"

    def _get_module_name(self) -> str:
        return "Derivación e Integración"

    def _get_method_description(self) -> str:
        return ("Aproxima la integral definida usando parábolas. "
                "Requiere un número par de subintervalos.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = QLineEdit()
        self._input_func.setPlaceholderText("Ej: x**2")

        self._input_a = QLineEdit()
        self._input_a.setPlaceholderText("Ej: 0")

        self._input_b = QLineEdit()
        self._input_b.setPlaceholderText("Ej: 1")

        self._input_n = QLineEdit("10")
        self._input_n.setToolTip("Número de subintervalos (debe ser par)")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("a (límite inferior):", self._input_a)
        layout.addRow("b (límite superior):", self._input_b)
        layout.addRow("n (subintervalos, par):", self._input_n)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "a": self._input_a.text(),
            "b": self._input_b.text(),
            "n": self._input_n.text(),
        }

    def _run_calculation(self) -> dict:
        result = simpson(
            func_str=self._input_func.text().strip(),
            a=float(self._input_a.text()),
            b=float(self._input_b.text()),
            n_intervals=int(self._input_n.text()),
        )
        headers = ["No.", "Δx", "xi", "f(xi)", "Factor", "(Δx/3)·factor·f(xi)"]
        rows = [[r.index, r.dx, r.xi, r.fxi, r.factor, r.partial] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x**2")
        self._input_a.setText("0")
        self._input_b.setText("1")
        self._input_n.setText("10")

    def _clear_form(self):
        self._input_func.clear()
        self._input_a.clear()
        self._input_b.clear()
        self._input_n.setText("10")
