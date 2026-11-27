"""Чтение матрицы из файла и сумма элементов по условию варианта 2."""

from pathlib import Path


def read_matrix(path):
    """Прочитать прямоугольную матрицу из текстового файла UTF-8.

    Первая строка — два положительных числа: количество строк и столбцов.
    Затем ровно столько строк, в каждой ровно столько целых чисел.
    Пустые и лишние строки — ошибка, один перевод строки в конце файла допустим.
    """
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    if not lines:
        raise ValueError("файл пуст: нет строки заголовка")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("строка 1: заголовок должен содержать два числа — строки и столбцы")

    try:
        rows, columns = (int(token) for token in header)
    except ValueError:
        raise ValueError("строка 1: в заголовке должны быть целые числа") from None

    if rows <= 0 or columns <= 0:
        raise ValueError("строка 1: размеры матрицы должны быть положительными")

    data_lines = lines[1:]
    matrix = []
    for number, line in enumerate(data_lines, start=2):
        if number - 1 > rows:
            raise ValueError(f"строка {number}: лишние данные после последней строки матрицы")
        tokens = line.split()
        if not tokens:
            raise ValueError(f"строка {number}: пустая строка вместо {columns} чисел")
        if len(tokens) != columns:
            raise ValueError(
                f"строка {number}: ожидалось {columns} чисел, получено {len(tokens)}"
            )
        try:
            matrix.append([int(token) for token in tokens])
        except ValueError:
            raise ValueError(f"строка {number}: все значения должны быть целыми числами") from None

    if len(matrix) < rows:
        raise ValueError(f"недостаточно строк данных: нужно {rows}, найдено {len(matrix)}")

    return matrix


def selected_sum(matrix):
    """Вариант 2: сумма отрицательных элементов, иначе 0."""
    return sum(value for row in matrix for value in row if value < 0)
