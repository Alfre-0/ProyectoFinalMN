"""
history_view.py — Vista del historial de cálculos realizados.
Permite consultar, recargar y eliminar registros.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QMessageBox, QScrollArea,
    QHeaderView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles.tokens import Spacing, Typography
from infrastructure.history_repo import HistoryRepository


class HistoryView(QWidget):
    """Panel de historial de cálculos."""

    record_selected = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._repo = HistoryRepository()
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.LARGE)
        layout.setSpacing(Spacing.LARGE)

        header = QLabel("📜 Historial de Cálculos")
        header.setObjectName("heading")
        layout.addWidget(header)

        subtitle = QLabel("Consulta, recarga o elimina cálculos anteriores.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        # Botones
        btn_row = QHBoxLayout()
        self._btn_refresh = QPushButton("🔄  Actualizar")
        self._btn_refresh.setObjectName("secondaryButton")
        self._btn_refresh.clicked.connect(self.refresh)

        self._btn_clear = QPushButton("🗑  Limpiar Todo")
        self._btn_clear.setObjectName("dangerButton")
        self._btn_clear.clicked.connect(self._on_clear_all)

        btn_row.addWidget(self._btn_refresh)
        btn_row.addStretch()
        btn_row.addWidget(self._btn_clear)
        layout.addLayout(btn_row)

        # Tabla
        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels([
            "Fecha/Hora", "Módulo", "Método", "Resultado", "Acciones"
        ])
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setAlternatingRowColors(True)
        layout.addWidget(self._table)

    def refresh(self):
        """Recarga los datos del historial."""
        records = self._repo.load_all()
        self._table.setRowCount(len(records))

        for row, record in enumerate(records):
            self._table.setItem(row, 0, QTableWidgetItem(record.timestamp))
            self._table.setItem(row, 1, QTableWidgetItem(record.module))
            self._table.setItem(row, 2, QTableWidgetItem(record.method))
            self._table.setItem(row, 3, QTableWidgetItem(record.result_summary[:80]))

            delete_btn = QPushButton("❌")
            delete_btn.setFixedWidth(40)
            delete_btn.setToolTip("Eliminar este registro")
            delete_btn.clicked.connect(lambda checked, idx=row: self._on_delete(idx))
            
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(delete_btn)
            
            self._table.setCellWidget(row, 4, btn_container)

        self._table.resizeColumnsToContents()
        self._table.resizeRowsToContents()

    def _on_delete(self, index: int):
        reply = QMessageBox.question(
            self, "Confirmar", "¿Eliminar este registro del historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._repo.delete(index)
            self.refresh()

    def _on_clear_all(self):
        reply = QMessageBox.question(
            self, "Confirmar", "¿Eliminar TODO el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._repo.clear_all()
            self.refresh()
