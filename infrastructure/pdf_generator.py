"""
pdf_generator.py — Wrapper para generación de reportes PDF.
Usa fpdf2 internamente. Si se cambia la librería, solo se modifica este archivo.
"""
import os
import tempfile
from fpdf import FPDF
from datetime import datetime


class PdfGenerator:
    """Genera un reporte PDF con los datos de un cálculo numérico."""

    def __init__(self):
        self._pdf = FPDF()
        self._pdf.set_auto_page_break(auto=True, margin=20)

    def _sanitize(self, text: str) -> str:
        """Reemplaza caracteres no soportados por la fuente estándar."""
        if not isinstance(text, str):
            text = str(text)
        replacements = {
            '≈': '~',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '±': '+/-',
            'π': 'pi',
            '∫': 'Integral',
            'Δ': 'Delta',
            '∑': 'Suma',
            '√': 'raiz',
            '²': '^2',
            '³': '^3',
            '∞': 'infinito',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def generate_report(
        self,
        method_name: str,
        parameters: dict,
        procedure_text: str,
        table_headers: list[str],
        table_rows: list[list[str]],
        result_summary: str,
        observations: str = "",
        chart_image_path: str | None = None,
        output_path: str | None = None,
    ) -> str:
        """
        Genera un PDF completo con los datos del cálculo.
        Retorna la ruta del archivo generado.
        """
        # Sanitizar entradas
        method_name = self._sanitize(method_name)
        procedure_text = self._sanitize(procedure_text) if procedure_text else procedure_text
        result_summary = self._sanitize(result_summary)
        observations = self._sanitize(observations) if observations else observations
        parameters = {self._sanitize(k): self._sanitize(v) for k, v in parameters.items()}
        table_headers = [self._sanitize(h) for h in (table_headers or [])]
        table_rows = [[self._sanitize(c) for c in (r or [])] for r in (table_rows or [])]

        self._pdf.add_page()
        self._pdf.set_font("Helvetica", "B", 18)
        self._pdf.cell(0, 12, "Reporte de Cálculo Numérico", new_x="LMARGIN", new_y="NEXT", align="C")
        self._pdf.ln(4)

        self._pdf.set_font("Helvetica", "", 10)
        self._pdf.cell(
            0, 8,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            new_x="LMARGIN", new_y="NEXT",
        )
        self._pdf.cell(0, 8, f"Método: {method_name}", new_x="LMARGIN", new_y="NEXT")
        self._pdf.ln(4)

        # ── Parámetros ──
        self._add_section("Datos de Entrada")
        for key, value in parameters.items():
            self._pdf.set_font("Helvetica", "B", 10)
            self._pdf.cell(50, 7, f"{key}:", new_x="RIGHT")
            self._pdf.set_font("Helvetica", "", 10)
            self._pdf.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")

        # ── Procedimiento ──
        if procedure_text:
            self._add_section("Procedimiento")
            self._pdf.set_font("Helvetica", "", 9)
            self._pdf.multi_cell(0, 5, procedure_text)

        # ── Tabla de iteraciones ──
        if table_headers and table_rows:
            self._add_section("Tabla de Iteraciones")
            self._add_table(table_headers, table_rows)

        # ── Resultado ──
        self._add_section("Resultado")
        self._pdf.set_font("Helvetica", "B", 11)
        self._pdf.multi_cell(0, 7, result_summary)

        # ── Observaciones ──
        if observations:
            self._add_section("Observaciones")
            self._pdf.set_font("Helvetica", "", 10)
            self._pdf.multi_cell(0, 6, observations)

        # ── Gráfica ──
        if chart_image_path and os.path.exists(chart_image_path):
            self._add_section("Gráfica")
            available_width = self._pdf.w - self._pdf.l_margin - self._pdf.r_margin
            self._pdf.image(chart_image_path, w=min(available_width, 170))

        # ── Guardar ──
        if output_path is None:
            output_path = os.path.join(
                tempfile.gettempdir(),
                f"reporte_{method_name.replace(' ', '_')}_{datetime.now():%Y%m%d_%H%M%S}.pdf"
            )

        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        self._pdf.output(output_path)
        return output_path

    def _add_section(self, title: str):
        self._pdf.ln(6)
        self._pdf.set_font("Helvetica", "B", 12)
        self._pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self._pdf.set_draw_color(79, 107, 237)
        self._pdf.line(
            self._pdf.l_margin,
            self._pdf.get_y(),
            self._pdf.w - self._pdf.r_margin,
            self._pdf.get_y(),
        )
        self._pdf.ln(3)

    def _add_table(self, headers: list[str], rows: list[list[str]]):
        available_width = self._pdf.w - self._pdf.l_margin - self._pdf.r_margin
        col_width = available_width / max(len(headers), 1)

        self._pdf.set_font("Helvetica", "B", 8)
        self._pdf.set_fill_color(232, 236, 253)
        for header in headers:
            self._pdf.cell(col_width, 7, header, border=1, fill=True, align="C")
        self._pdf.ln()

        self._pdf.set_font("Helvetica", "", 7)
        for row in rows:
            for cell_value in row:
                self._pdf.cell(col_width, 6, str(cell_value)[:15], border=1, align="C")
            self._pdf.ln()
