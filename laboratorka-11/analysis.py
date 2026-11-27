"""Проверка учебного набора задач, подсчёт лидеров и выборка варианта 10.

Вариант 10: задачи пользователя, у которых длина названия не меньше порога.
"""

REQUIRED_FIELDS = ("id", "userId", "title", "completed")


def validate_todos(data):
    """Проверить структуру набора задач, при нарушении бросить ValueError."""
    if not isinstance(data, list):
        raise ValueError("корень JSON должен быть списком задач")

    seen_ids = set()
    for index, record in enumerate(data, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"запись {index}: ожидался объект, получено {type(record).__name__}")

        for field in REQUIRED_FIELDS:
            if field not in record:
                raise ValueError(f"запись {index}: нет обязательного поля {field}")

        for field in ("id", "userId"):
            value = record[field]
            if type(value) is not int:
                raise ValueError(
                    f"запись {index}: поле {field} должно быть целым числом, "
                    f"а не {type(value).__name__}"
                )
            if value <= 0:
                raise ValueError(f"запись {index}: поле {field} должно быть положительным")

        title = record["title"]
        if type(title) is not str:
            raise ValueError(f"запись {index}: поле title должно быть строкой")
        if not title.strip():
            raise ValueError(f"запись {index}: поле title не должно быть пустым")

        if type(record["completed"]) is not bool:
            raise ValueError(f"запись {index}: поле completed должно быть логическим значением")

        if record["id"] in seen_ids:
            raise ValueError(f"запись {index}: повторяющийся id {record['id']}")
        seen_ids.add(record["id"])


def completion_counts(todos):
    """Словарь «пользователь — число выполненных задач», включая нули."""
    counts = {}
    for record in todos:
        user = record["userId"]
        counts.setdefault(user, 0)
        if record["completed"]:
            counts[user] += 1
    return counts


def top_users(counts):
    """Отсортированные идентификаторы пользователей с максимумом выполненных задач."""
    if not counts:
        return []
    best = max(counts.values())
    if best == 0:
        return []
    return sorted(user for user, value in counts.items() if value == best)


def select_tasks(todos, user_id, parameter=None):
    """Вариант 10: id задач пользователя, где длина названия не меньше порога."""
    if parameter is None:
        raise ValueError("для варианта 10 нужен порог длины названия")
    if type(parameter) is not int or parameter < 0:
        raise ValueError("порог должен быть целым неотрицательным числом")

    return [
        record["id"]
        for record in todos
        if record["userId"] == user_id and len(record["title"]) >= parameter
    ]
