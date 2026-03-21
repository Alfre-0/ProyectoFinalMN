"""
theme.py — Gestor de temas claro/oscuro.
Genera hojas de estilos QSS dinámicas a partir de los tokens.
"""
from ui.styles.tokens import Colors, ColorsDark, Spacing, Radius, Typography


class ThemeManager:
    """Singleton-like que gestiona el tema actual de la aplicación."""

    _is_dark = False

    @classmethod
    def is_dark(cls) -> bool:
        return cls._is_dark

    @classmethod
    def toggle(cls):
        cls._is_dark = not cls._is_dark

    @classmethod
    def set_dark(cls, dark: bool):
        cls._is_dark = dark

    @classmethod
    def colors(cls):
        return ColorsDark if cls._is_dark else Colors

    @classmethod
    def stylesheet(cls) -> str:
        """Genera la hoja de estilos global basada en el tema activo."""
        c = cls.colors()
        return f"""
        /* ── Base global ─────────────────────────── */
        QMainWindow, QWidget#centralWidget {{
            background-color: {c.BACKGROUND};
        }}

        QLabel {{
            color: {c.TEXT_PRIMARY};
            font-size: {Typography.BODY}pt;
        }}

        QLabel#sectionTitle {{
            font-size: {Typography.TITLE}pt;
            font-weight: 700;
            color: {c.TEXT_PRIMARY};
        }}

        QLabel#subtitle {{
            font-size: {Typography.SUBTITLE}pt;
            color: {c.TEXT_SECONDARY};
        }}

        QLabel#heading {{
            font-size: {Typography.HEADING}pt;
            font-weight: 700;
            color: {c.TEXT_PRIMARY};
        }}

        /* ── Inputs ──────────────────────────────── */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            background-color: {c.SURFACE};
            color: {c.TEXT_PRIMARY};
            border: 1px solid {c.BORDER};
            border-radius: {Radius.MEDIUM}px;
            padding: {Spacing.SMALL}px {Spacing.MEDIUM}px;
            font-size: {Typography.BODY}pt;
            min-height: 28px;
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border: 2px solid {c.BORDER_FOCUS};
        }}

        QComboBox::drop-down {{
            border: none;
            padding-right: {Spacing.SMALL}px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {c.SURFACE};
            color: {c.TEXT_PRIMARY};
            border: 1px solid {c.BORDER};
            selection-background-color: {c.PRIMARY_LIGHT};
            selection-color: {c.TEXT_PRIMARY};
        }}

        /* ── Botón primario ──────────────────────── */
        QPushButton {{
            background-color: {c.PRIMARY};
            color: {c.TEXT_ON_PRIMARY};
            border: none;
            border-radius: {Radius.MEDIUM}px;
            padding: {Spacing.SMALL}px {Spacing.LARGE}px;
            font-weight: 600;
            font-size: {Typography.BODY}pt;
            min-height: 32px;
        }}
        QPushButton:hover {{
            background-color: {c.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {c.PRIMARY_PRESSED};
        }}

        QPushButton#secondaryButton {{
            background-color: transparent;
            color: {c.PRIMARY};
            border: 1px solid {c.PRIMARY};
        }}
        QPushButton#secondaryButton:hover {{
            background-color: {c.PRIMARY_LIGHT};
        }}

        QPushButton#dangerButton {{
            background-color: {c.DANGER};
        }}
        QPushButton#dangerButton:hover {{
            background-color: #C0392B;
        }}

        QPushButton#accentButton {{
            background-color: {c.ACCENT};
        }}
        QPushButton#accentButton:hover {{
            background-color: {c.ACCENT_HOVER};
        }}

        /* ── ToolBar (Matplotlib) ────────────────── */
        QToolButton {{
            background-color: transparent;
            color: {c.TEXT_PRIMARY};
            border-radius: {Radius.SMALL}px;
            padding: {Spacing.SMALL}px;
        }}
        QToolButton:hover {{
            background-color: {c.SURFACE_ALT};
        }}

        /* ── Tablas ──────────────────────────────── */
        QTableWidget {{
            background-color: {c.SURFACE};
            alternate-background-color: {c.SURFACE_ALT};
            selection-background-color: {c.PRIMARY};
            selection-color: {c.TEXT_ON_PRIMARY};
            color: {c.TEXT_PRIMARY};
            border: 1px solid {c.BORDER};
            border-radius: {Radius.MEDIUM}px;
            gridline-color: {c.BORDER};
            font-size: {Typography.BODY}pt;
        }}
        QTableWidget::item {{
            padding: {Spacing.SMALL}px;
        }}
        QTableWidget::item:selected {{
            background-color: {c.PRIMARY};
            color: {c.TEXT_ON_PRIMARY};
        }}
        QHeaderView::section {{
            background-color: {c.SURFACE_ALT};
            color: {c.TEXT_PRIMARY};
            font-weight: 600;
            padding: {Spacing.SMALL}px;
            border: none;
            border-bottom: 2px solid {c.PRIMARY};
        }}

        /* ── ScrollArea ──────────────────────────── */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background-color: {c.BORDER};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {c.TEXT_MUTED};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
            height: 0px;
        }}

        /* ── Tarjetas / Paneles ──────────────────── */
        QFrame#card {{
            background-color: {c.SURFACE};
            border: 1px solid {c.BORDER};
            border-radius: {Radius.LARGE}px;
        }}

        QFrame#moduleCard {{
            background-color: {c.SURFACE};
            border: 1px solid {c.BORDER};
            border-radius: {Radius.LARGE}px;
        }}
        QFrame#moduleCard:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {c.PRIMARY_LIGHT}, stop:1 {c.SURFACE});
            border: 1px solid {c.PRIMARY};
        }}

        /* ── TextEdit (procedimiento) ────────────── */
        QTextEdit {{
            background-color: {c.SURFACE};
            color: {c.TEXT_PRIMARY};
            border: 1px solid {c.BORDER};
            border-radius: {Radius.MEDIUM}px;
            padding: {Spacing.MEDIUM}px;
            font-size: {Typography.BODY}pt;
        }}

        /* ── Tooltips ────────────────────────────── */
        QToolTip {{
            background-color: {c.SURFACE};
            color: {c.TEXT_PRIMARY};
            border: 1px solid {c.BORDER};
            padding: {Spacing.SMALL}px;
            border-radius: {Radius.SMALL}px;
        }}

        /* ── Tab Widget ──────────────────────────── */
        QTabWidget::pane {{
            border: 1px solid {c.BORDER};
            border-radius: {Radius.MEDIUM}px;
            background-color: {c.SURFACE};
        }}
        QTabBar::tab {{
            background-color: {c.SURFACE_ALT};
            color: {c.TEXT_SECONDARY};
            padding: {Spacing.SMALL}px {Spacing.LARGE}px;
            border-top-left-radius: {Radius.MEDIUM}px;
            border-top-right-radius: {Radius.MEDIUM}px;
            margin-right: 2px;
            font-weight: 500;
        }}
        QTabBar::tab:selected {{
            background-color: {c.SURFACE};
            color: {c.PRIMARY};
            border-bottom: 2px solid {c.PRIMARY};
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {c.PRIMARY_LIGHT};
        }}
        """
