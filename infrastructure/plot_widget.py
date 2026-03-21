"""
plot_widget.py — Wrapper agnóstico sobre Matplotlib embebido en PyQt6.
Si en el futuro se reemplaza Matplotlib por otra librería (ej: PyQtGraph),
solo se edita este archivo.
"""
import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from ui.styles.tokens import Spacing, Radius
from ui.styles.theme import ThemeManager


class PlotWidget(QFrame):
    """Widget reutilizable para mostrar gráficas Matplotlib dentro de la app."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.axes = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            Spacing.SMALL, Spacing.SMALL, Spacing.SMALL, Spacing.SMALL
        )
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self._apply_theme()

    def _apply_theme(self):
        """Aplica los colores del tema actual al gráfico."""
        c = ThemeManager.colors()
        self.figure.set_facecolor(c.PLOT_BG)
        self.axes.set_facecolor(c.PLOT_BG)
        self.axes.tick_params(colors=c.TEXT_PRIMARY)
        self.axes.xaxis.label.set_color(c.TEXT_PRIMARY)
        self.axes.yaxis.label.set_color(c.TEXT_PRIMARY)
        self.axes.title.set_color(c.TEXT_PRIMARY)
        for spine in self.axes.spines.values():
            spine.set_color(c.BORDER)
        self.axes.grid(True, color=c.PLOT_GRID, linestyle="--", alpha=0.5)

    def clear(self):
        """Limpia el gráfico y reaplica el tema."""
        self.axes.clear()
        self._apply_theme()
        self.canvas.draw()

    def refresh(self):
        """Redibuja el canvas después de modificar axes externamente."""
        self._apply_theme()
        self.figure.tight_layout()
        self.canvas.draw()

    def update_theme(self):
        """Llamar al cambiar de tema para reaplicar colores."""
        self._apply_theme()
        self.figure.tight_layout()
        self.canvas.draw()
