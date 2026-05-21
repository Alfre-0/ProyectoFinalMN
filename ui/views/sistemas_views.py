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
        # 1. Validar Matriz A
        matrix_text = self._input_matrix.text().strip()
        if not matrix_text:
            raise ValueError("Por favor, ingrese la Matriz A.")
        try:
            rows_text = [r.strip() for r in matrix_text.replace("\n", ";").split(";") if r.strip()]
            matrix_a = [[float(v.strip()) for v in row.split(",") if v.strip()] for row in rows_text]
        except Exception as e:
            raise ValueError("La Matriz A tiene un formato inválido. Use comas para separar los elementos y punto y coma (;) para separar las filas.\nEjemplo: 4, -1, 0; -1, 4, -1; 0, -1, 4") from e

        if not matrix_a or any(len(row) == 0 for row in matrix_a):
            raise ValueError("La Matriz A no puede estar vacía.")

        n_rows = len(matrix_a)
        for idx, row in enumerate(matrix_a):
            if len(row) != n_rows:
                raise ValueError(f"La Matriz A debe ser cuadrada. La fila {idx+1} tiene {len(row)} columnas pero el sistema tiene {n_rows} filas.")

        # 2. Validar Vector b
        b_text = self._input_b.text().strip()
        if not b_text:
            raise ValueError("Por favor, ingrese el Vector b.")
        try:
            vector_b = [float(v.strip()) for v in b_text.split(",") if v.strip()]
        except Exception as e:
            raise ValueError("El Vector b tiene un formato inválido. Separe los elementos con comas. Ejemplo: 15, 10, 10") from e

        if len(vector_b) != n_rows:
            raise ValueError(f"Las dimensiones no coinciden: el Vector b tiene {len(vector_b)} elementos, pero la Matriz A tiene {n_rows} filas.")

        # 3. Validar Vector inicial x0 (opcional)
        x0_text = self._input_x0.text().strip()
        if x0_text:
            try:
                x0 = [float(v.strip()) for v in x0_text.split(",") if v.strip()]
            except Exception as e:
                raise ValueError("El Vector inicial x₀ tiene un formato inválido. Separe los elementos con comas. Ejemplo: 0, 0, 0") from e
            if len(x0) != n_rows:
                raise ValueError(f"El Vector inicial x₀ tiene {len(x0)} elementos, pero debe tener {n_rows} para coincidir con el sistema.")
        else:
            x0 = None

        # 4. Validar Tolerancia y Máx. iteraciones
        try:
            tol = float(self._input_tol.text())
            if tol <= 0:
                raise ValueError("La tolerancia debe ser un número positivo mayor que cero.")
        except ValueError as e:
            if "positivo" in str(e): raise
            raise ValueError("La tolerancia debe ser un número decimal válido (ej: 1e-6).") from e

        try:
            max_iter = int(self._input_max_iter.text())
            if max_iter <= 0:
                raise ValueError("El número de iteraciones debe ser un entero positivo.")
        except ValueError as e:
            if "entero positivo" in str(e): raise
            raise ValueError("El número máximo de iteraciones debe ser un número entero válido (ej: 100).") from e

        result = gauss_seidel(
            matrix_a=matrix_a, vector_b=vector_b, x0=x0,
            tolerance=tol, max_iterations=max_iter,
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

    def _get_examples(self) -> list[dict]:
        return [
            {
                "name": "1. Dominante 3x3 (Convergente)",
                "values": {"matrix": "4, -1, 0; -1, 4, -1; 0, -1, 4", "b": "15, 10, 10", "x0": "0, 0, 0", "tol": "1e-6", "max_iter": "100"}
            },
            {
                "name": "2. Dominante 2x2 (Simple)",
                "values": {"matrix": "3, 1; 1, 4", "b": "5, 6", "x0": "0, 0", "tol": "1e-6", "max_iter": "100"}
            },
            {
                "name": "3. Red Eléctrica 3x3 (Física)",
                "values": {"matrix": "5, -2, -1; -2, 6, -2; -1, -2, 7", "b": "10, 20, 30", "x0": "0, 0, 0", "tol": "1e-6", "max_iter": "100"}
            },
            {
                "name": "4. Tridiagonal Simétrica 3x3",
                "values": {"matrix": "4, 1, 0; 1, 4, 1; 0, 1, 4", "b": "5, 6, 5", "x0": "0, 0, 0", "tol": "1e-6", "max_iter": "100"}
            }
        ]

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
        # 1. Validar Matriz A
        matrix_text = self._input_matrix.text().strip()
        if not matrix_text:
            raise ValueError("Por favor, ingrese la Matriz A.")
        try:
            rows_text = [r.strip() for r in matrix_text.replace("\n", ";").split(";") if r.strip()]
            matrix_a = [[float(v.strip()) for v in row.split(",") if v.strip()] for row in rows_text]
        except Exception as e:
            raise ValueError("La Matriz A tiene un formato inválido. Use comas para separar los elementos y punto y coma (;) para separar las filas.\nEjemplo: 2, 1, 1; 4, 3, 3; 8, 7, 9") from e

        if not matrix_a or any(len(row) == 0 for row in matrix_a):
            raise ValueError("La Matriz A no puede estar vacía.")

        n_rows = len(matrix_a)
        for idx, row in enumerate(matrix_a):
            if len(row) != n_rows:
                raise ValueError(f"La Matriz A debe ser cuadrada. La fila {idx+1} tiene {len(row)} columnas pero el sistema tiene {n_rows} filas.")

        # 2. Validar Vector b
        b_text = self._input_b.text().strip()
        if not b_text:
            raise ValueError("Por favor, ingrese el Vector b.")
        try:
            vector_b = [float(v.strip()) for v in b_text.split(",") if v.strip()]
        except Exception as e:
            raise ValueError("El Vector b tiene un formato inválido. Separe los elementos con comas. Ejemplo: 1, 1, 1") from e

        if len(vector_b) != n_rows:
            raise ValueError(f"Las dimensiones no coinciden: el Vector b tiene {len(vector_b)} elementos, pero la Matriz A tiene {n_rows} filas.")

        result = factorizacion_lu(matrix_a=matrix_a, vector_b=vector_b)

        headers = ["Paso", "Operación", "Observación"]
        rows = [[r.step, r.operation, r.observation] for r in result.table]

        return {
            "message": result.message, "converged": result.converged,
            "procedure_steps": result.procedure_steps,
            "table_headers": headers, "table_rows": rows,
            "x_plot": None, "y_plot": None,
        }

    def _get_examples(self) -> list[dict]:
        return [
            {
                "name": "1. Estándar 3x3 (LU sin pivoteo)",
                "values": {"matrix": "2, 1, 1; 4, 3, 3; 8, 7, 9", "b": "1, 1, 1"}
            },
            {
                "name": "2. Sistema 3x3 (Solución única)",
                "values": {"matrix": "1, 1, 1; 2, 3, 1; 1, -1, -2", "b": "6, 11, -6"}
            },
            {
                "name": "3. Sistema 3x3 (Convergente)",
                "values": {"matrix": "3, 2, 4; 2, 2, 3; 3, 3, 5", "b": "1, 2, 3"}
            },
            {
                "name": "4. Sistema 2x2 (Básico)",
                "values": {"matrix": "4, 3; 6, 3", "b": "10, 12"}
            }
        ]

    def _load_example(self):
        self._input_matrix.setText("2, 1, 1; 4, 3, 3; 8, 7, 9")
        self._input_b.setText("1, 1, 1")

    def _clear_form(self):
        self._input_matrix.clear()
        self._input_b.clear()
