"""
edos_views.py — Vistas para ecuaciones diferenciales ordinarias (Euler, RK4).
"""
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel
from ui.views.base_method_view import BaseMethodView
from core.edos.edos import euler, runge_kutta_4


class EulerView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Método de Euler"

    def _get_module_name(self) -> str:
        return "Ecuaciones Diferenciales"

    def _get_method_description(self) -> str:
        return ("Aproxima la solución de una EDO dy/dx = f(x, y) avanzando "
                "paso a paso con incrementos lineales.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = QLineEdit()
        self._input_func.setPlaceholderText("Ej: x + y")
        self._input_func.setToolTip("Ecuación dy/dx = f(x, y). Use 'x' e 'y' como variables.")

        self._input_x0 = QLineEdit()
        self._input_x0.setPlaceholderText("Ej: 0")

        self._input_y0 = QLineEdit()
        self._input_y0.setPlaceholderText("Ej: 1")

        self._input_xf = QLineEdit()
        self._input_xf.setPlaceholderText("Ej: 2")

        self._input_h = QLineEdit()
        self._input_h.setPlaceholderText("Ej: 0.1")

        layout.addRow("dy/dx = f(x, y) =", self._input_func)
        layout.addRow("x₀:", self._input_x0)
        layout.addRow("y(x₀) = y₀:", self._input_y0)
        layout.addRow("x final:", self._input_xf)
        layout.addRow("Paso h:", self._input_h)

        help_label = QLabel("💡 Ingrese la ecuación diferencial usando 'x' e 'y' como variables.")
        help_label.setObjectName("subtitle")
        help_label.setWordWrap(True)
        layout.addRow(help_label)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x,y)": self._input_func.text(),
            "x₀": self._input_x0.text(),
            "y₀": self._input_y0.text(),
            "x final": self._input_xf.text(),
            "h": self._input_h.text(),
        }

    def _run_calculation(self) -> dict:
        result = euler(
            func_str=self._input_func.text().strip(),
            x0=float(self._input_x0.text()),
            y0=float(self._input_y0.text()),
            x_final=float(self._input_xf.text()),
            h=float(self._input_h.text()),
        )
        headers = ["Iteración", "xi", "yi", "f(xi,yi)", "yi+1", "Error"]
        rows = [[r.iteration, r.xi, r.yi, r.fxy, r.yi_next, r.error] for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_values, "y_plot": result.y_values,
            "xlabel": "x", "ylabel": "y(x)", "plot_label": "Solución aprox. (Euler)",
        }

    def _load_example(self):
        self._input_func.setText("x + y")
        self._input_x0.setText("0")
        self._input_y0.setText("1")
        self._input_xf.setText("2")
        self._input_h.setText("0.1")

    def _clear_form(self):
        self._input_func.clear()
        self._input_x0.clear()
        self._input_y0.clear()
        self._input_xf.clear()
        self._input_h.clear()


class RungeKuttaView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Runge-Kutta (RK4)"

    def _get_module_name(self) -> str:
        return "Ecuaciones Diferenciales"

    def _get_method_description(self) -> str:
        return ("Método de Runge-Kutta de 4to orden para resolver EDOs. "
                "Más preciso que Euler, calcula 4 pendientes intermedias por paso.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(10)

        self._input_func = QLineEdit()
        self._input_func.setPlaceholderText("Ej: x + y")

        self._input_x0 = QLineEdit()
        self._input_x0.setPlaceholderText("Ej: 0")

        self._input_y0 = QLineEdit()
        self._input_y0.setPlaceholderText("Ej: 1")

        self._input_xf = QLineEdit()
        self._input_xf.setPlaceholderText("Ej: 2")

        self._input_h = QLineEdit()
        self._input_h.setPlaceholderText("Ej: 0.1")

        layout.addRow("dy/dx = f(x, y) =", self._input_func)
        layout.addRow("x₀:", self._input_x0)
        layout.addRow("y(x₀) = y₀:", self._input_y0)
        layout.addRow("x final:", self._input_xf)
        layout.addRow("Paso h:", self._input_h)

        return widget

    def _get_parameters(self) -> dict:
        return {
            "f(x,y)": self._input_func.text(),
            "x₀": self._input_x0.text(),
            "y₀": self._input_y0.text(),
            "x final": self._input_xf.text(),
            "h": self._input_h.text(),
        }

    def _run_calculation(self) -> dict:
        result = runge_kutta_4(
            func_str=self._input_func.text().strip(),
            x0=float(self._input_x0.text()),
            y0=float(self._input_y0.text()),
            x_final=float(self._input_xf.text()),
            h=float(self._input_h.text()),
        )
        headers = ["Iteración", "xi", "yi", "k1", "k2", "k3", "k4", "yi+1", "Error"]
        rows = [[r.iteration, r.xi, r.yi, r.k1, r.k2, r.k3, r.k4, r.yi_next, r.error]
                for r in result.table]

        return {
            "message": result.message, "converged": True,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": result.x_values, "y_plot": result.y_values,
            "xlabel": "x", "ylabel": "y(x)", "plot_label": "Solución aprox. (RK4)",
        }

    def _load_example(self):
        self._input_func.setText("x + y")
        self._input_x0.setText("0")
        self._input_y0.setText("1")
        self._input_xf.setText("2")
        self._input_h.setText("0.1")

    def _clear_form(self):
        self._input_func.clear()
        self._input_x0.clear()
        self._input_y0.clear()
        self._input_xf.clear()
        self._input_h.clear()
