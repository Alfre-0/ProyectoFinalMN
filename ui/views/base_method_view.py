"""
base_method_view.py — Vista base abstracta para cualquier método numérico.
Define la estructura estándar: formulario + botones + resultados (tabs).
Cada vista de módulo hereda de esta clase, así se asegura consistencia visual.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QTabWidget,
    QScrollArea, QFrame, QMessageBox, QFileDialog, QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.styles.tokens import Spacing, Typography, Radius
from ui.styles.theme import ThemeManager
from infrastructure.plot_widget import PlotWidget
from infrastructure.pdf_generator import PdfGenerator
from infrastructure.history_repo import HistoryRepository, HistoryRecord
from ui.components.math_canvas import MathCanvas
from ui.components.math_ast import MathExpression, build_ast_from_text
import tempfile
import os


class BaseMethodView(QWidget):
    """
    Vista base para todos los métodos numéricos.
    Las subclases solo deben implementar:
      - _build_form()        → retorna un QWidget con los campos de entrada
      - _get_method_name()   → nombre legible del método
      - _get_module_name()   → nombre del módulo (ej: 'Raíces')
      - _run_calculation()   → ejecuta la lógica y retorna datos para mostrar
      - _load_example()      → carga datos de ejemplo en los campos
      - _get_parameters()    → dict con los parámetros actuales
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history_repo = HistoryRepository()
        self._last_result = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            Spacing.XL, Spacing.XL, Spacing.XL, Spacing.LARGE
        )
        main_layout.setSpacing(Spacing.LARGE)

        # ── Encabezado ──
        header = QLabel(self._get_method_name())
        header.setObjectName("heading")
        main_layout.addWidget(header)

        subtitle = QLabel(self._get_method_description())
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        # ── Cuerpo principal: dos paneles horizontales ──
        from PyQt6.QtWidgets import QSplitter
        body_splitter = QSplitter(Qt.Orientation.Horizontal)

        # ═══════════ PANEL IZQUIERDO (≈25%) ═══════════
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, Spacing.SMALL, 0)
        left_layout.setSpacing(Spacing.MEDIUM)

        # Tarjeta de formulario
        form_card = QFrame()
        form_card.setObjectName("card")
        form_card_layout = QVBoxLayout(form_card)
        form_card_layout.setContentsMargins(
            Spacing.LARGE, Spacing.LARGE, Spacing.LARGE, Spacing.LARGE
        )

        form_title = QLabel("📝 Datos de Entrada")
        form_title.setObjectName("sectionTitle")
        form_card_layout.addWidget(form_title)

        form_widget = self._build_form()
        form_card_layout.addWidget(form_widget)

        # Botones de acción (apilados verticalmente para el panel estrecho)
        self._btn_calculate = QPushButton("▶  Calcular")
        self._btn_calculate.setMinimumHeight(36)
        self._btn_calculate.clicked.connect(self._on_calculate)
        form_card_layout.addWidget(self._btn_calculate)

        btn_row1 = QHBoxLayout()
        btn_row1.setSpacing(Spacing.SMALL)
        self._btn_example = QPushButton("📋 Ejemplo")
        self._btn_example.setObjectName("secondaryButton")
        self._btn_example.clicked.connect(self._on_load_example)
        self._btn_clear = QPushButton("🗑 Limpiar")
        self._btn_clear.setObjectName("secondaryButton")
        self._btn_clear.clicked.connect(self._on_clear)
        btn_row1.addWidget(self._btn_example)
        btn_row1.addWidget(self._btn_clear)
        form_card_layout.addLayout(btn_row1)

        self._btn_export = QPushButton("📄 Exportar PDF")
        self._btn_export.setObjectName("accentButton")
        self._btn_export.clicked.connect(self._on_export_pdf)
        self._btn_export.setEnabled(False)
        form_card_layout.addWidget(self._btn_export)

        # Espacio extra debajo de los botones
        form_card_layout.addSpacing(Spacing.LARGE)

        left_layout.addWidget(form_card)

        # Resumen de resultado (debajo de los botones, en el panel izquierdo)
        self._results_summary_card = QFrame()
        self._results_summary_card.setObjectName("card")
        self._results_summary_card.setVisible(False)
        summary_card_layout = QVBoxLayout(self._results_summary_card)
        summary_card_layout.setContentsMargins(
            Spacing.LARGE, Spacing.LARGE, Spacing.LARGE, Spacing.LARGE
        )
        summary_title = QLabel("📊 Resultado")
        summary_title.setObjectName("sectionTitle")
        summary_card_layout.addWidget(summary_title)

        self._result_summary_label = QLabel()
        self._result_summary_label.setWordWrap(True)
        self._result_summary_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SUBTITLE))
        summary_card_layout.addWidget(self._result_summary_label)

        self._result_math_canvas = MathCanvas(MathExpression())
        self._result_math_canvas.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._result_math_canvas.setCursor(Qt.CursorShape.ArrowCursor)
        self._result_math_canvas.setVisible(False)
        self._result_math_canvas.setMinimumHeight(40)
        self._result_math_canvas.setStyleSheet("background-color: transparent; border: none;")
        summary_card_layout.addWidget(self._result_math_canvas)

        left_layout.addWidget(self._results_summary_card)
        left_layout.addStretch()

        left_scroll.setWidget(left_widget)
        body_splitter.addWidget(left_scroll)

        # ═══════════ PANEL DERECHO (≈75%) ═══════════
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(Spacing.SMALL, 0, 0, 0)
        right_layout.setSpacing(Spacing.MEDIUM)

        # Gráfica (siempre visible)
        self._plot_widget = PlotWidget()
        self._plot_widget.setMinimumHeight(280)
        right_layout.addWidget(self._plot_widget, 3)

        # Tabs: Procedimiento + Tabla (debajo de la gráfica)
        self._results_card = QFrame()
        self._results_card.setObjectName("card")
        self._results_card.setVisible(False)
        results_inner = QVBoxLayout(self._results_card)
        results_inner.setContentsMargins(
            Spacing.MEDIUM, Spacing.MEDIUM, Spacing.MEDIUM, Spacing.MEDIUM
        )

        self._tabs = QTabWidget()

        # Tab: Procedimiento
        self._procedure_text = QTextEdit()
        self._procedure_text.setReadOnly(True)
        self._procedure_text.setMinimumHeight(120)

        # Tab: Tabla
        self._result_table = QTableWidget()
        self._result_table.setAlternatingRowColors(True)
        self._result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._result_table.setMinimumHeight(120)

        # Agregar la tabla primero
        self._tabs.addTab(self._result_table, "📋 Tabla")
        self._tabs.addTab(self._procedure_text, "📖 Procedimiento")
        results_inner.addWidget(self._tabs)
        right_layout.addWidget(self._results_card, 2)

        body_splitter.addWidget(right_widget)

        # Proporciones iniciales para el splitter (30% / 70%)
        body_splitter.setStretchFactor(0, 3)
        body_splitter.setStretchFactor(1, 7)
        body_splitter.setSizes([360, 840])

        main_layout.addWidget(body_splitter, 1)

    # ── Slots ──────────────────────────────────────────────────────

    def _on_calculate(self):
        try:
            result = self._run_calculation()
            self._last_result = result
            self._display_result(result)
            self._btn_export.setEnabled(True)

            # Guardar en historial
            record = HistoryRecord.create_now(
                module=self._get_module_name(),
                method=self._get_method_name(),
                parameters=self._get_parameters(),
                result_summary=result.get("message", ""),
            )
            self._history_repo.save(record)

        except ValueError as error:
            QMessageBox.warning(self, "Error de Validación", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error de Cálculo", f"Ocurrió un error inesperado:\n{error}")

    def _on_load_example(self):
        try:
            self._load_example()
        except Exception as error:
            QMessageBox.warning(self, "Error", f"No se pudo cargar el ejemplo:\n{error}")

    def _on_clear(self):
        self._clear_form()
        self._results_card.setVisible(False)
        self._results_summary_card.setVisible(False)
        self._last_result = None
        self._btn_export.setEnabled(False)
        self._plot_widget.clear()

    def _on_export_pdf(self):
        if not self._last_result:
            QMessageBox.warning(self, "Sin datos", "Primero debe realizar un cálculo.")
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Guardar Reporte PDF", "", "PDF (*.pdf)"
        )
        if not filepath:
            return

        try:
            # Generar imagen temporal de la gráfica
            chart_path = None
            if self._last_result.get("x_plot"):
                chart_path = os.path.join(tempfile.gettempdir(), "chart_export.png")
                self._plot_widget.figure.savefig(chart_path, dpi=150, bbox_inches="tight")

            gen = PdfGenerator()
            output = gen.generate_report(
                method_name=self._get_method_name(),
                parameters=self._get_parameters(),
                procedure_text="\n".join(self._last_result.get("procedure_steps", [])),
                table_headers=self._last_result.get("table_headers", []),
                table_rows=self._last_result.get("table_rows", []),
                result_summary=self._last_result.get("message", ""),
                observations=self._last_result.get("observations", ""),
                chart_image_path=chart_path,
                output_path=filepath,
            )
            QMessageBox.information(self, "Éxito", f"Reporte guardado en:\n{output}")
        except Exception as error:
            QMessageBox.critical(self, "Error al exportar", str(error))

    # ── Display ────────────────────────────────────────────────────

    def _display_result(self, result: dict):
        """Muestra los resultados en la UI."""
        self._results_card.setVisible(True)
        self._results_summary_card.setVisible(True)

        # Resumen
        msg = result.get("message", "")
        converged = result.get("converged", True)
        color = ThemeManager.colors().SUCCESS if converged else ThemeManager.colors().DANGER
        self._result_summary_label.setText(msg)
        self._result_summary_label.setStyleSheet(f"color: {color}; font-weight: 600;")

        # Polinomio Matemático
        if poly_math := result.get("polynomial_math"):
            self._result_math_canvas._expr.clear()
            nodes = build_ast_from_text(poly_math)
            for node in nodes:
                self._result_math_canvas._expr.root_slot.insert(
                    len(self._result_math_canvas._expr.root_slot), node
                )
            self._result_math_canvas.setVisible(True)
            self._result_math_canvas.update()
        else:
            self._result_math_canvas.setVisible(False)

        # Procedimiento
        steps = result.get("procedure_steps", [])
        self._procedure_text.setPlainText("\n".join(steps))

        # Tabla
        headers = result.get("table_headers", [])
        rows = result.get("table_rows", [])
        self._result_table.setColumnCount(len(headers))
        self._result_table.setRowCount(len(rows))
        self._result_table.setHorizontalHeaderLabels(headers)
        for r, row in enumerate(rows):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self._result_table.setItem(r, c_idx, item)
        self._result_table.resizeColumnsToContents()

        # Gráfica
        if result.get("x_plot") and result.get("y_plot"):
            self._plot_widget.clear()
            colors = ThemeManager.colors().PLOT_LINE_COLORS
            self._plot_widget.axes.plot(
                result["x_plot"], result["y_plot"],
                color=colors[0], linewidth=2.5, label=result.get("plot_label", "f(x)"),
                zorder=3
            )
            # Título de la gráfica
            title = f"{self._get_method_name()}"
            if result.get("plot_label"):
                title += f" — {result['plot_label']}"
            self._plot_widget.axes.set_title(title)

            # Puntos adicionales (marcadores diamante)
            if result.get("x_points") and result.get("y_points"):
                self._plot_widget.axes.scatter(
                    result["x_points"], result["y_points"],
                    color=colors[1], zorder=5, s=80, marker='D',
                    edgecolors='white', linewidths=1.2, label="Puntos"
                )
            if result.get("highlight_x") is not None:
                self._plot_widget.axes.axvline(
                    result["highlight_x"], color=colors[1],
                    linestyle="--", alpha=0.7, label=result.get("highlight_label", "")
                )
            self._plot_widget.axes.legend()
            self._plot_widget.axes.set_xlabel(result.get("xlabel", "x"))
            self._plot_widget.axes.set_ylabel(result.get("ylabel", "y"))
            self._plot_widget.refresh()

    # ── Para sobrescribir en subclases ─────────────────────────────

    def _build_form(self) -> QWidget:
        raise NotImplementedError

    def _get_method_name(self) -> str:
        raise NotImplementedError

    def _get_module_name(self) -> str:
        raise NotImplementedError

    def _get_method_description(self) -> str:
        return ""

    def _run_calculation(self) -> dict:
        raise NotImplementedError

    def _load_example(self):
        raise NotImplementedError

    def _get_parameters(self) -> dict:
        raise NotImplementedError

    def _clear_form(self):
        """Limpia los campos del formulario. Sobrescribir según necesidad."""
        pass

    def update_theme(self):
        """Llamar cuando cambia el tema."""
        self._plot_widget.update_theme()
        # Actualizar todos los MathInput del formulario
        from ui.components.math_input import MathInput
        for math_input in self.findChildren(MathInput):
            math_input.update_theme()
