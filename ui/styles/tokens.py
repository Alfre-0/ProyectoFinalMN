"""
tokens.py — Sistema de Diseño Atómico.
Todas las variables semánticas de color, espaciado y tipografía viven aquí.
Ningún archivo de UI debería usar valores mágicos (ej: '#3A7CFF' o '16px').
"""


class Colors:
    """Paleta de colores semánticos para tema claro."""

    # ── Marca ──────────────────────────────────────
    PRIMARY = "#4F6BED"
    PRIMARY_HOVER = "#3A55D4"
    PRIMARY_PRESSED = "#2E45B8"
    PRIMARY_LIGHT = "#E8ECFD"

    # ── Acentos ────────────────────────────────────
    ACCENT = "#00B894"
    ACCENT_HOVER = "#009B7D"

    # ── Superficies ────────────────────────────────
    BACKGROUND = "#F5F7FB"
    SURFACE = "#FFFFFF"
    SURFACE_ALT = "#EEF1F8"
    SIDEBAR_BG = "#1E2A3A"
    SIDEBAR_ITEM_HOVER = "#2A3B50"
    SIDEBAR_ITEM_ACTIVE = "#4F6BED"

    # ── Texto ──────────────────────────────────────
    TEXT_PRIMARY = "#1A1D26"
    TEXT_SECONDARY = "#5A6275"
    TEXT_MUTED = "#9AA0B0"
    TEXT_ON_PRIMARY = "#FFFFFF"
    TEXT_SIDEBAR = "#C0C8D8"
    TEXT_SIDEBAR_ACTIVE = "#FFFFFF"

    # ── Bordes ─────────────────────────────────────
    BORDER = "#D8DCE6"
    BORDER_FOCUS = "#4F6BED"
    BORDER_ERROR = "#E74C3C"

    # ── Estados ────────────────────────────────────
    SUCCESS = "#27AE60"
    WARNING = "#F39C12"
    DANGER = "#E74C3C"
    INFO = "#3498DB"

    # ── Gráficas ───────────────────────────────────
    PLOT_BG = "#FFFFFF"
    PLOT_GRID = "#E0E0E0"
    PLOT_LINE_COLORS = ["#4F6BED", "#E74C3C", "#27AE60", "#F39C12", "#9B59B6"]


class ColorsDark:
    """Paleta de colores semánticos para tema oscuro."""

    PRIMARY = "#6C8AFF"
    PRIMARY_HOVER = "#5A75E6"
    PRIMARY_PRESSED = "#4A63CC"
    PRIMARY_LIGHT = "#1E2640"

    ACCENT = "#00D9A5"
    ACCENT_HOVER = "#00B894"

    BACKGROUND = "#0F1219"
    SURFACE = "#1A1F2E"
    SURFACE_ALT = "#232838"
    SIDEBAR_BG = "#0D1017"
    SIDEBAR_ITEM_HOVER = "#1A2030"
    SIDEBAR_ITEM_ACTIVE = "#6C8AFF"

    TEXT_PRIMARY = "#E8ECF4"
    TEXT_SECONDARY = "#A0AAC0"
    TEXT_MUTED = "#5E6880"
    TEXT_ON_PRIMARY = "#FFFFFF"
    TEXT_SIDEBAR = "#8090A8"
    TEXT_SIDEBAR_ACTIVE = "#FFFFFF"

    BORDER = "#2A3040"
    BORDER_FOCUS = "#6C8AFF"
    BORDER_ERROR = "#E74C3C"

    SUCCESS = "#2ECC71"
    WARNING = "#F1C40F"
    DANGER = "#E74C3C"
    INFO = "#5DADE2"

    PLOT_BG = "#1A1F2E"
    PLOT_GRID = "#2A3040"
    PLOT_LINE_COLORS = ["#6C8AFF", "#E74C3C", "#2ECC71", "#F1C40F", "#BB86FC"]


class Spacing:
    """Escala de espaciado consistente (px)."""
    TINY = 4
    SMALL = 8
    MEDIUM = 12
    LARGE = 16
    XL = 24
    XXL = 32
    SECTION = 48


class Radius:
    """Radios de borde semánticos."""
    SMALL = 4
    MEDIUM = 8
    LARGE = 12
    PILL = 20
    CIRCLE = 9999


class Typography:
    """Tamaños de tipografía en pt."""
    CAPTION = 9
    BODY = 10
    SUBTITLE = 12
    TITLE = 16
    HEADING = 20
    DISPLAY = 28
    FONT_FAMILY = "Segoe UI"
