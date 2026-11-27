"""Проверки files_lab.py и вспомогательных функций main.py."""

import contextlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from files_lab import read_matrix, selected_sum
from main import build_report, read_positive_integer

MATRIX_TEXT = "2 3\n1 -2 3\n4 0 -6\n"


def make_file(directory, text):
    path = Path(directory) / "matrix.txt"
    path.write_text(text, encoding="utf-8")
    return path


def expect_value_error(path, part=None):
    try:
        read_matrix(path)
    except ValueError as error:
        if part is not None:
            assert part in str(error), f"в сообщении нет {part!r}: {error}"
    else:
        assert False, "Ошибка не обнаружена"


def test_single_element():
    with TemporaryDirectory() as directory:
        path = make_file(directory, "1 1\n7\n")
        assert read_matrix(path) == [[7]]


def test_two_rows_matrix():
    with TemporaryDirectory() as directory:
        path = make_file(directory, MATRIX_TEXT)
        assert read_matrix(path) == [[1, -2, 3], [4, 0, -6]]


def test_trailing_newline_is_allowed():
    with TemporaryDirectory() as directory:
        assert read_matrix(make_file(directory, "1 1\n7\n")) == [[7]]
        assert read_matrix(make_file(directory, "1 1\n7")) == [[7]]


def test_empty_file():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, ""))


def test_zero_rows_header():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "0 3\n"))


def test_short_row_reports_line_two():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "1 2\n1\n"), "строка 2")


def test_non_numeric_cell_reports_line_two():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "1 2\n1 x\n"), "строка 2")


def test_extra_data_rows():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "1 1\n7\n8\n"))


def test_empty_line_inside():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "1 1\n\n7\n"), "строка 2")


def test_header_without_two_numbers():
    with TemporaryDirectory() as directory:
        expect_value_error(make_file(directory, "1\n7\n"))


def test_missing_path():
    with TemporaryDirectory() as directory:
        missing = Path(directory) / "missing.txt"
        try:
            read_matrix(missing)
        except FileNotFoundError:
            pass
        else:
            assert False, "Ошибка не обнаружена"


def test_read_positive_integer_skips_bad_input():
    answers = iter(["abc", "0", "-2", "3"])
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=lambda prompt="": next(answers)):
        with contextlib.redirect_stdout(buffer):
            assert read_positive_integer() == 3
    output = buffer.getvalue()
    assert "не целое число" in output
    assert "больше нуля" in output


def test_reported_values_for_matrix_txt():
    with TemporaryDirectory() as directory:
        matrix = read_matrix(make_file(directory, MATRIX_TEXT))
    assert build_report(matrix) == (
        "Суммы строк: 2 -2\n"
        "Суммы столбцов: 5 -2 -3\n"
        "Результат варианта: -8\n"
    )


def test_selected_sum_without_negatives():
    assert selected_sum([[1, 2], [3, 4]]) == 0
    assert selected_sum([]) == 0


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
