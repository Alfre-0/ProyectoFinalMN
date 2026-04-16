"""
math_ast.py — Modelo de expresiones matemáticas como árbol de bloques (AST visual).
Responsabilidad: representar la estructura de una expresión matemática,
proveer navegación con cursor, y exportar a LaTeX y string evaluable.
NO contiene ninguna referencia a PyQt6 ni UI.
"""
from __future__ import annotations
from typing import Optional


# ── Slot (área editable) ──────────────────────────────────────────

class Slot:
    """
    Área editable: lista ordenada de MathNodes donde el cursor puede
    posicionarse. Ejemplos: raíz de la expresión, exponente de un
    PowerNode, radicando de un SqrtNode.
    """

    def __init__(self, parent_node: Optional[MathNode] = None):
        self.nodes: list[MathNode] = []
        self.parent_node = parent_node

    def insert(self, index: int, node: MathNode):
        node.parent_slot = self
        self.nodes.insert(index, node)

    def remove(self, index: int) -> MathNode:
        node = self.nodes.pop(index)
        node.parent_slot = None
        return node

    def __len__(self):
        return len(self.nodes)

    def __bool__(self):
        return True  # Slot siempre truthy; usar len() para vacío


# ── Nodos ─────────────────────────────────────────────────────────

class MathNode:
    """Clase base abstracta para todos los nodos del AST matemático."""

    def __init__(self):
        self.parent_slot: Optional[Slot] = None

    def get_child_slots(self) -> list[Slot]:
        return []

    def to_latex(self) -> str:
        raise NotImplementedError

    def to_evaluable(self) -> str:
        raise NotImplementedError


class CharNode(MathNode):
    """Nodo hoja: un solo carácter (dígito, variable, operador, constante)."""

    _LATEX_MAP = {
        'π': '\\pi', '×': '\\times', '÷': '\\div',
        '·': '\\cdot', '≤': '\\leq', '≥': '\\geq',
        '≠': '\\neq', '∞': '\\infty',
    }
    _EVAL_MAP = {
        'π': 'pi', '×': '*', '÷': '/', '·': '*', '−': '-',
    }
    _DISPLAY_MAP = {
        '*': '×', '/': '÷', '-': '−',
    }

    def __init__(self, char: str, is_constant: bool = False):
        super().__init__()
        self.char = char
        self.is_constant = is_constant

    @property
    def display_char(self) -> str:
        return self._DISPLAY_MAP.get(self.char, self.char)

    @property
    def is_operator(self) -> bool:
        return self.char in '+-×÷·=<>*/≤≥≠−'

    def to_latex(self) -> str:
        return self._LATEX_MAP.get(self.char, self.char)

    def to_evaluable(self) -> str:
        if self.is_constant and self.char == 'e':
            return 'E'
        return self._EVAL_MAP.get(self.char, self.char)


class PowerNode(MathNode):
    """Potencia: base^{exponente}."""

    def __init__(self):
        super().__init__()
        self.base_slot = Slot(parent_node=self)
        self.exponent_slot = Slot(parent_node=self)

    def get_child_slots(self) -> list[Slot]:
        return [self.base_slot, self.exponent_slot]

    def to_latex(self) -> str:
        base = _slot_to_latex(self.base_slot)
        exp = _slot_to_latex(self.exponent_slot)
        if len(self.base_slot.nodes) > 1:
            base = '{' + base + '}'
        return f'{{{base}}}^{{{exp}}}'

    def to_evaluable(self) -> str:
        base = _slot_to_evaluable(self.base_slot)
        exp = _slot_to_evaluable(self.exponent_slot)
        return f'({base})**({exp})'


class SqrtNode(MathNode):
    """Raíz cuadrada: √{radicando}."""

    def __init__(self):
        super().__init__()
        self.radicand_slot = Slot(parent_node=self)

    def get_child_slots(self) -> list[Slot]:
        return [self.radicand_slot]

    def to_latex(self) -> str:
        return f'\\sqrt{{{_slot_to_latex(self.radicand_slot)}}}'

    def to_evaluable(self) -> str:
        return f'sqrt({_slot_to_evaluable(self.radicand_slot)})'


class FractionNode(MathNode):
    """Fracción: numerador / denominador."""

    def __init__(self):
        super().__init__()
        self.numerator_slot = Slot(parent_node=self)
        self.denominator_slot = Slot(parent_node=self)

    def get_child_slots(self) -> list[Slot]:
        return [self.numerator_slot, self.denominator_slot]

    def to_latex(self) -> str:
        n = _slot_to_latex(self.numerator_slot)
        d = _slot_to_latex(self.denominator_slot)
        return f'\\frac{{{n}}}{{{d}}}'

    def to_evaluable(self) -> str:
        n = _slot_to_evaluable(self.numerator_slot)
        d = _slot_to_evaluable(self.denominator_slot)
        return f'({n})/({d})'


class FuncNode(MathNode):
    """Función matemática: sin, cos, ln, etc."""

    _LATEX_NAMES = {
        'sin': '\\sin', 'cos': '\\cos', 'tan': '\\tan',
        'asin': '\\arcsin', 'acos': '\\arccos', 'atan': '\\arctan',
        'ln': '\\ln', 'log': '\\log', 'exp': '\\exp',
    }
    _EVAL_NAMES = {
        'ln': 'log',   # SymPy: log() = logaritmo natural
        'sen': 'sin',  # Alias español
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.argument_slot = Slot(parent_node=self)

    def get_child_slots(self) -> list[Slot]:
        return [self.argument_slot]

    def to_latex(self) -> str:
        latex_name = self._LATEX_NAMES.get(self.name, self.name)
        arg = _slot_to_latex(self.argument_slot)
        if self.name == 'abs':
            return f'\\left|{arg}\\right|'
        return f'{latex_name}\\left({arg}\\right)'

    def to_evaluable(self) -> str:
        eval_name = self._EVAL_NAMES.get(self.name, self.name)
        arg = _slot_to_evaluable(self.argument_slot)
        if self.name == 'abs':
            return f'Abs({arg})'
        return f'{eval_name}({arg})'


class ParenNode(MathNode):
    """Paréntesis estructural: (contenido)."""

    def __init__(self):
        super().__init__()
        self.content_slot = Slot(parent_node=self)

    def get_child_slots(self) -> list[Slot]:
        return [self.content_slot]

    def to_latex(self) -> str:
        return f'\\left({_slot_to_latex(self.content_slot)}\\right)'

    def to_evaluable(self) -> str:
        return f'({_slot_to_evaluable(self.content_slot)})'


# ── Funciones de exportación ──────────────────────────────────────

def _slot_to_latex(slot: Slot) -> str:
    if not slot.nodes:
        return '\\square'
    return ''.join(n.to_latex() for n in slot.nodes)


def _slot_to_evaluable(slot: Slot) -> str:
    return ''.join(n.to_evaluable() for n in slot.nodes)


# ── Cursor ────────────────────────────────────────────────────────

class MathCursor:
    """
    Cursor que navega dentro de la estructura del AST.
    Posición 0 = antes del primer nodo, len(slot) = después del último.
    """

    def __init__(self, root_slot: Slot):
        self.slot = root_slot
        self.position = 0

    # ── Navegación ──

    def move_right(self):
        if self.position < len(self.slot):
            next_node = self.slot.nodes[self.position]
            children = next_node.get_child_slots()
            if children:
                self.slot = children[0]
                self.position = 0
                return
            self.position += 1
            return
        self._exit_slot_right()

    def move_left(self):
        if self.position > 0:
            prev_node = self.slot.nodes[self.position - 1]
            children = prev_node.get_child_slots()
            if children:
                self.slot = children[-1]
                self.position = len(self.slot)
                return
            self.position -= 1
            return
        self._exit_slot_left()

    def _exit_slot_right(self):
        parent = self.slot.parent_node
        if parent is None:
            return
        siblings = parent.get_child_slots()
        idx = next((i for i, s in enumerate(siblings) if s is self.slot), -1)
        if idx >= 0 and idx + 1 < len(siblings):
            self.slot = siblings[idx + 1]
            self.position = 0
            return
        parent_slot = parent.parent_slot
        if parent_slot is None:
            return
        parent_pos = next((i for i, n in enumerate(parent_slot.nodes) if n is parent), 0)
        self.slot = parent_slot
        self.position = parent_pos + 1

    def _exit_slot_left(self):
        parent = self.slot.parent_node
        if parent is None:
            return
        siblings = parent.get_child_slots()
        idx = next((i for i, s in enumerate(siblings) if s is self.slot), -1)
        if idx > 0:
            self.slot = siblings[idx - 1]
            self.position = len(self.slot)
            return
        parent_slot = parent.parent_slot
        if parent_slot is None:
            return
        parent_pos = next((i for i, n in enumerate(parent_slot.nodes) if n is parent), 0)
        self.slot = parent_slot
        self.position = parent_pos

    def force_exit_to_root(self, root_slot: Slot):
        while self.slot is not root_slot and self.slot.parent_node is not None:
            self._exit_slot_right()

    # ── Inserción ──

    def insert_char(self, char: str, is_constant: bool = False):
        node = CharNode(char, is_constant=is_constant)
        self.slot.insert(self.position, node)
        self.position += 1

    def insert_power(self):
        """xⁿ — consume anterior como base, cursor en exponente."""
        power = PowerNode()
        if self.position > 0:
            prev = self.slot.remove(self.position - 1)
            self.position -= 1
            power.base_slot.insert(0, prev)
        self.slot.insert(self.position, power)
        self.slot = power.exponent_slot
        self.position = 0

    def insert_power_squared(self):
        """x² — consume anterior como base, exponente = 2."""
        power = PowerNode()
        if self.position > 0:
            prev = self.slot.remove(self.position - 1)
            self.position -= 1
            power.base_slot.insert(0, prev)
        power.exponent_slot.insert(0, CharNode('2'))
        self.slot.insert(self.position, power)
        self.position += 1

    def insert_sqrt(self):
        sqrt_node = SqrtNode()
        self.slot.insert(self.position, sqrt_node)
        self.slot = sqrt_node.radicand_slot
        self.position = 0

    def insert_fraction(self):
        frac = FractionNode()
        if self.position > 0:
            prev = self.slot.remove(self.position - 1)
            self.position -= 1
            frac.numerator_slot.insert(0, prev)
        self.slot.insert(self.position, frac)
        if frac.numerator_slot.nodes:
            self.slot = frac.denominator_slot
        else:
            self.slot = frac.numerator_slot
        self.position = 0

    def insert_function(self, name: str):
        func = FuncNode(name)
        self.slot.insert(self.position, func)
        self.slot = func.argument_slot
        self.position = 0

    def insert_open_paren(self):
        paren = ParenNode()
        self.slot.insert(self.position, paren)
        self.slot = paren.content_slot
        self.position = 0

    def insert_close_paren(self):
        """Sale del ParenNode actual si existe; si no, inserta ')' literal."""
        current = self.slot
        while current.parent_node is not None:
            if isinstance(current.parent_node, ParenNode):
                paren = current.parent_node
                pslot = paren.parent_slot
                if pslot:
                    idx = next((i for i, n in enumerate(pslot.nodes) if n is paren), 0)
                    self.slot = pslot
                    self.position = idx + 1
                    return
            parent = current.parent_node
            current = parent.parent_slot if parent.parent_slot else current
            if current is self.slot:
                break
        self.insert_char(')')

    def backspace(self):
        if self.position > 0:
            node = self.slot.nodes[self.position - 1]
            self.slot.remove(self.position - 1)
            self.position -= 1
            # Si era compuesto, reinsertar contenido aplanado
            children = node.get_child_slots()
            if children:
                offset = 0
                for child_slot in children:
                    for child_node in child_slot.nodes:
                        self.slot.insert(self.position + offset, child_node)
                        offset += 1
                self.position += offset
        elif self.slot.parent_node is not None:
            parent = self.slot.parent_node
            all_empty = all(len(s) == 0 for s in parent.get_child_slots())
            if all_empty and parent.parent_slot:
                idx = next((i for i, n in enumerate(parent.parent_slot.nodes)
                            if n is parent), 0)
                target_slot = parent.parent_slot
                target_slot.remove(idx)
                self.slot = target_slot
                self.position = idx
                return
            self._exit_slot_left()


# ── Expresión raíz ────────────────────────────────────────────────

class MathExpression:
    """Contenedor principal: slot raíz + cursor."""

    def __init__(self):
        self.root_slot = Slot()
        self.cursor = MathCursor(self.root_slot)

    def to_latex(self) -> str:
        return _slot_to_latex(self.root_slot)

    def to_evaluable(self) -> str:
        return _slot_to_evaluable(self.root_slot)

    def clear(self):
        self.root_slot.nodes.clear()
        self.cursor.slot = self.root_slot
        self.cursor.position = 0

    def is_empty(self) -> bool:
        return len(self.root_slot.nodes) == 0


# ── Parser texto → AST ───────────────────────────────────────────

_FUNC_NAMES = ['sqrt', 'asin', 'acos', 'atan', 'sin', 'cos', 'tan',
               'sen', 'ln', 'log', 'exp', 'abs']


def _match_func(text: str, pos: int):
    for name in _FUNC_NAMES:
        if text[pos:].startswith(name):
            end = pos + len(name)
            if end >= len(text) or not text[end].isalpha():
                return name, end
    return None


def _extract_balanced(text: str, pos: int, open_c: str, close_c: str):
    if pos >= len(text) or text[pos] != open_c:
        return '', 0
    depth, j = 1, pos + 1
    while j < len(text) and depth > 0:
        if text[j] == open_c:
            depth += 1
        elif text[j] == close_c:
            depth -= 1
        j += 1
    return text[pos + 1:j - 1], j - pos


def build_ast_from_text(text: str) -> list[MathNode]:
    """Construye lista de MathNodes desde texto plano. Para setText()."""
    text = text.strip().replace('**', '^')
    nodes: list[MathNode] = []
    i = 0

    while i < len(text):
        if text[i] == ' ':
            i += 1
            continue

        # Funciones (sin, cos, sqrt, etc.)
        func_match = _match_func(text, i)
        if func_match:
            fname, new_i = func_match
            i = new_i
            if fname == 'sqrt':
                node = SqrtNode()
                target = node.radicand_slot
            else:
                real_name = 'sin' if fname == 'sen' else fname
                node = FuncNode(real_name)
                target = node.argument_slot
            if i < len(text) and text[i] == '(':
                inner, consumed = _extract_balanced(text, i, '(', ')')
                i += consumed
                for n in build_ast_from_text(inner):
                    target.insert(len(target), n)
            nodes.append(node)
            continue

        # Paréntesis
        if text[i] == '(':
            inner, consumed = _extract_balanced(text, i, '(', ')')
            i += consumed
            paren = ParenNode()
            for n in build_ast_from_text(inner):
                paren.content_slot.insert(len(paren.content_slot), n)
            nodes.append(paren)
            continue

        # Potencia
        if text[i] == '^':
            i += 1
            power = PowerNode()
            if nodes:
                power.base_slot.insert(0, nodes.pop())
            if i < len(text):
                if text[i] == '{':
                    inner, consumed = _extract_balanced(text, i, '{', '}')
                    i += consumed
                    for n in build_ast_from_text(inner):
                        power.exponent_slot.insert(len(power.exponent_slot), n)
                else:
                    j = i
                    if j < len(text) and text[j] == '-':
                        j += 1
                    while j < len(text) and (text[j].isalnum() or text[j] == '.'):
                        j += 1
                    for c in text[i:j]:
                        power.exponent_slot.insert(len(power.exponent_slot), CharNode(c))
                    i = j
            nodes.append(power)
            continue

        # Carácter normal
        nodes.append(CharNode(text[i]))
        i += 1

    return nodes
