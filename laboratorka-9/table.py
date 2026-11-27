"""Табличные операции: суммы строк и столбцов, диагональный узор, преобразование.

Индивидуальный вариант 2: положительные элементы заменяются единицами.
Функции ничего не печатают и не меняют полученную матрицу.
"""


def row_sums(matrix):
    """Список сумм строк."""
    return [sum(row) for row in matrix]


def column_sums(matrix):
    """Список сумм столбцов для непустой прямоугольной матрицы."""
    if not matrix:
        return []
    return [sum(row[index] for row in matrix) for index in range(len(matrix[0]))]


def diagonal_pattern(size):
    """Квадратная таблица size x size: 0 на диагонали, 1 выше, 2 ниже."""
    if size < 1:
        raise ValueError("размер должен быть не меньше 1")
    return [
        [0 if row == column else 1 if row < column else 2 for column in range(size)]
        for row in range(size)
    ]


def transform(matrix):
    """Новая матрица той же формы: положительные элементы заменены единицами."""
    return [[1 if value > 0 else value for value in row] for row in matrix]
