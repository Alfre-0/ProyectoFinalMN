"""
interpolacion_views.py — Vistas para interpolación (Lagrange, Newton).
"""
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel
from ui.views.base_method_view import BaseMethodView
from ui.components.math_input import MathInput
from core.interpolacion.interpolacion import lagrange, newton_interpolation


class LagrangeView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Interpolación de Lagrange"

    def _get_module_name(self) -> str:
        return "Interpolación"

    def _get_method_description(self) -> str:
        return ("Construye un polinomio interpolante a partir de un conjunto "
                "de puntos conocidos (xi, yi) usando los polinomios base de Lagrange.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_x = MathInput()
        self._input_x.setPlaceholderText("Ej: 1, 2, 3, 4")
        self._input_x.setToolTip("Valores de x separados por comas")

        self._input_y = MathInput()
        self._input_y.setPlaceholderText("Ej: 1, 4, 9, 16")
        self._input_y.setToolTip("Valores de y correspondientes, separados por comas")

        self._input_xeval = MathInput()
        self._input_xeval.setPlaceholderText("Ej: 2.5")
        self._input_xeval.setToolTip("Valor de x donde se desea interpolar")

        layout.addRow("Valores x:", self._input_x)
        layout.addRow("Valores y:", self._input_y)
        layout.addRow("x a interpolar:", self._input_xeval)

        help_label = QLabel("💡 Ingrese los puntos separados por comas. No se permiten x repetidos.")
        help_label.setObjectName("subtitle")
        help_label.setWordWrap(True)
        layout.addRow(help_label)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "Puntos x": self._input_x.text(),
            "Puntos y": self._input_y.text(),
            "x a interpolar": self._input_xeval.text(),
        }

    def _run_calculation(self) -> dict:
        x_points = [float(v.strip()) for v in self._input_x.text().split(",")]
        y_points = [float(v.strip()) for v in self._input_y.text().split(",")]
        x_eval = float(self._input_xeval.text())

        result = lagrange(x_points, y_points, x_eval)

        headers = ["i", "xi", "yi", "Li(x)", "Término", "Acumulado"]
        rows = [[r.i, r.xi, r.yi, r.li_value, r.term, r.accumulated] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "x_points": x_points, "y_points": y_points,
            "highlight_x": x_eval,
            "highlight_label": f"P({x_eval}) ≈ {result.interpolated_value:.6f}",
            "xlabel": "x", "ylabel": "P(x)", "plot_label": "Polinomio interpolante",
        }

    def _load_example(self):
        self._input_x.setText("1, 2, 4, 7")
        self._input_y.setText("1, 4, 16, 49")
        self._input_xeval.setText("3")

    def _clear_form(self):
        self._input_x.clear()
        self._input_y.clear()
        self._input_xeval.clear()


class NewtonInterpolacionView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Interpolación de Newton"

    def _get_module_name(self) -> str:
        return "Interpolación"

    def _get_method_description(self) -> str:
        return ("Construye un polinomio interpolante usando diferencias divididas de Newton. "
                "Eficiente para agregar nuevos puntos.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_x = MathInput()
        self._input_x.setPlaceholderText("Ej: 1, 2, 3, 4")

        self._input_y = MathInput()
        self._input_y.setPlaceholderText("Ej: 1, 4, 9, 16")

        self._input_xeval = MathInput()
        self._input_xeval.setPlaceholderText("Ej: 2.5")

        layout.addRow("Valores x:", self._input_x)
        layout.addRow("Valores y:", self._input_y)
        layout.addRow("x a interpolar:", self._input_xeval)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "Puntos x": self._input_x.text(),
            "Puntos y": self._input_y.text(),
            "x a interpolar": self._input_xeval.text(),
        }

    def _run_calculation(self) -> dict:
        x_points = [float(v.strip()) for v in self._input_x.text().split(",")]
        y_points = [float(v.strip()) for v in self._input_y.text().split(",")]
        x_eval = float(self._input_xeval.text())

        result = newton_interpolation(x_points, y_points, x_eval)

        headers = ["i", "xi", "yi", "Dif. Dividida", "Coeficiente", "Acumulado"]
        rows = [[r.i, r.xi, r.yi, r.divided_diff, r.coefficient, r.accumulated] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_plot, "y_plot": result.y_plot,
            "x_points": x_points, "y_points": y_points,
            "highlight_x": x_eval,
            "highlight_label": f"P({x_eval}) ≈ {result.interpolated_value:.6f}",
            "xlabel": "x", "ylabel": "P(x)", "plot_label": "Polinomio interpolante",
        }

    def _load_example(self):
        self._input_x.setText("1, 2, 4, 7")
        self._input_y.setText("1, 4, 16, 49")
        self._input_xeval.setText("3")

    def _clear_form(self):
        self._input_x.clear()
        self._input_y.clear()
        self._input_xeval.clear()
