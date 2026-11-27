"""Чтение и запись JSON-файла записей. Без консольного ввода-вывода."""

import json
from pathlib import Path


def load_records(path):
    """Прочитать список записей из JSON UTF-8.

    Ошибки не скрываются: FileNotFoundError, UnicodeDecodeError,
    json.JSONDecodeError и OSError обрабатывает интерфейс.
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_records(path, records):
    """Записать записи в JSON UTF-8 целиком.

    Сначала пишется временный файл, затем он заменяет основной,
    поэтому при ошибке записи прежний файл остаётся нетронутым.
    """
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)
