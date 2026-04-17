"""
plot_widget.py — Wrapper agnóstico sobre Matplotlib embebido en PyQt6.
Si en el futuro se reemplaza Matplotlib por otra librería (ej: PyQtGraph),
solo se edita este archivo.
"""
import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QApplication, QLabel, QTabWidget
from PyQt6.QtCore import QTimer
from ui.styles.tokens import Spacing, Radius
from ui.styles.theme import ThemeManager


class CustomNavigationToolbar(NavigationToolbar2QT):
    """Toolbar de Matplotlib traducido al español."""

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        self._translate_toolbar()

    def _translate_toolbar(self):
        translator = {
            'Home': 'Inicio',
            'Reset original view': 'Restablecer vista',
            'Back': 'Atrás',
            'Back to previous view': 'Vista anterior',
            'Forward': 'Adelante',
            'Forward to next view': 'Siguiente vista',
            'Pan': 'Mover',
            'Pan axes with left mouse, zoom with right': 'Mover ejes con clic izquierdo, zoom con derecho',
            'Zoom': 'Lupa',
            'Zoom to rectangle': 'Zoom en región cuadrada',
            'Subplots': 'Márgenes',
            'Configure subplots': 'Configurar márgenes de la gráfica',
            'Customize': 'Opciones',
            'Edit axis, curve and image parameters': 'Paleta y propiedades gráficas',
            'Save': 'Guardar',
            'Save the figure': 'Guardar imagen'
        }
        for action in self.actions():
            clean = action.text().replace('&', '')
            if clean in translator:
                action.setText(translator[clean])
            if action.toolTip() in translator:
                action.setToolTip(translator[action.toolTip()])

    def configure_subplots(self):
        QTimer.singleShot(10, self._translate_subplots_dialog)
        super().configure_subplots()

    def _translate_subplots_dialog(self):
        from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QGroupBox
        win = QApplication.activeWindow()
        if not win: return
        
        win.setWindowTitle("Configuración de Márgenes")
        
        for gbox in win.findChildren(QGroupBox):
            t = gbox.title().replace("&", "")
            if "Borders" in t: gbox.setTitle("Bordes")
            elif "Spacings" in t: gbox.setTitle("Espaciados")
            
        for label in win.findChildren(QLabel):
            t = label.text().replace("&", "")
            if t == "top": label.setText("Arriba")
            elif t == "bottom": label.setText("Abajo")
            elif t == "left": label.setText("Izquierda")
            elif t == "right": label.setText("Derecha")
            elif t == "hspace": label.setText("Espaciado H")
            elif t == "wspace": label.setText("Espaciado V")
            
        for btn in win.findChildren(QPushButton):
            t = btn.text().replace("&", "")
            if t == "Tight layout": btn.setText("Autoajustar")
            elif t == "Reset": btn.setText("Reiniciar")
            elif t == "Close": btn.setText("Cerrar")
            elif t == "Export values": btn.setText("Exportar")

    def edit_parameters(self):
        QTimer.singleShot(10, self._translate_figure_options)
        super().edit_parameters()

    def _translate_figure_options(self):
        from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QTabWidget, QCheckBox
        win = QApplication.activeWindow()
        if not win: return
        
        win.setWindowTitle("Opciones de Gráfica")
        
        for tab in win.findChildren(QTabWidget):
            for i in range(tab.count()):
                t = tab.tabText(i).replace("&", "")
                if "Axes" in t: tab.setTabText(i, "Ejes")
                elif "Curves" in t: tab.setTabText(i, "Curvas")
                elif "Images" in t: tab.setTabText(i, "Imágenes")
                
        for label in win.findChildren(QLabel):
            t = label.text()
            if "X-Axis" in t: label.setText(t.replace("X-Axis", "Eje X"))
            elif "Y-Axis" in t: label.setText(t.replace("Y-Axis", "Eje Y"))
            else:
                t_clean = t.replace("&", "")
                if t_clean == "Title": label.setText("Título")
                elif t_clean == "Min": label.setText("Mínimo")
                elif t_clean == "Max": label.setText("Máximo")
                elif t_clean == "Label": label.setText("Etiqueta")
                elif t_clean == "Scale": label.setText("Escala")
                elif t_clean == "Line style": label.setText("Estilo de línea")
                elif t_clean == "Draw style": label.setText("Estilo de dibujo")
                elif t_clean == "Width": label.setText("Grosor")
                elif t_clean == "Color (RGBA)": label.setText("Color (RGBA)")
                elif t_clean == "Marker": label.setText("Marcador")
                elif t_clean == "Size": label.setText("Tamaño")
                elif t_clean == "Facecolor": label.setText("Color de Relleno")
                elif t_clean == "Edgecolor": label.setText("Color de Borde")

        for cb in win.findChildren(QCheckBox):
            if "(Re-)Generate" in cb.text():
                cb.setText("Generar leyenda activamente")

        for btn in win.findChildren(QPushButton):
            t = btn.text().replace("&", "")
            if t == "OK": btn.setText("Aceptar")
            elif t == "Cancel": btn.setText("Cancelar")
            elif t == "Apply": btn.setText("Aplicar")


class PlotWidget(QFrame):
    """Widget reutilizable para mostrar gráficas Matplotlib dentro de la app."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = CustomNavigationToolbar(self.canvas, self)
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

        # Tick labels
        self.axes.tick_params(
            colors=c.TEXT_PRIMARY, labelsize=10, width=1.2,
            direction='out', length=4
        )

        # Axis labels
        self.axes.xaxis.label.set_color(c.TEXT_PRIMARY)
        self.axes.xaxis.label.set_fontsize(12)
        self.axes.xaxis.label.set_fontweight('bold')
        self.axes.yaxis.label.set_color(c.TEXT_PRIMARY)
        self.axes.yaxis.label.set_fontsize(12)
        self.axes.yaxis.label.set_fontweight('bold')

        # Title
        self.axes.title.set_color(c.TEXT_PRIMARY)
        self.axes.title.set_fontsize(13)
        self.axes.title.set_fontweight('bold')

        # Spines
        for spine in self.axes.spines.values():
            spine.set_color(c.BORDER)
            spine.set_linewidth(1.2)

        # Grid
        self.axes.grid(
            True, color=c.PLOT_GRID, linestyle='-', alpha=0.4, linewidth=0.8
        )
        self.axes.set_axisbelow(True)

    def clear(self):
        """Limpia el gráfico y reaplica el tema."""
        self.axes.clear()
        self._apply_theme()
        self.canvas.draw()

    def refresh(self):
        """Redibuja el canvas después de modificar axes externamente."""
        self._apply_theme()
        self.figure.tight_layout(pad=1.5)
        self.canvas.draw()

    def update_theme(self):
        """Llamar al cambiar de tema para reaplicar colores."""
        self._apply_theme()
        self.figure.tight_layout(pad=1.5)
        self.canvas.draw()
