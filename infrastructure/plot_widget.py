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
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QPushButton
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

        zoom_layout = QHBoxLayout()
        btn_zoom_in = QPushButton("🔍 +")
        btn_zoom_in.setToolTip("Acercar gráfica")
        btn_zoom_in.clicked.connect(lambda: self.zoom(1.5))
        
        btn_zoom_out = QPushButton("🔍 -")
        btn_zoom_out.setToolTip("Alejar gráfica")
        btn_zoom_out.clicked.connect(lambda: self.zoom(1/1.5))

        # Opcional: estilizar los botones de zoom para que no sean tan invasivos
        style = "QPushButton { padding: 4px; font-weight: bold; border-radius: 4px; max-width: 40px; }"
        btn_zoom_in.setStyleSheet(style)
        btn_zoom_out.setStyleSheet(style)

        zoom_layout.addWidget(self.toolbar)
        zoom_layout.addStretch()
        zoom_layout.addWidget(btn_zoom_in)
        zoom_layout.addWidget(btn_zoom_out)

        layout.addLayout(zoom_layout)
        layout.addWidget(self.canvas)

        self._apply_theme()

    def zoom(self, factor: float):
        """Aplica un zoom (factor > 1 acerca, factor < 1 aleja)."""
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        
        x_c = (xlim[0] + xlim[1]) / 2
        y_c = (ylim[0] + ylim[1]) / 2
        
        x_r = (xlim[1] - xlim[0]) / factor
        y_r = (ylim[1] - ylim[0]) / factor
        
        self.axes.set_xlim([x_c - x_r/2, x_c + x_r/2])
        self.axes.set_ylim([y_c - y_r/2, y_c + y_r/2])
        self.canvas.draw()

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
