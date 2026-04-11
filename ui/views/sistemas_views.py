"""
sistemas_views.py — Vistas para sistemas de ecuaciones (Gauss-Seidel, LU).
"""
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QLabel, QTextEdit, QVBoxLayout,
)
from ui.views.base_method_view import BaseMethodView
from ui.components.math_input import MathInput
from core.sistemas.sistemas import gauss_seidel, factorizacion_lu


class GaussSeidelView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Gauss-Seidel"

    def _get_module_name(self) -> str:
        return "Sistemas de Ecuaciones"

    def _get_method_description(self) -> str:
        return ("Método iterativo para resolver sistemas lineales Ax = b. "
                "Funciona mejor cuando la matriz es diagonalmente dominante.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        help_label = QLabel(
            "💡 Ingrese la matriz A fila por fila, separando elementos con comas "
            "y filas con punto y coma (;).\nEj: 4, -1, 0; -1, 4, -1; 0, -1, 4"
        )
        help_label.setObjectName("subtitle")
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        form = QFormLayout()

        self._input_matrix = MathInput()
        self._input_matrix.setPlaceholderText("4, -1, 0; -1, 4, -1; 0, -1, 4")

        self._input_b = MathInput()
        self._input_b.setPlaceholderText("Ej: 15, 10, 10")

        self._input_x0 = MathInput()
        self._input_x0.setPlaceholderText("Ej: 0, 0, 0 (o dejar vacío)")

        self._input_tol = QLineEdit("1e-6")
        self._input_max_iter = QLineEdit("100")

        form.addRow("Matriz A:", self._input_matrix)
        form.addRow("Vector b:", self._input_b)
        form.addRow("Vector inicial x₀:", self._input_x0)
        form.addRow("Tolerancia:", self._input_tol)
        form.addRow("Máx. iteraciones:", self._input_max_iter)

        layout.addLayout(form)
        return widget

    def _get_parameters(self) -> dict:
        return {
            "Matriz A": self._input_matrix.text(),
            "Vector b": self._input_b.text(),
            "Vector x₀": self._input_x0.text() or "(ceros)",
            "Tolerancia": self._input_tol.text(),
        }

    def _run_calculation(self) -> dict:
        matrix_text = self._input_matrix.text().strip()
        rows_text = [r.strip() for r in matrix_text.replace("\n", ";").split(";") if r.strip()]
        matrix_a = [[float(v.strip()) for v in row.split(",")] for row in rows_text]

        vector_b = [float(v.strip()) for v in self._input_b.text().split(",")]

        x0_text = self._input_x0.text().strip()
        x0 = [float(v.strip()) for v in x0_text.split(",")] if x0_text else None

        result = gauss_seidel(
            matrix_a=matrix_a, vector_b=vector_b, x0=x0,
            tolerance=float(self._input_tol.text()),
            max_iterations=int(self._input_max_iter.text()),
        )

        n = len(vector_b)
        headers = ["Iteración"] + [f"x{i+1}" for i in range(n)] + ["Error"]
        rows = []
        for r in result.table:
            row_data = [r.iteration] + list(r.values) + [r.error]
            rows.append(row_data)

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": None, "y_plot": None,
        }

    def _load_example(self):
        self._input_matrix.setText("4, -1, 0; -1, 4, -1; 0, -1, 4")
        self._input_b.setText("15, 10, 10")
        self._input_x0.setText("0, 0, 0")
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")

    def _clear_form(self):
        self._input_matrix.clear()
        self._input_b.clear()
        self._input_x0.clear()
        self._input_tol.setText("1e-6")
        self._input_max_iter.setText("100")


class FactorizacionLUView(BaseMethodView):

    def _get_method_name(self) -> str:
        return "Factorización LU"

    def _get_module_name(self) -> str:
        return "Sistemas de Ecuaciones"

    def _get_method_description(self) -> str:
        return ("Descompone la matriz A en L (triangular inferior) y U (triangular superior) "
                "para resolver el sistema mediante sustituciones sucesivas.")

    def _build_form(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        help_label = QLabel(
            "💡 Ingrese la matriz A fila por fila (comas entre elementos, ; entre filas)."
        )
        help_label.setObjectName("subtitle")
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        form = QFormLayout()

        self._input_matrix = MathInput()
        self._input_matrix.setPlaceholderText("2, 1, 1; 4, 3, 3; 8, 7, 9")

        self._input_b = MathInput()
        self._input_b.setPlaceholderText("Ej: 1, 1, 1")

        form.addRow("Matriz A:", self._input_matrix)
        form.addRow("Vector b:", self._input_b)

        layout.addLayout(form)
        return widget

    def _get_parameters(self) -> dict:
        return {
            "Matriz A": self._input_matrix.text(),
            "Vector b": self._input_b.text(),
        }

    def _run_calculation(self) -> dict:
        matrix_text = self._input_matrix.text().strip()
        rows_text = [r.strip() for r in matrix_text.replace("\n", ";").split(";") if r.strip()]
        matrix_a = [[float(v.strip()) for v in row.split(",")] for row in rows_text]
        vector_b = [float(v.strip()) for v in self._input_b.text().split(",")]

        result = factorizacion_lu(matrix_a=matrix_a, vector_b=vector_b)

        headers = ["Paso", "Operación", "Observación"]
        rows = [[r.step, r.operation, r.observation] for r in result.table]

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": None, "y_plot": None,
        }

    def _load_example(self):
        self._input_matrix.setText("2, 1, 1; 4, 3, 3; 8, 7, 9")
        self._input_b.setText("1, 1, 1")

    def _clear_form(self):
        self._input_matrix.clear()
        self._input_b.clear()
