"""
math_keyboard.py — Teclado virtual matemático con pestañas categorizadas.
Inspirado en el diseño de GeoGebra. Emite señales de acción
que el MathCanvas procesa para modificar el AST.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTabWidget, QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from ui.styles.tokens import Spacing, Typography, Radius
from ui.styles.theme import ThemeManager


# ── Definición de teclas ──────────────────────────────────────────
# (label, action, data, style_class)
# action: 'char','constant','power','power_squared','sqrt','fraction',
#          'function','left','right','backspace','open_paren','close_paren'
# style_class: 'variable','number','operator','function','constant',
#              'action','nav','disabled'

_SEP = None  # Marcador de separador visual

TAB_123 = [
    [('x', 'char', 'x', 'variable'), ('y', 'char', 'y', 'variable'),
     ('z', 'char', 'z', 'variable'), ('π', 'constant', 'π', 'constant'),
     _SEP,
     ('7', 'char', '7', 'number'), ('8', 'char', '8', 'number'),
     ('9', 'char', '9', 'number'), ('×', 'char', '×', 'operator'),
     ('÷', 'char', '÷', 'operator')],

    [('x²', 'power_squared', '', 'function'), ('xⁿ', 'power', '', 'function'),
     ('√', 'sqrt', '', 'function'), ('e', 'constant', 'e', 'constant'),
     _SEP,
     ('4', 'char', '4', 'number'), ('5', 'char', '5', 'number'),
     ('6', 'char', '6', 'number'), ('+', 'char', '+', 'operator'),
     ('−', 'char', '-', 'operator')],

    [('a/b', 'fraction', '', 'function'), ('|x|', 'function', 'abs', 'function'),
     (' ', None, '', 'disabled'), (' ', None, '', 'disabled'),
     _SEP,
     ('1', 'char', '1', 'number'), ('2', 'char', '2', 'number'),
     ('3', 'char', '3', 'number'), ('=', 'char', '=', 'operator'),
     ('⌫', 'backspace', '', 'action')],

    [('(', 'open_paren', '', 'variable'), (')', 'close_paren', '', 'variable'),
     (',', 'char', ',', 'variable'), ('.', 'char', '.', 'variable'),
     _SEP,
     ('0', 'char', '0', 'number'), (' ', None, '', 'disabled'),
     (' ', None, '', 'disabled'),
     ('◀', 'left', '', 'nav'), ('▶', 'right', '', 'nav')],
]

TAB_FX = [
    [('sin', 'function', 'sin', 'function'), ('cos', 'function', 'cos', 'function'),
     ('tan', 'function', 'tan', 'function'), ('asin', 'function', 'asin', 'function')],
    [('acos', 'function', 'acos', 'function'), ('atan', 'function', 'atan', 'function'),
     ('ln', 'function', 'ln', 'function'), ('log', 'function', 'log', 'function')],
    [('exp', 'function', 'exp', 'function'), ('|x|', 'function', 'abs', 'function'),
     ('x²', 'power_squared', '', 'function'), ('√', 'sqrt', '', 'function')],
    [('xⁿ', 'power', '', 'function'), ('a/b', 'fraction', '', 'function'),
     ('π', 'constant', 'π', 'constant'), ('e', 'constant', 'e', 'constant')],
]

TAB_ABC = [
    [('a', 'char', 'a', 'variable'), ('b', 'char', 'b', 'variable'),
     ('c', 'char', 'c', 'variable'), ('d', 'char', 'd', 'variable'),
     ('f', 'char', 'f', 'variable'), ('g', 'char', 'g', 'variable'),
     ('h', 'char', 'h', 'variable')],
    [('i', 'char', 'i', 'variable'), ('j', 'char', 'j', 'variable'),
     ('k', 'char', 'k', 'variable'), ('n', 'char', 'n', 'variable'),
     ('m', 'char', 'm', 'variable'), ('p', 'char', 'p', 'variable'),
     ('t', 'char', 't', 'variable')],
    [('x', 'char', 'x', 'variable'), ('y', 'char', 'y', 'variable'),
     ('z', 'char', 'z', 'variable'), ('r', 'char', 'r', 'variable'),
     ('s', 'char', 's', 'variable'), ('u', 'char', 'u', 'variable'),
     ('v', 'char', 'v', 'variable')],
]

TAB_SYM = [
    [('≤', 'char', '≤', 'operator'), ('≥', 'char', '≥', 'operator'),
     ('≠', 'char', '≠', 'operator'), ('<', 'char', '<', 'operator')],
    [('>', 'char', '>', 'operator'), ('∞', 'char', '∞', 'constant'),
     (' ', None, '', 'disabled'), (' ', None, '', 'disabled')],
]


class MathKeyboardButton(QPushButton):
    """Botón individual del teclado matemático con estilo por categoría."""

    def __init__(self, label: str, style_class: str = 'number', parent=None):
        super().__init__(label, parent)
        self._style_class = style_class
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMinimumSize(QSize(30, 32))
        self.setMaximumHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._apply_style()

    def _apply_style(self):
        c = ThemeManager.colors()
        is_dark = ThemeManager.is_dark()

        palettes = {
            'number':   (c.SURFACE, c.TEXT_PRIMARY, '600'),
            'variable': (c.SURFACE_ALT, c.PRIMARY, '600'),
            'operator': (c.SURFACE_ALT, c.DANGER, '700'),
            'function': (c.PRIMARY_LIGHT, c.PRIMARY, '600'),
            'constant': (c.PRIMARY_LIGHT, c.ACCENT, '700'),
            'action':   ('#3A2020' if is_dark else '#FFE0E0', c.DANGER, '700'),
            'nav':      (c.PRIMARY, '#FFFFFF', '700'),
            'disabled': (c.SURFACE_ALT, c.TEXT_MUTED, '400'),
        }
        bg, fg, weight = palettes.get(self._style_class, palettes['number'])

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {c.BORDER};
                border-radius: {Radius.MEDIUM}px;
                font-size: {Typography.CAPTION}pt;
                font-weight: {weight};
                padding: 2px 1px;
            }}
            QPushButton:hover {{
                background-color: {c.PRIMARY_LIGHT};
                border-color: {c.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {c.PRIMARY};
                color: white;
            }}
        """)
        if self._style_class == 'disabled':
            self.setEnabled(False)

    def update_theme(self):
        self._apply_style()


class MathKeyboard(QWidget):
    """
    Teclado virtual matemático con pestañas (123, f(x), ABC, #&¬).
    Emite key_action(action, data) al presionar cualquier tecla.
    """

    key_action = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: list[MathKeyboardButton] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, Spacing.TINY, 0, 0)
        layout.setSpacing(0)

        self._tabs = QTabWidget()
        self._tabs.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._tabs.tabBar().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._tabs.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        self._tabs.addTab(self._build_tab(TAB_123), '123')
        self._tabs.addTab(self._build_tab(TAB_FX), 'f(x)')
        self._tabs.addTab(self._build_tab(TAB_ABC), 'ABC')
        self._tabs.addTab(self._build_tab(TAB_SYM), '#&¬')

        layout.addWidget(self._tabs)

    def _build_tab(self, rows: list) -> QWidget:
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(2, 2, 2, 2)
        tab_layout.setSpacing(2)

        for row_data in rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(2)

            for item in row_data:
                if item is None:
                    sep = QFrame()
                    sep.setFixedWidth(4)
                    row_layout.addWidget(sep)
                    continue

                label, action, data, style = item
                btn = MathKeyboardButton(label, style)
                self._buttons.append(btn)

                if action:
                    btn.clicked.connect(
                        lambda checked, a=action, d=data: self.key_action.emit(a, d)
                    )

                row_layout.addWidget(btn)

            tab_layout.addLayout(row_layout)

        tab_layout.addStretch()
        return tab

    def update_theme(self):
        for btn in self._buttons:
            btn.update_theme()
