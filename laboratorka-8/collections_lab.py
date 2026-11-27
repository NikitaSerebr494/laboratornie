"""Практикум по коллекциям: словари, множества, кортежи.

Задания 1-3 и функции индивидуального варианта 11.
Интерактивная часть (задание 3) запускается под if __name__ == "__main__":
"""

PUNCTUATION = ".,!?:"


def word_counts(text):
    """Вернуть словарь «слово — количество» для text."""
    counts = {}
    for token in text.split():
        word = token.lower().strip(PUNCTUATION)
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def sorted_pairs(counts):
    """Пары (слово, количество) по алфавиту."""
    return sorted(counts.items())


def print_word_counts(text):
    """Напечатать пары «слово — количество» по алфавиту."""
    for word, count in sorted_pairs(word_counts(text)):
        print(f"{word}: {count}")


def common_topics(first, second):
    """Отсортированный список общих тем."""
    return sorted(set(first) & set(second))


def all_topics(first, second):
    """Отсортированный список всех уникальных тем."""
    return sorted(set(first) | set(second))


def totals_by_category(records):
    """Словарь сумм amount по категориям."""
    totals = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0) + record["amount"]
    return totals


def titles_in_category(records, category):
    """Названия записей нужной категории в исходном порядке."""
    return [record["title"] for record in records if record["category"] == category]


def record_demo():
    """Задание 3: словарь записи, кортеж, распаковка."""
    lesson = {"title": "Множества", "hours": 2}
    lesson["hours"] = 3
    lesson["completed"] = False

    title_and_hours = (lesson["title"], lesson["hours"])
    title, hours = title_and_hours

    print("Запись:", lesson)
    print("Кортеж:", title_and_hours)
    print("После распаковки:", title, hours)
    return lesson, title_and_hours


if __name__ == "__main__":
    print("Пары по алфавиту:")
    print_word_counts("Python, python! SQL. И ещё python: SQL?")
    print()
    record_demo()
