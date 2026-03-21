"""
history_repo.py — Repositorio de historial de cálculos.
Persiste los registros en un archivo JSON local.
"""
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Any


HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "historial.json",
)


@dataclass
class HistoryRecord:
    """Registro inmutable de un cálculo realizado."""
    timestamp: str
    module: str
    method: str
    parameters: dict
    result_summary: str
    full_data: dict = field(default_factory=dict)

    @staticmethod
    def create_now(module: str, method: str, parameters: dict,
                   result_summary: str, full_data: dict | None = None) -> "HistoryRecord":
        return HistoryRecord(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            module=module,
            method=method,
            parameters=parameters,
            result_summary=result_summary,
            full_data=full_data or {},
        )


class HistoryRepository:
    """Capa de persistencia para el historial (wrapper sobre JSON)."""

    def __init__(self, filepath: str = HISTORY_FILE):
        self._filepath = filepath
        self._ensure_directory()

    def _ensure_directory(self):
        directory = os.path.dirname(self._filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def load_all(self) -> list[HistoryRecord]:
        """Carga todos los registros almacenados."""
        if not os.path.exists(self._filepath):
            return []
        try:
            with open(self._filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [HistoryRecord(**record) for record in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def save(self, record: HistoryRecord):
        """Agrega un registro al historial."""
        records = self.load_all()
        records.insert(0, record)
        self._write(records)

    def delete(self, index: int):
        """Elimina un registro por índice."""
        records = self.load_all()
        if 0 <= index < len(records):
            records.pop(index)
            self._write(records)

    def clear_all(self):
        """Elimina todo el historial."""
        self._write([])

    def _write(self, records: list[HistoryRecord]):
        with open(self._filepath, "w", encoding="utf-8") as file:
            json.dump([asdict(r) for r in records], file, ensure_ascii=False, indent=2)
