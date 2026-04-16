"""
integracion_views.py — Vistas para derivación e integración numérica.
Diferencias Finitas, Trapecio, Simpson.
"""
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox
from ui.views.base_method_view import BaseMethodView
from ui.components.math_input import MathInput
from ui.styles.theme import ThemeManager
from core.integracion_derivacion.integracion_derivacion import (
    punto_medio, trapecio, simpson,
)


class PuntoMedioView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Regla del Punto Medio"

    def _get_module_name(self) -> str:
        return "Derivación e Integración"

    def _get_method_description(self) -> str:
        return ("Aproxima el área bajo la curva calculando rectángulos cuya altura "
                "está dada por la función evaluada en el centro de cada subintervalo.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^2")

        self._input_a = QLineEdit()
        self._input_a.setPlaceholderText("Ej: 0.0")

        self._input_b = QLineEdit()
        self._input_b.setPlaceholderText("Ej: 1.0")

        self._input_n = QLineEdit("10")
        self._input_n.setToolTip("Número de rectángulos")

        layout.addRow("f(x) =", self._input_func)
        layout.addRow("a (límite inferior):", self._input_a)
        layout.addRow("b (límite superior):", self._input_b)
        layout.addRow("n (rectángulos):", self._input_n)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x)": self._input_func.text(),
            "a": self._input_a.text(),
            "b": self._input_b.text(),
            "n": self._input_n.text(),
        }

    def _run_calculation(self) -> dict:
        result = punto_medio(
            func_str=self._input_func.text().strip(),
            a=float(self._input_a.text()),
            b=float(self._input_b.text()),
            n_intervals=int(self._input_n.text()),
        )
        headers = ["No.", "Xi", "Xi + 1", "X̄", "f(X̄)", "Area (Ai)"]
        rows = [[r.index, r.xi, r.xi_plus_1, r.x_mid, r.f_x_mid, r.area_i] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
            "rectangles": result.rectangles
        }

    def _display_result(self, result: dict):
        super()._display_result(result)
        
        # Inyectar rectángulos de área
        colors = ThemeManager.colors().PLOT_LINE_COLORS
        rect_color = colors[1] if len(colors) > 1 else "blue"
        
        for rect in result.get("rectangles", []):
            x_mid = rect["x_mid"]
            width = rect["width"]
            height = rect["height"]
            
            # Dibujar el rectángulo
            self._plot_widget.axes.bar(
                x_mid, height, width=width, align="center",
                edgecolor="black", color=rect_color, alpha=0.3, zorder=2
            )
            # Dibujar el centro del rectángulo
            self._plot_widget.axes.scatter(
                x_mid, height, color="red", zorder=4, s=30, marker="o"
            )
            
        self._plot_widget.refresh()

    def _load_example(self):
        self._input_func.setText("x^2")
        self._input_a.setText("0")
        self._input_b.setText("1")
        self._input_n.setText("10")

    def _clear_form(self):
        self._input_func.clear()
        self._input_a.clear()
        self._input_b.clear()
        self._input_n.setText("10")


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

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^2")

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
        headers = ["No.", "dx", "xi", "f(xi)", "Factor", "dx/2 * factor * f(xi)"]
        rows = [[r.index, r.dx, r.xi, r.fxi, r.factor, r.partial] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x^2")
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

        self._input_func = MathInput()
        self._input_func.setPlaceholderText("Ej: x^2")

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
        headers = ["No.", "dx", "xi", "f(xi)", "Factor", "(dx/3) * factor * f(xi)"]
        rows = [[r.index, r.dx, r.xi, r.fxi, r.factor, r.partial] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "xlabel": "x", "ylabel": "f(x)", "plot_label": "f(x)",
        }

    def _load_example(self):
        self._input_func.setText("x^2")
        self._input_a.setText("0")
        self._input_b.setText("1")
        self._input_n.setText("10")

    def _clear_form(self):
        self._input_func.clear()
        self._input_a.clear()
        self._input_b.clear()
        self._input_n.setText("10")
