"""
math_input.py — Componente compuesto de entrada matemática.
Ensambla MathCanvas + MathKeyboard en un widget cohesivo.
API compatible con QLineEdit para integración transparente con las vistas.

El usuario interactúa con la expresión renderizada (canvas), NO con texto plano.
El teclado virtual es colapsable con toggle y se auto-expande al recibir foco.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QCursor
from ui.components.math_ast import MathExpression, build_ast_from_text
from ui.components.math_canvas import MathCanvas
from ui.components.math_keyboard import MathKeyboard
from ui.styles.tokens import Spacing, Radius, Typography
from ui.styles.theme import ThemeManager


class MathInput(QWidget):
    """
    Widget de entrada matemática con edición estructurada por bloques.
    Reemplaza QLineEdit para campos de funciones f(x).

    API pública compatible:
        text()              → str evaluable (SymPy-compatible)
        setText(str)        → poblar desde texto plano
        clear()             → limpiar expresión
        setPlaceholderText  → texto placeholder
        setToolTip          → tooltip (heredado de QWidget)
    """

    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expression = MathExpression()
        self._keyboard_visible = False
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # ── Canvas + toggle ──
        canvas_row = QHBoxLayout()
        canvas_row.setSpacing(4)

        self._canvas = MathCanvas(self._expression)
        self._canvas.setFixedHeight(48)
        canvas_row.addWidget(self._canvas, 1)

        self._toggle_btn = QPushButton('fₓ')
        self._toggle_btn.setFixedSize(40, 48)
        self._toggle_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setToolTip('Mostrar/ocultar teclado matemático')
        self._update_toggle_style()
        canvas_row.addWidget(self._toggle_btn, 0, Qt.AlignmentFlag.AlignTop)

        layout.addLayout(canvas_row)

        # ── Teclado virtual (colapsable) ──
        self._keyboard = MathKeyboard()
        self._keyboard.setVisible(False)
        layout.addWidget(self._keyboard)

    def _connect_signals(self):
        self._toggle_btn.clicked.connect(self._toggle_keyboard)
        self._keyboard.key_action.connect(self._on_keyboard_action)
        self._canvas.text_changed.connect(self.textChanged)
        self._canvas.focused.connect(self._on_canvas_focus)

    # ── Estado del teclado ──

    def _toggle_keyboard(self):
        self._keyboard_visible = not self._keyboard_visible
        self._keyboard.setVisible(self._keyboard_visible)
        self._update_toggle_style()

    def _on_canvas_focus(self, focused: bool):
        """Auto-expandir teclado cuando el canvas recibe foco, y colapsar al perderlo asegurando que no clickeó el propio teclado."""
        if focused and not self._keyboard_visible:
            self._keyboard_visible = True
            self._keyboard.setVisible(True)
            self._update_toggle_style()
        elif not focused and self._keyboard_visible:
            # Retrasamos la comprobación milisegundos para que Qt asigne el nuevo foco
            QTimer.singleShot(10, self._check_focus_loss)

    def _check_focus_loss(self):
        fw = QApplication.focusWidget()
        # Si el nuevo foco se quedó dentro de nuestro input/teclado explícitamente
        if fw and self.isAncestorOf(fw):
            return
            
        # Validar la geometría: si el cursor del mouse está dentro de nuestros límites
        # significa que el clic fue en un área muerta (fondos, pestañas) de nuestro teclado.
        # En este caso, NO encerramos, interceptamos y restauramos el foco al canvas fuertemente.
        global_pos = QCursor.pos()
        if self.rect().contains(self.mapFromGlobal(global_pos)):
            self._canvas.setFocus()
            return
            
        if self._keyboard_visible:
            self._keyboard_visible = False
            self._keyboard.setVisible(False)
            self._update_toggle_style()

    def _on_keyboard_action(self, action: str, data: str):
        self._canvas.handle_action(action, data)

    def _update_toggle_style(self):
        c = ThemeManager.colors()
        bg = c.PRIMARY if self._keyboard_visible else c.SURFACE_ALT
        fg = '#FFFFFF' if self._keyboard_visible else c.TEXT_PRIMARY
        self._toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {c.BORDER};
                border-radius: {Radius.MEDIUM}px;
                font-size: {Typography.SUBTITLE}pt;
                font-weight: 700;
                font-family: '{Typography.FONT_FAMILY}';
                padding: 0px;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c.PRIMARY_HOVER};
                color: white;
            }}
        """)

    # ── API compatible con QLineEdit ──

    def text(self) -> str:
        """Retorna el string evaluable (Python/SymPy compatible)."""
        return self._expression.to_evaluable()

    def setText(self, text: str):
        """Establece la expresión desde texto plano (para _load_example)."""
        self._expression.clear()
        nodes = build_ast_from_text(text)
        for node in nodes:
            self._expression.root_slot.insert(
                len(self._expression.root_slot), node
            )
        self._expression.cursor.slot = self._expression.root_slot
        self._expression.cursor.position = len(self._expression.root_slot)
        self._canvas.update()

    def clear(self):
        """Limpia toda la expresión."""
        self._expression.clear()
        self._keyboard_visible = False
        self._keyboard.setVisible(False)
        self._update_toggle_style()
        self._canvas.update()

    def setPlaceholderText(self, text: str):
        self._canvas.setPlaceholderText(text)

    # ── Tema ──

    def update_theme(self):
        self._update_toggle_style()
        self._keyboard.update_theme()
        self._canvas.update()
