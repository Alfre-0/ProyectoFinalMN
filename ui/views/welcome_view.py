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

    def __init__(self, icon: str, name: str, description: str, parent=None):
        super().__init__(parent)
        self.module_name = name
        self.setObjectName("moduleCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(150)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(Spacing.LARGE, Spacing.LARGE, Spacing.LARGE, Spacing.LARGE)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.module_name)
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
            ("🎯", "Cálculo de Raíces", "Bisección, Newton-Raphson,\nSecante"),
            ("📐", "Interpolación", "Lagrange, Newton\n(diferencias divididas)"),
            ("🔢", "Sistemas de Ecuaciones", "Gauss-Seidel,\nFactorización LU"),
            ("∫", "Integración y Derivación", "Trapecio, Simpson,\nDiferencias Finitas"),
            ("📈", "Ecuaciones Diferenciales", "Euler,\nRunge-Kutta (RK4)"),
            ("📜", "Historial", "Consulta y reutiliza\ncálculos anteriores"),
        ]

        for idx, (icon, name, desc) in enumerate(modules):
            card = ModuleCard(icon, name, desc)
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
