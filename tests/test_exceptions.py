import unittest

from src.exceptions.argument_exception import ArgumentException

"""
Тестирование функций кастомных исключений
"""
class TestUtils(unittest.TestCase):
    """
    Тестирует функцию check_arg с валидными аргументами
    """
    def test_check_arg_valid(self):
        ArgumentException.check_arg("hello", str)
        ArgumentException.check_arg(123, int)
        ArgumentException.check_arg(None, str, check_none=True)

    """
    Тестирует функцию check_arg с невалидными данными
    """
    def test_check_arg_invalid_type(self):
        with self.assertRaises(ArgumentException):
            ArgumentException.check_arg(123, str)

    """
    Тестирует функцию check_max_len с валидными для сравнения данными
    """
    def test_check_max_len_valid(self):
        ArgumentException.check_max_len("1" * 255, 255)


    """
    Тестирует функцию check_max_len с невалидными данными для сравнения
    """
    def test_check_max_len_exceeded(self):
        long_string = "a" * 256
        with self.assertRaises(ArgumentException):
            ArgumentException.check_max_len(long_string, 255)

    """
    Тестирует функцию check_exact_len с валидными данными
    """
    def test_check_exact_len_valid(self):
        valid_string = "1" * 5
        ArgumentException.check_exact_length(valid_string, 5)
        assert True

    """
    Тестирует функцию check_exact_len с невалдиными данными
    """
    def test_check_exact_len_invalid(self):
        valid_string = "1"
        with self.assertRaises(ArgumentException):
            ArgumentException.check_exact_length(valid_string, 0)

if __name__ == "__main__":
    unittest.main()
