"""
main_window.py — Ventana principal de la aplicación.
Responsabilidad: organizar el sidebar de navegación y el panel central dinámico.
No contiene lógica matemática — solo orquestación de vistas.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QSizePolicy, QScrollArea,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from ui.styles.tokens import Colors, ColorsDark, Spacing, Typography, Radius
from ui.styles.theme import ThemeManager

# Importar vistas
from ui.views.welcome_view import WelcomeView
from ui.views.raices_views import BiseccionView, NewtonRaphsonView, SecanteView
from ui.views.interpolacion_views import LagrangeView, NewtonInterpolacionView
from ui.views.sistemas_views import GaussSeidelView, FactorizacionLUView
from ui.views.integracion_views import DiferenciasFinitasView, TrapecioView, SimpsonView
from ui.views.edos_views import EulerView, RungeKuttaView
from ui.views.history_view import HistoryView


# ── Datos de navegación ──────────────────────────────────────────

SIDEBAR_MODULES = [
    {
        "icon": "🏠",
        "label": "Inicio",
        "methods": [],
        "view_key": "welcome",
    },
    {
        "icon": "🎯",
        "label": "Raíces",
        "methods": [
            {"label": "Bisección", "view_key": "biseccion"},
            {"label": "Newton-Raphson", "view_key": "newton_raphson"},
            {"label": "Secante", "view_key": "secante"},
        ],
    },
    {
        "icon": "📐",
        "label": "Interpolación",
        "methods": [
            {"label": "Lagrange", "view_key": "lagrange"},
            {"label": "Newton", "view_key": "newton_interp"},
        ],
    },
    {
        "icon": "🔢",
        "label": "Sistemas",
        "methods": [
            {"label": "Gauss-Seidel", "view_key": "gauss_seidel"},
            {"label": "Factorización LU", "view_key": "lu"},
        ],
    },
    {
        "icon": "∫",
        "label": "Integración",
        "methods": [
            {"label": "Dif. Finitas", "view_key": "dif_finitas"},
            {"label": "Trapecio", "view_key": "trapecio"},
            {"label": "Simpson", "view_key": "simpson"},
        ],
    },
    {
        "icon": "📈",
        "label": "EDOs",
        "methods": [
            {"label": "Euler", "view_key": "euler"},
            {"label": "Runge-Kutta", "view_key": "runge_kutta"},
        ],
    },
    {
        "icon": "📜",
        "label": "Historial",
        "methods": [],
        "view_key": "history",
    },
]


class SidebarButton(QPushButton):
    """Botón personalizado para el sidebar con soporte de estado activo."""

    def __init__(self, text: str, icon_text: str = "", parent=None):
        display = f"  {icon_text}  {text}" if icon_text else f"  {text}"
        super().__init__(display, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._is_submenu = not bool(icon_text)
        self._update_style(False)

    def _update_style(self, active: bool):
        c = ThemeManager.colors()
        if active:
            bg = c.SIDEBAR_ITEM_ACTIVE
            fg = c.TEXT_SIDEBAR_ACTIVE
            weight = "700"
        else:
            bg = "transparent"
            fg = c.TEXT_SIDEBAR
            weight = "400"

        padding_left = 40 if self._is_submenu else 8
        font_size = Typography.CAPTION if self._is_submenu else Typography.BODY

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: none;
                border-radius: {Radius.MEDIUM}px;
                text-align: left;
                padding-left: {padding_left}px;
                font-size: {font_size}pt;
                font-weight: {weight};
                background-clip: border;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c.SIDEBAR_ITEM_HOVER}, stop:1 transparent);
                border-left: 3px solid {c.PRIMARY if not active else "transparent"};
            }}
        """)

    def set_active(self, active: bool):
        self.setChecked(active)
        self._update_style(active)

    def update_theme(self):
        self._update_style(self.isChecked())


class MainWindow(QMainWindow):
    """Ventana principal con sidebar de navegación y panel central dinámico."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Métodos Numéricos — Herramienta Académica")
        self.setMinimumSize(1100, 700)
        self.resize(1300, 800)

        self._sidebar_buttons: list[SidebarButton] = []
        self._module_menu_buttons: dict[str, SidebarButton] = {}
        self._current_active_button: SidebarButton | None = None

        self._setup_views()
        self._setup_ui()
        self._apply_theme()

        # Mostrar vista de bienvenida
        self._navigate_to("welcome")

    def _setup_views(self):
        """Registra todas las vistas por clave."""
        welcome = WelcomeView()
        welcome.module_selected.connect(self.expand_sidebar_menu)
        
        self._views: dict[str, QWidget] = {
            "welcome": welcome,
            "biseccion": BiseccionView(),
            "newton_raphson": NewtonRaphsonView(),
            "secante": SecanteView(),
            "lagrange": LagrangeView(),
            "newton_interp": NewtonInterpolacionView(),
            "gauss_seidel": GaussSeidelView(),
            "lu": FactorizacionLUView(),
            "dif_finitas": DiferenciasFinitasView(),
            "trapecio": TrapecioView(),
            "simpson": SimpsonView(),
            "euler": EulerView(),
            "runge_kutta": RungeKuttaView(),
            "history": HistoryView(),
        }

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──
        sidebar = self._build_sidebar()
        main_layout.addWidget(sidebar)

        # ── Panel central (stacked) ──
        self._stack = QStackedWidget()
        for key, view in self._views.items():
            self._stack.addWidget(view)
        main_layout.addWidget(self._stack, 1)

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(
            Spacing.MEDIUM, Spacing.LARGE, Spacing.MEDIUM, Spacing.MEDIUM
        )
        sidebar_layout.setSpacing(Spacing.TINY)

        # Logo / Título
        logo_label = QLabel("🧮")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet(f"font-size: {Typography.DISPLAY}pt; padding: {Spacing.MEDIUM}px;")
        sidebar_layout.addWidget(logo_label)

        app_title = QLabel("Métodos\nNuméricos")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_title.setStyleSheet(
            f"font-size: {Typography.TITLE}pt; font-weight: 700; "
            f"padding-bottom: {Spacing.LARGE}px;"
        )
        sidebar_layout.addWidget(app_title)

        # Separador
        separator = QFrame()
        separator.setFixedHeight(1)
        sidebar_layout.addWidget(separator)
        sidebar_layout.addSpacing(Spacing.SMALL)

        # Scroll area para los botones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(2)

        for module in SIDEBAR_MODULES:
            # Botón principal del módulo
            view_key = module.get("view_key")
            methods = module.get("methods", [])

            btn = SidebarButton(str(module["label"]), str(module.get("icon", "")))
            self._sidebar_buttons.append(btn)
            self._module_menu_buttons[str(module["label"])] = btn

            if view_key and not methods:
                # Módulo sin submenú (acceso directo: Inicio, Historial)
                btn.clicked.connect(
                    lambda checked, vk=view_key, b=btn: self._on_sidebar_click(vk, b)
                )
            elif methods:
                # Módulo con submenú: click expande/colapsa
                sub_buttons = []
                sub_container = QWidget()
                sub_layout = QVBoxLayout(sub_container)
                sub_layout.setContentsMargins(0, 0, 0, 0)
                sub_layout.setSpacing(2)

                for method in methods:
                    sub_btn = SidebarButton(method["label"])
                    sub_btn.clicked.connect(
                        lambda checked, vk=method["view_key"], b=sub_btn: self._on_sidebar_click(vk, b)
                    )
                    sub_layout.addWidget(sub_btn)
                    self._sidebar_buttons.append(sub_btn)
                    sub_buttons.append(sub_btn)

                sub_container.setVisible(False)
                btn.clicked.connect(
                    lambda checked, sc=sub_container: sc.setVisible(not sc.isVisible())
                )

            scroll_layout.addWidget(btn)
            if methods:
                scroll_layout.addWidget(sub_container)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        sidebar_layout.addWidget(scroll, 1)

        # ── Tema toggle (parte inferior del sidebar) ──
        sidebar_layout.addSpacing(Spacing.SMALL)

        theme_separator = QFrame()
        theme_separator.setFixedHeight(1)
        sidebar_layout.addWidget(theme_separator)

        self._theme_btn = QPushButton("🌙  Modo Oscuro")
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.setFixedHeight(36)
        self._theme_btn.clicked.connect(self._toggle_theme)
        sidebar_layout.addWidget(self._theme_btn)

        self._sidebar_frame = sidebar
        return sidebar

    def _on_sidebar_click(self, view_key: str, button: SidebarButton):
        """Navega a la vista seleccionada y actualiza el estado visual."""
        self._navigate_to(view_key)

        # Desactivar todos
        for btn in self._sidebar_buttons:
            btn.set_active(False)

        button.set_active(True)
        self._current_active_button = button

        # Si es historial, refrescar
        if view_key == "history":
            self._views["history"].refresh()

    def expand_sidebar_menu(self, module_label: str):
        """Abre (expande) el submenú de un módulo en la barra lateral."""
        if module_label in self._module_menu_buttons:
            btn = self._module_menu_buttons[module_label]
            # Emitir click si no está ya expandido, o forzar su apertura si es posible
            btn.click()

    def _navigate_to(self, view_key: str):
        """Cambia la vista central activa."""
        view = self._views.get(view_key)
        if view:
            self._stack.setCurrentWidget(view)

    def _toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        ThemeManager.toggle()
        self._apply_theme()

    def _apply_theme(self):
        """Aplica el tema actual a toda la aplicación."""
        c = ThemeManager.colors()

        # Stylesheet global
        self.setStyleSheet(ThemeManager.stylesheet())

        # Sidebar styling
        self._sidebar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {c.SIDEBAR_BG};
            }}
            QLabel {{
                color: {c.TEXT_SIDEBAR_ACTIVE};
            }}
        """)

        # Actualizar botones del sidebar
        for btn in self._sidebar_buttons:
            btn.update_theme()

        # Tema del botón toggle
        is_dark = ThemeManager.is_dark()
        self._theme_btn.setText("☀️  Modo Claro" if is_dark else "🌙  Modo Oscuro")
        self._theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c.SIDEBAR_ITEM_HOVER};
                color: {c.TEXT_SIDEBAR_ACTIVE};
                border: none;
                border-radius: {Radius.MEDIUM}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {c.SIDEBAR_ITEM_ACTIVE};
            }}
        """)

        # Actualizar gráficas de todas las vistas
        for key, view in self._views.items():
            if hasattr(view, "update_theme"):
                view.update_theme()
