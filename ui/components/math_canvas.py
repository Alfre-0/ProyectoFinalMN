"""
math_canvas.py — Widget de renderizado interactivo de expresiones matemáticas.
Dibuja el AST usando QPainter y maneja la navegación del cursor.
Es el componente principal de edición: el usuario interactúa directamente
con la expresión renderizada, no con texto plano.
"""
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, pyqtSignal, QSize
from PyQt6.QtGui import (
    QPainter, QPen, QColor, QFont, QFontMetricsF, QPainterPath, QKeyEvent,
)
from ui.styles.tokens import Typography, Radius
from ui.styles.theme import ThemeManager
from ui.components.math_ast import (
    MathExpression, MathNode, CharNode, PowerNode, SqrtNode,
    FractionNode, FuncNode, ParenNode, Slot,
)


class MathCanvas(QWidget):
    """
    Canvas interactivo que renderiza el AST matemático con QPainter.
    Soporta renderizado visual de potencias, raíces, fracciones, funciones,
    paréntesis, cursor parpadeante, y entrada de teclado físico.
    """

    text_changed = pyqtSignal(str)
    focused = pyqtSignal(bool)

    _BASE_FONT_SIZE = 16
    _EXP_SCALE = 0.7
    _FRAC_SCALE = 0.85
    _PAD = 12

    def __init__(self, expression: MathExpression, parent=None):
        super().__init__(parent)
        self._expr = expression
        self._placeholder = ""
        self._cursor_vis = True
        self._cursor_rects: dict[tuple[int, int], tuple[float, float, float]] = {}

        self._blink = QTimer(self)
        self._blink.timeout.connect(self._toggle_cursor)
        self._blink.start(530)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumHeight(48)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def setPlaceholderText(self, text: str):
        self._placeholder = text
        self.update()

    # ── Paint ─────────────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        c = ThemeManager.colors()

        # Fondo con borde
        bg = self.rect().adjusted(0, 0, -1, -1)
        border_color = c.BORDER_FOCUS if self.hasFocus() else c.BORDER
        painter.setPen(QPen(QColor(border_color), 2 if self.hasFocus() else 1))
        painter.setBrush(QColor(c.SURFACE))
        painter.drawRoundedRect(bg, Radius.MEDIUM, Radius.MEDIUM)

        self._cursor_rects.clear()

        if self._expr.is_empty() and not self.hasFocus():
            painter.setPen(QColor(c.TEXT_MUTED))
            font = QFont(Typography.FONT_FAMILY, self._BASE_FONT_SIZE - 2)
            font.setItalic(True)
            painter.setFont(font)
            r = self.rect().adjusted(self._PAD, 0, -self._PAD, 0)
            painter.drawText(r, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                             self._placeholder)
        else:
            fs = self._BASE_FONT_SIZE
            tw, ta, td = self._m_slot(self._expr.root_slot, fs)
            x0 = self._PAD
            yb = self.height() / 2 + (ta - td) / 2

            painter.setPen(QColor(c.TEXT_PRIMARY))
            self._p_slot(painter, self._expr.root_slot, x0, yb, fs)

            # Cursor
            if self.hasFocus() and self._cursor_vis:
                cur = self._expr.cursor
                key = (id(cur.slot), cur.position)
                if key in self._cursor_rects:
                    cx, ct, cb = self._cursor_rects[key]
                    painter.setPen(QPen(QColor(c.PRIMARY), 2))
                    painter.drawLine(QPointF(cx, ct), QPointF(cx, cb))

        painter.end()

    # ── Medición ──────────────────────────────────────────────────

    def _m_slot(self, slot: Slot, fs: float) -> tuple[float, float, float]:
        """Mide slot → (width, ascent, descent)."""
        if not slot.nodes:
            return (fs * 0.6, fs * 0.65, fs * 0.2)
        w, a, d = 0.0, 0.0, 0.0
        for node in slot.nodes:
            nw, na, nd = self._m_node(node, fs)
            w += nw
            a = max(a, na)
            d = max(d, nd)
        return (w, a, d)

    def _m_node(self, node: MathNode, fs: float):
        if isinstance(node, CharNode):
            return self._m_char(node, fs)
        if isinstance(node, PowerNode):
            return self._m_power(node, fs)
        if isinstance(node, SqrtNode):
            return self._m_sqrt(node, fs)
        if isinstance(node, FractionNode):
            return self._m_frac(node, fs)
        if isinstance(node, FuncNode):
            return self._m_func(node, fs)
        if isinstance(node, ParenNode):
            return self._m_paren(node, fs)
        return (0, 0, 0)

    def _font(self, fs: float, italic: bool = False) -> QFont:
        f = QFont(Typography.FONT_FAMILY, max(8, int(fs)))
        f.setItalic(italic)
        return f

    def _m_char(self, node: CharNode, fs: float):
        is_var = node.char.isalpha() and not node.is_operator and not node.is_constant
        fm = QFontMetricsF(self._font(fs, italic=is_var))
        w = fm.horizontalAdvance(node.display_char)
        if node.is_operator:
            w += fs * 0.4
        return (w, fm.ascent(), fm.descent())

    def _m_power(self, node: PowerNode, fs: float):
        bw, ba, bd = self._m_slot(node.base_slot, fs)
        efs = fs * self._EXP_SCALE
        ew, ea, ed = self._m_slot(node.exponent_slot, efs)
        return (bw + ew + 1, max(ba, ba * 0.6 + ea + ed), bd)

    def _m_sqrt(self, node: SqrtNode, fs: float):
        rw, ra, rd = self._m_slot(node.radicand_slot, fs)
        sw = fs * 0.75
        return (sw + rw + 4, ra + fs * 0.2 + 3, rd + 2)

    def _m_frac(self, node: FractionNode, fs: float):
        ffs = fs * self._FRAC_SCALE
        nw, na, nd = self._m_slot(node.numerator_slot, ffs)
        dw, da, dd = self._m_slot(node.denominator_slot, ffs)
        gap = 3
        ma = fs * 0.3
        w = max(nw, dw) + 8
        asc = ma + gap + na + nd
        desc = max(fs * 0.2, -ma + gap + 1.5 + da + dd)
        return (w, asc, desc)

    def _m_func(self, node: FuncNode, fs: float):
        fm = QFontMetricsF(self._font(fs))
        aw, aa, ad = self._m_slot(node.argument_slot, fs)
        if node.name == 'abs':
            bw = fs * 0.15
            return (bw + aw + bw + 6, max(aa, fm.ascent()), max(ad, fm.descent()))
        nw = fm.horizontalAdvance(node.name)
        pw = fm.horizontalAdvance('(') + fm.horizontalAdvance(')')
        return (nw + pw + aw, max(aa, fm.ascent()), max(ad, fm.descent()))

    def _m_paren(self, node: ParenNode, fs: float):
        cw, ca, cd = self._m_slot(node.content_slot, fs)
        fm = QFontMetricsF(self._font(fs))
        pw = fm.horizontalAdvance('(')
        return (pw * 2 + cw, max(ca, fm.ascent()), max(cd, fm.descent()))

    # ── Pintado ───────────────────────────────────────────────────

    def _p_slot(self, p: QPainter, slot: Slot, x: float, yb: float, fs: float):
        _, sa, sd = self._m_slot(slot, fs)
        c = ThemeManager.colors()

        if not slot.nodes:
            # Placeholder vacío
            ph_w, ph_h = fs * 0.5, fs * 0.55
            rect = QRectF(x + 2, yb - ph_h * 0.7, ph_w, ph_h)
            p.setPen(QPen(QColor(c.TEXT_MUTED), 1.0, Qt.PenStyle.DashLine))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(rect, 2, 2)
            self._cursor_rects[(id(slot), 0)] = (x + 2, yb - sa, yb + sd)
            return

        cx = x
        for i, node in enumerate(slot.nodes):
            self._cursor_rects[(id(slot), i)] = (cx, yb - sa, yb + sd)
            cx += self._p_node(p, node, cx, yb, fs)
        self._cursor_rects[(id(slot), len(slot.nodes))] = (cx, yb - sa, yb + sd)

    def _p_node(self, p: QPainter, node: MathNode, x: float, yb: float, fs: float) -> float:
        if isinstance(node, CharNode):
            return self._p_char(p, node, x, yb, fs)
        if isinstance(node, PowerNode):
            return self._p_power(p, node, x, yb, fs)
        if isinstance(node, SqrtNode):
            return self._p_sqrt(p, node, x, yb, fs)
        if isinstance(node, FractionNode):
            return self._p_frac(p, node, x, yb, fs)
        if isinstance(node, FuncNode):
            return self._p_func(p, node, x, yb, fs)
        if isinstance(node, ParenNode):
            return self._p_paren(p, node, x, yb, fs)
        return 0

    def _p_char(self, p: QPainter, node: CharNode, x: float, yb: float, fs: float) -> float:
        c = ThemeManager.colors()
        is_var = node.char.isalpha() and not node.is_operator and not node.is_constant
        font = self._font(fs, italic=is_var)
        p.setFont(font)
        fm = QFontMetricsF(font)
        ch = node.display_char
        cw = fm.horizontalAdvance(ch)

        if node.is_operator:
            p.setPen(QColor(c.PRIMARY))
            pad = fs * 0.2
            p.drawText(QPointF(x + pad, yb), ch)
            return cw + fs * 0.4
        elif node.is_constant:
            p.setPen(QColor(c.ACCENT))
        else:
            p.setPen(QColor(c.TEXT_PRIMARY))

        p.drawText(QPointF(x, yb), ch)
        return cw

    def _p_power(self, p: QPainter, node: PowerNode, x: float, yb: float, fs: float) -> float:
        bw, ba, _ = self._m_slot(node.base_slot, fs)
        self._p_slot(p, node.base_slot, x, yb, fs)
        efs = fs * self._EXP_SCALE
        _, _, ed = self._m_slot(node.exponent_slot, efs)
        ey = yb - ba * 0.6 - ed
        self._p_slot(p, node.exponent_slot, x + bw + 1, ey, efs)
        ew = self._m_slot(node.exponent_slot, efs)[0]
        return bw + ew + 1

    def _p_sqrt(self, p: QPainter, node: SqrtNode, x: float, yb: float, fs: float) -> float:
        c = ThemeManager.colors()
        rw, ra, rd = self._m_slot(node.radicand_slot, fs)
        sw = fs * 0.75
        top_y = yb - ra - fs * 0.2

        path = QPainterPath()
        path.moveTo(x + 2, yb - ra * 0.3)
        path.lineTo(x + sw * 0.35, yb + rd + 1)
        path.lineTo(x + sw * 0.7, top_y)
        path.lineTo(x + sw + rw + 2, top_y)
        p.setPen(QPen(QColor(c.TEXT_PRIMARY), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(path)

        self._p_slot(p, node.radicand_slot, x + sw, yb, fs)
        return sw + rw + 4

    def _p_frac(self, p: QPainter, node: FractionNode, x: float, yb: float, fs: float) -> float:
        c = ThemeManager.colors()
        ffs = fs * self._FRAC_SCALE
        nw, na, nd = self._m_slot(node.numerator_slot, ffs)
        dw, da, _ = self._m_slot(node.denominator_slot, ffs)
        gap, bar_t, ma = 3, 1.5, fs * 0.3
        tw = max(nw, dw) + 8
        bar_y = yb - ma

        num_yb = bar_y - gap - nd
        self._p_slot(p, node.numerator_slot, x + (tw - nw) / 2, num_yb, ffs)

        p.setPen(QPen(QColor(c.TEXT_PRIMARY), bar_t))
        p.drawLine(QPointF(x + 2, bar_y), QPointF(x + tw - 2, bar_y))

        den_yb = bar_y + bar_t + gap + da
        self._p_slot(p, node.denominator_slot, x + (tw - dw) / 2, den_yb, ffs)
        return tw

    def _p_func(self, p: QPainter, node: FuncNode, x: float, yb: float, fs: float) -> float:
        c = ThemeManager.colors()
        font = self._font(fs)
        p.setFont(font)
        fm = QFontMetricsF(font)
        aw = self._m_slot(node.argument_slot, fs)[0]

        if node.name == 'abs':
            bw = fs * 0.15
            p.setPen(QPen(QColor(c.TEXT_PRIMARY), 2))
            aa, ad = self._m_slot(node.argument_slot, fs)[1:]
            p.drawLine(QPointF(x + 2, yb - aa), QPointF(x + 2, yb + ad))
            self._p_slot(p, node.argument_slot, x + bw + 3, yb, fs)
            rx = x + bw + 3 + aw + 1
            p.drawLine(QPointF(rx, yb - aa), QPointF(rx, yb + ad))
            return bw + aw + bw + 6

        p.setPen(QColor(c.TEXT_PRIMARY))
        p.drawText(QPointF(x, yb), node.name)
        nw = fm.horizontalAdvance(node.name)

        p.setPen(QColor(c.TEXT_SECONDARY))
        p.drawText(QPointF(x + nw, yb), '(')
        ow = fm.horizontalAdvance('(')
        self._p_slot(p, node.argument_slot, x + nw + ow, yb, fs)
        p.setPen(QColor(c.TEXT_SECONDARY))
        p.drawText(QPointF(x + nw + ow + aw, yb), ')')
        cw = fm.horizontalAdvance(')')
        return nw + ow + aw + cw

    def _p_paren(self, p: QPainter, node: ParenNode, x: float, yb: float, fs: float) -> float:
        c = ThemeManager.colors()
        font = self._font(fs)
        p.setFont(font)
        fm = QFontMetricsF(font)
        cw = self._m_slot(node.content_slot, fs)[0]
        pw = fm.horizontalAdvance('(')

        p.setPen(QColor(c.TEXT_SECONDARY))
        p.drawText(QPointF(x, yb), '(')
        self._p_slot(p, node.content_slot, x + pw, yb, fs)
        p.setPen(QColor(c.TEXT_SECONDARY))
        p.drawText(QPointF(x + pw + cw, yb), ')')
        return pw + cw + pw

    # ── Teclado físico ────────────────────────────────────────────

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        cur = self._expr.cursor

        if key == Qt.Key.Key_Left:
            cur.move_left()
        elif key == Qt.Key.Key_Right:
            cur.move_right()
        elif key == Qt.Key.Key_Backspace:
            cur.backspace()
        elif key == Qt.Key.Key_Delete:
            cur.move_right()
            cur.backspace()
        elif key == Qt.Key.Key_AsciiCircum:
            cur.insert_power()
        elif text == '(':
            cur.insert_open_paren()
        elif text == ')':
            cur.insert_close_paren()
        elif text and text.isprintable():
            cur.insert_char(text)
        else:
            super().keyPressEvent(event)
            return

        self._cursor_vis = True
        self._blink.start(530)
        self.update()
        self.text_changed.emit(self._expr.to_evaluable())

    # ── Focus ─────────────────────────────────────────────────────

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._cursor_vis = True
        self._blink.start(530)
        self.focused.emit(True)
        self.update()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._cursor_vis = False
        self._blink.stop()
        self.focused.emit(False)
        self.update()

    def _toggle_cursor(self):
        self._cursor_vis = not self._cursor_vis
        self.update()

    # ── Click para posicionar cursor ──────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setFocus(Qt.FocusReason.MouseFocusReason)
            click_x = event.position().x()
            best_key, best_dist = None, float('inf')
            for key, (cx, _, _) in self._cursor_rects.items():
                d = abs(cx - click_x)
                if d < best_dist:
                    best_dist = d
                    best_key = key
            if best_key is not None:
                slot_id, pos = best_key
                target = self._find_slot(self._expr.root_slot, slot_id)
                if target:
                    self._expr.cursor.slot = target
                    self._expr.cursor.position = pos
                    self._cursor_vis = True
                    self._blink.start(530)
                    self.update()
        super().mousePressEvent(event)

    def _find_slot(self, slot: Slot, target_id: int):
        if id(slot) == target_id:
            return slot
        for node in slot.nodes:
            for cs in node.get_child_slots():
                found = self._find_slot(cs, target_id)
                if found:
                    return found
        return None

    def sizeHint(self) -> QSize:
        return QSize(200, 48)

    # ── API para teclado virtual ──────────────────────────────────

    def handle_action(self, action: str, data: str = ''):
        cur = self._expr.cursor
        actions = {
            'char': lambda: cur.insert_char(data),
            'constant': lambda: cur.insert_char(data, is_constant=True),
            'power': cur.insert_power,
            'power_squared': cur.insert_power_squared,
            'sqrt': cur.insert_sqrt,
            'fraction': cur.insert_fraction,
            'function': lambda: cur.insert_function(data),
            'left': cur.move_left,
            'right': cur.move_right,
            'backspace': cur.backspace,
            'open_paren': cur.insert_open_paren,
            'close_paren': cur.insert_close_paren,
        }
        fn = actions.get(action)
        if fn:
            fn()
        self._cursor_vis = True
        self._blink.start(530)
        self.setFocus()
        self.update()
        self.text_changed.emit(self._expr.to_evaluable())
