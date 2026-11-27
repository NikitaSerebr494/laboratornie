"""Ввод прямоугольной матрицы, суммы, преобразование и диагональный узор."""

from table import column_sums, diagonal_pattern, row_sums, transform


def read_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Нужно целое число, попробуйте снова.")


def read_row(width):
    while True:
        raw = input("  строка: ").strip()
        if not raw:
            print(f"  пустая строка, нужно {width} чисел.")
            continue
        try:
            values = [int(part) for part in raw.split()]
        except ValueError:
            print("  только целые числа через пробел.")
            continue
        if len(values) != width:
            print(f"  длина строки {len(values)}, нужно {width}.")
            continue
        return values


def read_matrix():
    while True:
        rows = read_int("Число строк: ")
        if rows < 0:
            print("Число строк не может быть отрицательным.")
            continue
        if rows == 0:
            return []
        width = read_int("Число столбцов: ")
        if width < 1:
            print("Число столбцов должно быть положительным.")
            continue
        print(f"Введите {rows} строк по {width} целых чисел:")
        return [read_row(width) for _ in range(rows)]


def print_matrix(title, matrix):
    print(title)
    if not matrix:
        print("  (пустая матрица)")
        return
    for row in matrix:
        print("  " + " ".join(str(value) for value in row))


def main():
    matrix = read_matrix()

    print()
    print("Суммы строк:", row_sums(matrix))
    print("Суммы столбцов:", column_sums(matrix))

    transformed = transform(matrix)
    print()
    print_matrix("Исходная таблица:", matrix)
    print_matrix("После преобразования (вариант 2, положительные -> 1):", transformed)

    print()
    while True:
        size = read_int("Положительный размер узора: ")
        if size > 0:
            break
        print("Размер должен быть положительным.")

    print()
    print_matrix(f"Диагональный узор {size}x{size}:", diagonal_pattern(size))


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
