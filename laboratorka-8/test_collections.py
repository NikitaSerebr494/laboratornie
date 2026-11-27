"""Проверки для collections_lab.py и записей варианта 11."""

import contextlib
import io

from collections_lab import (
    all_topics,
    common_topics,
    print_word_counts,
    sorted_pairs,
    titles_in_category,
    totals_by_category,
    word_counts,
)
from variant import RECORDS

SAMPLE = [
    {"title": "A", "category": "основное", "amount": 4},
    {"title": "B", "category": "дополнительное", "amount": 2},
    {"title": "C", "category": "основное", "amount": 3},
]


def test_word_counts_basic():
    assert word_counts("Python, python! SQL") == {"python": 2, "sql": 1}


def test_word_counts_punctuation_only():
    assert word_counts("!!!") == {}


def test_word_counts_empty_text():
    assert word_counts("") == {}


def test_sorted_pairs_by_alphabet():
    counts = word_counts("SQL python, Python!")
    assert sorted_pairs(counts) == [("python", 2), ("sql", 1)]


def test_print_word_counts_order():
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print_word_counts("SQL python, Python!")
    assert buffer.getvalue() == "python: 2\nsql: 1\n"


def test_common_and_all_topics():
    first = ["python", "sql", "python"]
    second = ["sql", "git"]
    assert common_topics(first, second) == ["sql"]
    assert all_topics(first, second) == ["git", "python", "sql"]


def test_topics_with_empty_list():
    topics = ["python", "sql", "python"]
    assert common_topics(topics, []) == []
    assert all_topics(topics, []) == ["python", "sql"]
    assert common_topics([], topics) == []
    assert all_topics([], topics) == ["python", "sql"]


def test_totals_by_category_sample():
    assert totals_by_category(SAMPLE) == {"основное": 7, "дополнительное": 2}


def test_titles_in_category_sample():
    assert titles_in_category(SAMPLE, "основное") == ["A", "C"]
    assert titles_in_category(SAMPLE, "нет") == []


def test_totals_of_empty_records():
    assert totals_by_category([]) == {}


def test_sample_records_not_mutated():
    expected = [record.copy() for record in SAMPLE]
    totals_by_category(SAMPLE)
    titles_in_category(SAMPLE, "основное")
    assert SAMPLE == expected


def test_variant_records_shape():
    assert len(RECORDS) >= 5
    categories = {record["category"] for record in RECORDS}
    assert len(categories) >= 3
    assert len(categories) < len(RECORDS)
    for record in RECORDS:
        assert set(record) == {"title", "category", "amount"}
        assert isinstance(record["amount"], int)
        assert record["amount"] >= 0


def test_variant_totals():
    assert totals_by_category(RECORDS) == {
        "суккуленты": 12,
        "орхидеи": 3,
        "папоротники": 1,
    }


def test_variant_titles():
    assert titles_in_category(RECORDS, "суккуленты") == [
        "Алоэ вера",
        "Толстянка",
        "Эхинопсис",
    ]
    assert titles_in_category(RECORDS, "орхидеи") == ["Фаленопсис", "Дендробиум"]
    assert titles_in_category(RECORDS, "кактусы") == []


def test_variant_records_not_mutated():
    expected = [record.copy() for record in RECORDS]
    totals_by_category(RECORDS)
    titles_in_category(RECORDS, "суккуленты")
    assert RECORDS == expected


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
