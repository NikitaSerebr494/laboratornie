"""Индивидуальный вариант 11 — «Коллекция растений».

amount — количество растений, целое неотрицательное число.
"""

from collections_lab import titles_in_category, totals_by_category

VARIANT = 11
DOMAIN = "Коллекция растений"
UNIT = "количество растений"

RECORDS = [
    {"title": "Алоэ вера", "category": "суккуленты", "amount": 3},
    {"title": "Фаленопсис", "category": "орхидеи", "amount": 2},
    {"title": "Нефролепис", "category": "папоротники", "amount": 1},
    {"title": "Толстянка", "category": "суккуленты", "amount": 5},
    {"title": "Дендробиум", "category": "орхидеи", "amount": 1},
    {"title": "Эхинопсис", "category": "суккуленты", "amount": 4},
]


if __name__ == "__main__":
    print(f"Вариант {VARIANT}: {DOMAIN}, amount — {UNIT}")
    print()
    totals = totals_by_category(RECORDS)
    for category, total in sorted(totals.items()):
        titles = ", ".join(titles_in_category(RECORDS, category))
        print(f"{category}: {total} ({titles})")
    print()
    print("Всего записей:", len(RECORDS))
    print("Всего растений:", sum(record["amount"] for record in RECORDS))
