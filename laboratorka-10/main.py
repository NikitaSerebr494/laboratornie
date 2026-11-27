"""Основная программа: чтение matrix.txt и запись report.txt."""

import os
import sys
from pathlib import Path

from files_lab import read_matrix, selected_sum
from table import column_sums, row_sums


def read_positive_integer(prompt="Введите целое число больше нуля: "):
    """Повторять ввод, пока не получено целое число больше нуля."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Это не целое число, попробуйте снова.")
            continue
        if value <= 0:
            print("Число должно быть больше нуля.")
            continue
        return value


def build_report(matrix):
    """Текст отчёта: суммы строк, суммы столбцов и результат варианта."""
    rows = row_sums(matrix)
    columns = column_sums(matrix)
    lines = [
        "Суммы строк: " + " ".join(str(value) for value in rows),
        "Суммы столбцов: " + " ".join(str(value) for value in columns),
        f"Результат варианта: {selected_sum(matrix)}",
    ]
    return "\n".join(lines) + "\n"


def write_report(path, text):
    """Записать отчёт целиком: старый файл заменяется только готовым текстом."""
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def main(argv):
    input_path = Path(argv[1]) if len(argv) > 1 else Path(__file__).with_name("matrix.txt")
    report_path = Path(argv[2]) if len(argv) > 2 else Path(__file__).with_name("report.txt")

    try:
        matrix = read_matrix(input_path)
    except FileNotFoundError:
        print(f"Файл не найден: {input_path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Файл {input_path} не удалось прочитать в UTF-8", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Неверный формат данных: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Ошибка доступа к файлу {input_path}: {error}", file=sys.stderr)
        return 1

    try:
        write_report(report_path, build_report(matrix))
    except OSError as error:
        print(f"Не удалось записать отчёт {report_path}: {error}", file=sys.stderr)
        return 1

    print(f"Отчёт записан: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
