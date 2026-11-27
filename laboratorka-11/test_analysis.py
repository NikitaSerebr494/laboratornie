"""Проверки analysis.py на учебном наборе и граничных случаях варианта 10."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from analysis import completion_counts, select_tasks, top_users, validate_todos

TODOS = [
    {"id": 1, "userId": 5, "title": "Ваза", "completed": True},
    {"id": 2, "userId": 5, "title": "Число", "completed": False},
    {"id": 3, "userId": 10, "title": "Строка", "completed": True},
    {"id": 4, "userId": 10, "title": "Файл", "completed": True},
    {"id": 5, "userId": 5, "title": "Спичка", "completed": True},
]


def expect_value_error(data):
    try:
        validate_todos(data)
    except ValueError:
        pass
    else:
        assert False, f"Ошибка не обнаружена: {data!r}"


def test_sample_counts_and_leaders():
    counts = completion_counts(TODOS)
    assert counts == {5: 2, 10: 2}
    assert top_users(counts) == [5, 10]
    assert sum(counts.values()) == 4


def test_sample_selection():
    assert select_tasks(TODOS, 5, 5) == [2, 5]
    assert select_tasks(TODOS, 10, 0) == [3, 4]


def test_empty_todos():
    assert completion_counts([]) == {}
    assert top_users({}) == []
    assert select_tasks([], 5, 5) == []


def test_only_uncompleted():
    todos = [
        {"id": 1, "userId": 5, "title": "Ваза", "completed": False},
        {"id": 2, "userId": 5, "title": "Число", "completed": False},
    ]
    counts = completion_counts(todos)
    assert counts == {5: 0}
    assert top_users(counts) == []
    assert select_tasks(todos, 99, 0) == []


def test_single_leader():
    todos = [
        {"id": 1, "userId": 5, "title": "Ваза", "completed": True},
        {"id": 2, "userId": 7, "title": "Число", "completed": False},
    ]
    assert top_users(completion_counts(todos)) == [5]


def test_ties_between_leaders():
    todos = [
        {"id": 1, "userId": 7, "title": "Ваза", "completed": True},
        {"id": 2, "userId": 5, "title": "Число", "completed": True},
        {"id": 3, "userId": 5, "title": "Строка", "completed": True},
        {"id": 4, "userId": 7, "title": "Файл", "completed": True},
        {"id": 5, "userId": 9, "title": "Спичка", "completed": False},
    ]
    assert top_users(completion_counts(todos)) == [5, 7]


def test_variant_10_table():
    assert select_tasks(TODOS, 5, 5) == [2, 5]


def test_variant_10_unknown_user():
    assert select_tasks(TODOS, 999, 5) == []


def test_variant_10_without_matches():
    assert select_tasks(TODOS, 5, 100) == []


def test_variant_10_threshold_boundary():
    assert select_tasks(TODOS, 5, 4) == [1, 2, 5]
    assert select_tasks(TODOS, 5, 5) == [2, 5]
    assert select_tasks(TODOS, 5, 6) == [5]
    assert select_tasks(TODOS, 5, 7) == []


def test_validate_rejects_bad_data():
    cases = [
        {},
        [1],
        [{"userId": 5, "title": "x", "completed": True}],
        [{"id": 1, "title": "x", "completed": True}],
        [{"id": 1, "userId": 5, "completed": True}],
        [{"id": 1, "userId": 5, "title": "x"}],
        [{"id": 1, "userId": 5, "title": "", "completed": True}],
        [{"id": 1, "userId": 5, "title": "   ", "completed": True}],
        [{"id": 1, "userId": 5, "title": 7, "completed": True}],
        [{"id": 1, "userId": 5, "title": "x", "completed": "false"}],
        [{"id": 1, "userId": 5, "title": "x", "completed": 0}],
        [{"id": True, "userId": 5, "title": "x", "completed": True}],
        [{"id": 1.0, "userId": 5, "title": "x", "completed": True}],
        [{"id": 0, "userId": 5, "title": "x", "completed": True}],
        [{"id": 1, "userId": -5, "title": "x", "completed": True}],
        [
            {"id": 1, "userId": 5, "title": "x", "completed": True},
            {"id": 1, "userId": 7, "title": "y", "completed": False},
        ],
    ]
    for case in cases:
        expect_value_error(case)


def test_extra_keys_allowed():
    data = [{"id": 1, "userId": 5, "title": "x", "completed": True, "note": "ok"}]
    validate_todos(data)


def test_saved_selection_roundtrip():
    selection = select_tasks(TODOS, 5, 5)
    with TemporaryDirectory() as directory:
        path = Path(directory) / "selected.json"
        path.write_text(
            json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        assert json.loads(path.read_text(encoding="utf-8")) == selection


def test_source_records_not_changed():
    expected = [record.copy() for record in TODOS]
    validate_todos(TODOS)
    completion_counts(TODOS)
    select_tasks(TODOS, 5, 5)
    assert TODOS == expected


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
