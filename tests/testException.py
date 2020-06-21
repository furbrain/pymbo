import unittest

from exceptions import InvalidOperation
from tests.utils import PymboTest


class TestException(PymboTest):
    def test_basic_exception(self):
        code = """
        def main():
            result = False
            try:
                raise ValueError
            except ValueError:
                result = True
            return result
            """
        self.translate(code)

    def test_cant_return_from_within_try(self):
        code = """
        def main():
            try:
                return False
            except:
                pass
            return True
            """
        self.check_raises(code, InvalidOperation)

    @unittest.skip
    def test_raise_with_message(self):
        code = """
        def main():
            try:
                raise ValueError("Error Message")
            except ValueError as e:
                return e.args[0] == "Error Message"
            """
        self.translate(code)
