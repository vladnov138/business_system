import unittest

from src.exceptions.argument_exception import ArgumentException
from src.utils.checker import check_arg, check_max_len, check_exact_length


class TestUtils(unittest.TestCase):
    def test_check_arg_valid(self):
        check_arg("hello", str)
        check_arg(123, int)
        check_arg(None, str, check_none=True)
        assert True

    def test_check_arg_invalid_type(self):
        with self.assertRaises(ArgumentException) as context:
            check_arg(123, str)
        assert len(str(context.exception)) > 0

    def test_check_max_len_valid(self):
        check_max_len("1" * 255, 255)

    def test_check_max_len_exceeded(self):
        long_string = "a" * 256
        with self.assertRaises(ArgumentException) as context:
            check_max_len(long_string, 255)
        assert len(str(context.exception)) > 0

    def test_check_exact_len(self):
        valid_string = "1" * 5
        check_exact_length(valid_string, 5)
        assert True

    def test_check_invalid_exact_len(self):
        valid_string = "1"
        with self.assertRaises(ArgumentException) as context:
            check_exact_length(valid_string, 0)
        assert len(str(context.exception)) > 0

if __name__ == "__main__":
    unittest.main()
