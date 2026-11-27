"""Основная программа: сводка по todos.json, выборка варианта 10 и selected.json."""

import json
import os
import sys
from pathlib import Path

from analysis import completion_counts, select_tasks, top_users, validate_todos

BASE_DIR = Path(__file__).resolve().parent
TODOS_PATH = BASE_DIR / "todos.json"
SELECTED_PATH = BASE_DIR / "selected.json"


def read_int(prompt, minimum, too_small_message):
    """Повторять ввод, пока не получено целое число не меньше minimum."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Это не целое число, попробуйте снова.")
            continue
        if value < minimum:
            print(too_small_message)
            continue
        return value


def load_todos(path):
    """Прочитать JSON и проверить его структуру."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_todos(data)
    return data


def save_selected(values, path):
    """Записать выборку целиком: старый файл заменяется только готовым текстом."""
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main():
    try:
        todos = load_todos(TODOS_PATH)
    except FileNotFoundError:
        print(f"Файл не найден: {TODOS_PATH}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Файл {TODOS_PATH} не удалось прочитать в UTF-8", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(
            f"Некорректный JSON: {error.msg} (строка {error.lineno}, столбец {error.colno})",
            file=sys.stderr,
        )
        return 1
    except ValueError as error:
        print(f"Ошибка структуры данных: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Ошибка доступа к файлу {TODOS_PATH}: {error}", file=sys.stderr)
        return 1

    counts = completion_counts(todos)
    print(f"Всего задач: {len(todos)}, выполнено: {sum(counts.values())}")
    print("Выполнено по пользователям:", counts)
    print("Лидеры:", top_users(counts))
    print()

    user_id = read_int(
        "Пользователь (положительное целое): ", 1, "Число должно быть больше нуля."
    )
    threshold = read_int(
        "Минимальная длина названия: ", 0, "Порог не может быть отрицательным."
    )

    selected = select_tasks(todos, user_id, threshold)
    print("Выбранные задачи:", selected)

    try:
        save_selected(selected, SELECTED_PATH)
    except OSError as error:
        print(f"Не удалось записать {SELECTED_PATH}: {error}", file=sys.stderr)
        return 1

    print(f"Выборка сохранена: {SELECTED_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
