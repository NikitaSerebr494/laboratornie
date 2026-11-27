"""Итоговый проект: учёт печатных заказов. Вариант 10.

amount — количество страниц, completed — заказ напечатан.
"""

import json
import sys
from pathlib import Path

from logic import (
    add_record,
    delete_record,
    find_records,
    set_completed,
    statistics,
    validate_records,
)
from storage import load_records, save_records

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.json"

UNIT = "стр."
STATUS_DONE = "напечатан"
STATUS_TODO = "не напечатан"

MENU = """
1. Показать записи
2. Добавить запись
3. Найти записи
4. Изменить статус
5. Удалить запись
6. Статистика
7. Сохранить
8. Выход
"""


def show_records(records):
    if not records:
        print("Записей нет.")
        return
    for record in records:
        status = STATUS_DONE if record["completed"] else STATUS_TODO
        print(
            f"{record['id']}. {record['title']} | {record['category']} | "
            f"{record['amount']} {UNIT} | {status}"
        )


def read_text(prompt, error_message="Строка не должна быть пустой."):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(error_message)


def read_integer(prompt, minimum, too_small_message):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Нужно целое число, попробуйте снова.")
            continue
        if value < minimum:
            print(too_small_message)
            continue
        return value


def read_amount():
    return read_integer("Количество страниц: ", 0, "Количество не может быть отрицательным.")


def read_record_id():
    return read_integer("ID записи: ", 1, "ID должен быть положительным.")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "да":
            return True
        if answer == "нет":
            return False
        print("Ответьте «да» или «нет».")


def handle_add(records):
    title = read_text("Название: ")
    category = read_text("Категория: ")
    amount = read_amount()
    try:
        record = add_record(records, title, category, amount)
    except ValueError as error:
        print(f"Не удалось добавить запись: {error}")
        return
    print(f"Добавлена запись с ID {record['id']}.")


def handle_find(records):
    query = read_text("Часть названия: ", "Поисковый запрос не должен быть пустым.")
    found = find_records(records, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_records(found)


def handle_set_status(records):
    record_id = read_record_id()
    completed = ask_yes_no("Отметить как напечатанный? (да/нет): ")
    if set_completed(records, record_id, completed):
        print("Статус изменён.")
    else:
        print(f"Запись с ID {record_id} не найдена, данные не изменены.")


def handle_delete(records):
    record_id = read_record_id()
    if not ask_yes_no("Удалить запись? (да/нет): "):
        print("Удаление отменено.")
        return
    if delete_record(records, record_id):
        print("Запись удалена.")
    else:
        print(f"Запись с ID {record_id} не найдена.")


def handle_statistics(records):
    stats = statistics(records)
    print(
        f"Всего: {stats['total']}, напечатано: {stats['completed']}, "
        f"не напечатано: {stats['pending']}, сумма страниц: {stats['amount']}"
    )
    if stats["by_category"]:
        print("По категориям:")
        for category in sorted(stats["by_category"]):
            print(f"  {category}: {stats['by_category'][category]}")


def save_data(records, path):
    try:
        save_records(path, records)
    except OSError as error:
        print(f"Не удалось сохранить данные: {error}")
        return False
    print(f"Данные сохранены: {path.name}")
    return True


def ask_exit(records, path):
    while True:
        answer = input("Сохранить перед выходом? (да/нет): ").strip().lower()
        if answer == "нет":
            return True
        if answer == "да":
            return save_data(records, path)
        print("Ответьте «да» или «нет».")


def menu_loop(records, path):
    while True:
        print(MENU)
        choice = input("Команда: ").strip()
        if choice == "1":
            show_records(records)
        elif choice == "2":
            handle_add(records)
        elif choice == "3":
            handle_find(records)
        elif choice == "4":
            handle_set_status(records)
        elif choice == "5":
            handle_delete(records)
        elif choice == "6":
            handle_statistics(records)
        elif choice == "7":
            save_data(records, path)
        elif choice == "8":
            if ask_exit(records, path):
                print("Программа завершена.")
                return
        else:
            print("Неизвестная команда, попробуйте снова.")


def load_data(path):
    try:
        records = load_records(path)
    except FileNotFoundError:
        print(f"Файл {path.name} не найден, начинаем с пустого списка.")
        return []
    except UnicodeDecodeError:
        print(f"Файл {path.name} не в кодировке UTF-8. Исправьте файл и перезапустите программу.")
        return None
    except json.JSONDecodeError as error:
        print(
            f"Файл {path.name} содержит некорректный JSON: {error.msg} "
            f"(строка {error.lineno}, столбец {error.colno}). "
            "Исправьте файл и перезапустите программу."
        )
        return None
    except OSError as error:
        print(f"Не удалось прочитать {path.name}: {error}")
        return None

    try:
        validate_records(records)
    except ValueError as error:
        print(f"Данные не прошли проверку: {error}. Исправьте файл и перезапустите программу.")
        return None
    return records


def main():
    records = load_data(DATA_PATH)
    if records is None:
        return 1
    print(f"Загружено записей: {len(records)}.")
    try:
        menu_loop(records, DATA_PATH)
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван, программа завершена без сохранения.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
