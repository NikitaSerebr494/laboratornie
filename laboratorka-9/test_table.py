"""Проверки для table.py."""

from table import column_sums, diagonal_pattern, row_sums, transform

CONTROL = [[-2, 0, 3], [4, -5, 6]]


def test_row_and_column_sums():
    matrix = [[1, 2, 3], [4, 5, 6]]
    assert row_sums(matrix) == [6, 15]
    assert column_sums(matrix) == [5, 7, 9]


def test_single_element():
    assert row_sums([[7]]) == [7]
    assert column_sums([[7]]) == [7]
    assert diagonal_pattern(1) == [[0]]


def test_column_matrix():
    matrix = [[1], [-1], [0]]
    assert row_sums(matrix) == [1, -1, 0]
    assert column_sums(matrix) == [0]


def test_empty_matrix():
    assert row_sums([]) == []
    assert column_sums([]) == []
    assert transform([]) == []


def test_diagonal_pattern_size_3():
    assert diagonal_pattern(3) == [[0, 1, 1], [2, 0, 1], [2, 2, 0]]


def test_transform_variant_2():
    assert transform(CONTROL) == [[-2, 0, 1], [1, -5, 1]]


def test_transform_does_not_change_source():
    result = transform(CONTROL)
    result[0][0] = 99
    assert result is not CONTROL
    assert CONTROL == [[-2, 0, 3], [4, -5, 6]]
    for new_row, old_row in zip(result, CONTROL):
        assert new_row is not old_row


def test_sums_do_not_change_source():
    matrix = [[1, 2, 3], [4, 5, 6]]
    snapshot = [row[:] for row in matrix]
    row_sums(matrix)
    column_sums(matrix)
    assert matrix == snapshot


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
