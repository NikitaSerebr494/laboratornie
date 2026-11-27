"""Проверка записей и операции над списком. Без ввода-вывода и глобального состояния.

Список записей передаётся аргументом. Функции add_record, set_completed и
delete_record меняют переданный список и возвращают результат операции:
add_record — новую запись, set_completed и delete_record — True при успехе
и False, если запись с таким ID не найдена. find_records и statistics
исходный список не меняют.
"""

REQUIRED_FIELDS = ("id", "title", "category", "amount", "completed")


def validate_records(records):
    """Проверить структуру списка записей, при нарушении бросить ValueError."""
    if not isinstance(records, list):
        raise ValueError("корень JSON должен быть списком записей")

    seen_ids = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"запись {index}: ожидался объект")

        for field in REQUIRED_FIELDS:
            if field not in record:
                raise ValueError(f"запись {index}: нет обязательного поля {field}")

        if type(record["id"]) is not int:
            raise ValueError(f"запись {index}: id должен быть целым числом")
        if record["id"] <= 0:
            raise ValueError(f"запись {index}: id должен быть положительным")
        if record["id"] in seen_ids:
            raise ValueError(f"запись {index}: повторяющийся id {record['id']}")
        seen_ids.add(record["id"])

        for field in ("title", "category"):
            value = record[field]
            if type(value) is not str:
                raise ValueError(f"запись {index}: поле {field} должно быть строкой")
            if not value.strip():
                raise ValueError(f"запись {index}: поле {field} не должно быть пустым")

        if type(record["amount"]) is not int:
            raise ValueError(
                f"запись {index}: amount должен быть целым числом, "
                f"а не {type(record['amount']).__name__}"
            )
        if record["amount"] < 0:
            raise ValueError(f"запись {index}: amount не может быть отрицательным")

        if type(record["completed"]) is not bool:
            raise ValueError(f"запись {index}: completed должен быть логическим значением")


def add_record(records, title, category, amount):
    """Добавить запись со статусом False и вернуть её."""
    title = title.strip()
    category = category.strip()
    if not title:
        raise ValueError("название не должно быть пустым")
    if not category:
        raise ValueError("категория не должна быть пустой")
    if type(amount) is not int or amount < 0:
        raise ValueError("количество должно быть целым неотрицательным числом")

    record = {
        "id": max((record["id"] for record in records), default=0) + 1,
        "title": title,
        "category": category,
        "amount": amount,
        "completed": False,
    }
    records.append(record)
    return record


def find_records(records, query):
    """Записи, в названии которых есть query без учёта регистра."""
    query = query.strip().lower()
    if not query:
        raise ValueError("поисковый запрос не должен быть пустым")
    return [record for record in records if query in record["title"].lower()]


def set_completed(records, record_id, completed):
    """Установить статус записи. True при успехе, False если ID не найден."""
    if type(completed) is not bool:
        raise ValueError("статус должен быть логическим значением")
    for record in records:
        if record["id"] == record_id:
            record["completed"] = completed
            return True
    return False


def delete_record(records, record_id):
    """Удалить запись по ID. True при успехе, False если ID не найден."""
    for index, record in enumerate(records):
        if record["id"] == record_id:
            del records[index]
            return True
    return False


def statistics(records):
    """Сводка: количество записей, статусы, сумма amount и суммы по категориям."""
    completed = sum(1 for record in records if record["completed"])
    by_category = {}
    for record in records:
        category = record["category"].strip()
        by_category[category] = by_category.get(category, 0) + record["amount"]

    return {
        "total": len(records),
        "completed": completed,
        "pending": len(records) - completed,
        "amount": sum(record["amount"] for record in records),
        "by_category": by_category,
    }
