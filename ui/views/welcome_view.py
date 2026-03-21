"""
welcome_view.py — Vista de bienvenida / pantalla de inicio.
Muestra información general sobre la aplicación.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles.tokens import Spacing, Typography
from ui.styles.theme import ThemeManager


class ModuleCard(QFrame):
    """Tarjeta interactiva para cada módulo en la pantalla de inicio."""
    clicked = pyqtSignal(str)

    def __init__(self, icon: str, name: str, description: str, sidebar_key: str, parent=None):
        super().__init__(parent)
        self.sidebar_key = sidebar_key
        self.setObjectName("moduleCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        from PyQt6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.setMinimumHeight(220)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(Spacing.LARGE, Spacing.LARGE, Spacing.LARGE, Spacing.LARGE)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: {Typography.DISPLAY}pt; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        name_label = QLabel(name)
        name_label.setObjectName("sectionTitle")
        name_label.setStyleSheet("background: transparent;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("subtitle")
        desc_label.setStyleSheet("background: transparent;")
        desc_label.setTextFormat(Qt.TextFormat.RichText)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        desc_label.setWordWrap(True)
        desc_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        card_layout.addWidget(desc_label)
        
        card_layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.sidebar_key)
        super().mousePressEvent(event)


class WelcomeView(QWidget):
    """Pantalla de bienvenida que se muestra al iniciar la aplicación."""
    module_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.SECTION, Spacing.SECTION, Spacing.SECTION, Spacing.SECTION)
        layout.setSpacing(Spacing.XL)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título principal
        title = QLabel("🧮  Métodos Numéricos")
        title.setObjectName("heading")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: {Typography.DISPLAY}pt; font-weight: 800;")
        layout.addWidget(title)

        subtitle = QLabel("Herramienta académica para resolución de problemas numéricos")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"font-size: {Typography.TITLE}pt;")
        layout.addWidget(subtitle)

        layout.addSpacing(Spacing.XL)

        # Grid de módulos
        grid = QGridLayout()
        grid.setSpacing(Spacing.LARGE)

        modules = [
            ("🎯", "Cálculo de Raíces", 
             "Encuentra los interceptos en x (raíces) de funciones algebraicas y trascendentes. "
             "Verifica con tablas de iteración y gráficas que muestran el comportamiento del error.<br><br>"
             "<b>Métodos:</b> Bisección, Newton-Raphson, Secante", "Raíces"),
            
            ("📐", "Interpolación", 
             "Construye polinomios que pasan exactamente por un conjunto de puntos dados "
             "y te permite estimar valores exactos dentro de un intervalo específico.<br><br>"
             "<b>Métodos:</b> Lagrange, Newton (diferencias divididas)", "Interpolación"),
            
            ("🔢", "Sistemas de Ecuaciones", 
             "Resuelve sistemas matriciales lineales del tipo Ax = b, detallando el proceso de reducción o iteración "
             "para encontrar las incógnitas dependientes.<br><br>"
             "<b>Métodos:</b> Gauss-Seidel, Factorización LU", "Sistemas"),
            
            ("∫", "Integración y Derivación", 
             "Aproxima el área bajo la curva (integración) o la tasa de cambio (deriva) "
             "mediante discretización y fórmulas exactas de subintervalos estandarizados.<br><br>"
             "<b>Métodos:</b> Trapecio, Simpson, Punto Medio", "Integración"),
            
            ("📈", "Ecuaciones Diferenciales", 
             "Aproxima soluciones de problemas de valor inicial (PVI) paso a paso, "
             "estimando los valores continuos de la ecuación diferencial en el tiempo.<br><br>"
             "<b>Métodos:</b> Euler, Runge-Kutta (RK4)", "EDOs"),
            
            ("📜", "Historial", 
             "Consulta todos tus cálculos anteriores. Puedes cargar y reutilizar resultados pasados "
             "sin tener que reescribir nuevamente todas las ecuaciones o matrices.", "Historial"),
        ]

        for idx, (icon, name, desc, key) in enumerate(modules):
            card = ModuleCard(icon, name, desc, key)
            card.clicked.connect(self.module_selected.emit)
            row = idx // 3
            col = idx % 3
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()

        # Footer
        footer = QLabel("Selecciona un módulo arriba o del menú lateral para comenzar →")
        footer.setObjectName("subtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
