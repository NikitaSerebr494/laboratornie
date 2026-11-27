"""Проверки логики: валидация, добавление, поиск, статус, удаление, статистика."""

from logic import (
    add_record,
    delete_record,
    find_records,
    set_completed,
    statistics,
    validate_records,
)

SAMPLE = [
    {"id": 1, "title": "Основная листовка", "category": "листовки", "amount": 4, "completed": False},
    {"id": 2, "title": "Дополнительный буклет", "category": "буклеты", "amount": 2, "completed": True},
]


def fresh_records():
    return [record.copy() for record in SAMPLE]


def expect_value_error(callable_object, *args):
    try:
        callable_object(*args)
    except ValueError:
        pass
    else:
        assert False, f"Ошибка не обнаружена: {callable_object.__name__}{args!r}"


def test_validate_accepts_sample_and_extra_keys():
    validate_records(SAMPLE)
    validate_records([{"id": 7, "title": "x", "category": "y", "amount": 0,
                       "completed": False, "note": "лишний ключ"}])
    validate_records([])


def test_validate_rejects_bad_fields():
    cases = [
        {},
        [1],
        [{"title": "x", "category": "y", "amount": 1, "completed": False}],
        [{"id": 1, "category": "y", "amount": 1, "completed": False}],
        [{"id": 1, "title": "x", "amount": 1, "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "amount": 1}],
        [{"id": True, "title": "x", "category": "y", "amount": 1, "completed": False}],
        [{"id": 1.0, "title": "x", "category": "y", "amount": 1, "completed": False}],
        [{"id": 0, "title": "x", "category": "y", "amount": 1, "completed": False}],
        [{"id": -3, "title": "x", "category": "y", "amount": 1, "completed": False}],
        [{"id": 1, "title": "   ", "category": "y", "amount": 1, "completed": False}],
        [{"id": 1, "title": 5, "category": "y", "amount": 1, "completed": False}],
        [{"id": 1, "title": "x", "category": "", "amount": 1, "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "amount": -1, "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "amount": "5", "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "amount": True, "completed": False}],
        [{"id": 1, "title": "x", "category": "y", "amount": 1, "completed": "false"}],
        [{"id": 1, "title": "x", "category": "y", "amount": 1, "completed": 0}],
        [
            {"id": 1, "title": "x", "category": "y", "amount": 1, "completed": False},
            {"id": 1, "title": "z", "category": "y", "amount": 2, "completed": True},
        ],
    ]
    for case in cases:
        expect_value_error(validate_records, case)


def test_add_record_defaults_and_strips():
    records = []
    record = add_record(records, "  Python  ", "  учёба  ", 5)
    assert record == {
        "id": 1,
        "title": "Python",
        "category": "учёба",
        "amount": 5,
        "completed": False,
    }
    assert records == [record]


def test_add_allows_duplicate_titles():
    records = []
    first = add_record(records, "Визитки", "визитки", 100)
    second = add_record(records, "Визитки", "визитки", 200)
    assert first["id"] == 1
    assert second["id"] == 2
    assert len(records) == 2


def test_add_rejects_bad_values():
    records = []
    expect_value_error(add_record, records, "   ", "учёба", 1)
    expect_value_error(add_record, records, "x", "  ", 1)
    expect_value_error(add_record, records, "x", "y", -1)
    expect_value_error(add_record, records, "x", "y", "5")
    expect_value_error(add_record, records, "x", "y", True)
    assert records == []


def test_new_id_after_delete():
    records = fresh_records()
    assert delete_record(records, 1) is True
    new_record = add_record(records, "Новая листовка", "листовки", 1)
    assert new_record["id"] == 3
    assert [record["id"] for record in records] == [2, 3]


def test_find_case_insensitive():
    records = fresh_records()
    assert find_records(records, "ОСНОВ") == [records[0]]
    assert find_records(records, " бук ") == [records[1]]
    assert find_records(records, "нет такого") == []


def test_find_rejects_empty_query():
    records = fresh_records()
    expect_value_error(find_records, records, "")
    expect_value_error(find_records, records, "   ")


def test_set_completed():
    records = fresh_records()
    assert set_completed(records, 1, True) is True
    assert records[0]["completed"] is True
    assert set_completed(records, 1, False) is True
    assert records[0]["completed"] is False
    assert set_completed(records, 999, True) is False
    assert records == fresh_records()
    expect_value_error(set_completed, records, 1, "да")


def test_delete_record():
    records = fresh_records()
    assert delete_record(records, 999) is False
    assert delete_record(records, 1) is True
    assert [record["id"] for record in records] == [2]


def test_statistics_sample():
    assert statistics(SAMPLE) == {
        "total": 2,
        "completed": 1,
        "pending": 1,
        "amount": 6,
        "by_category": {"листовки": 4, "буклеты": 2},
    }


def test_statistics_empty():
    assert statistics([]) == {
        "total": 0,
        "completed": 0,
        "pending": 0,
        "amount": 0,
        "by_category": {},
    }


def test_statistics_strips_categories():
    records = [
        {"id": 1, "title": "a", "category": "  визитки ", "amount": 3, "completed": False},
        {"id": 2, "title": "b", "category": "визитки", "amount": 4, "completed": True},
    ]
    stats = statistics(records)
    assert stats["by_category"] == {"визитки": 7}
    assert sorted(stats["by_category"]) == ["визитки"]


def test_read_only_operations_do_not_change_records():
    records = fresh_records()
    find_records(records, "буклет")
    statistics(records)
    assert records == fresh_records()


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
