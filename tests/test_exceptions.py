import unittest

from src.exceptions.argument_exception import ArgumentException


class TestUtils(unittest.TestCase):
    """
    Тестирование функций кастомных исключений
    """

    def test_check_arg_valid(self):
        """
        Тестирует функцию check_arg с валидными аргументами
        """
        ArgumentException.check_arg("hello", str)
        ArgumentException.check_arg(123, int)
        ArgumentException.check_arg(None, str, check_none=True)


    def test_check_arg_invalid_type(self):
        """
        Тестирует функцию check_arg с невалидными данными
        """
        with self.assertRaises(ArgumentException):
            ArgumentException.check_arg(123, str)


    def test_check_max_len_valid(self):
        """
        Тестирует функцию check_max_len с валидными для сравнения данными
        """
        ArgumentException.check_max_len("1" * 255, 255)



    def test_check_max_len_exceeded(self):
        """
        Тестирует функцию check_max_len с невалидными данными для сравнения
        """
        long_string = "a" * 256
        with self.assertRaises(ArgumentException):
            ArgumentException.check_max_len(long_string, 255)


    def test_check_exact_len_valid(self):
        """
        Тестирует функцию check_exact_len с валидными данными
        """
        valid_string = "1" * 5
        ArgumentException.check_exact_length(valid_string, 5)
        assert True


    def test_check_exact_len_invalid(self):
        """
        Тестирует функцию check_exact_len с невалдиными данными
        """
        valid_string = "1"
        with self.assertRaises(ArgumentException):
            ArgumentException.check_exact_length(valid_string, 0)

if __name__ == "__main__":
    unittest.main()
