"""Проверки хранилища: сохранение, повторная загрузка, ошибки чтения."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from storage import load_records, save_records

SAMPLE = [
    {"id": 1, "title": "Визитки для салона", "category": "визитки", "amount": 200, "completed": True},
    {"id": 2, "title": "Буклет выставки", "category": "буклеты", "amount": 24, "completed": False},
]


def test_save_then_load_roundtrip():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        assert load_records(path) == SAMPLE


def test_save_keeps_cyrillic_readable():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        text = path.read_text(encoding="utf-8")
        assert "визитки" in text
        assert "\\u" not in text


def test_save_replaces_previous_content():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        save_records(path, SAMPLE[:1])
        assert load_records(path) == SAMPLE[:1]


def test_save_leaves_no_temporary_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        leftovers = [item.name for item in Path(directory).iterdir() if item.name.endswith(".tmp")]
        assert leftovers == []


def test_load_missing_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "missing.json"
        try:
            load_records(path)
        except FileNotFoundError:
            pass
        else:
            assert False, "Ошибка не обнаружена"


def test_load_broken_json():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        path.write_text("[{", encoding="utf-8")
        try:
            load_records(path)
        except json.JSONDecodeError:
            pass
        else:
            assert False, "Ошибка не обнаружена"


def test_load_wrong_encoding():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        path.write_bytes(b'[{"id": 1, "title": "\xe2\xe8\xe7\xe8\xf2\xea\xe8"}]')
        try:
            load_records(path)
        except UnicodeDecodeError:
            pass
        else:
            assert False, "Ошибка не обнаружена"


def test_save_error_keeps_old_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "data.json"
        save_records(path, SAMPLE)
        blocker = Path(directory) / "data.json.tmp"
        blocker.mkdir()
        try:
            save_records(path, SAMPLE[:1])
        except OSError:
            pass
        else:
            assert False, "Ошибка не обнаружена"
        assert load_records(path) == SAMPLE


def main():
    checks = [
        (name, value)
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for name, check in checks:
        check()
        print(f"OK  {name}")
    print(f"\nВсе проверки пройдены: {len(checks)}")


if __name__ == "__main__":
    main()
