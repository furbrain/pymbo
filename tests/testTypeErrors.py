from tests.utils import PymboTest
import unittest

from exceptions import TranslationError, UnhandledNode


class TestTypeErrors(PymboTest):
    @unittest.skip # pragma: no cover
    def test_different_return_types(self):
        TEST_CODE = """
        def test(a):
            if a==1:
                return 1
            else:
                return "not one"
        
        def main():
            test(1)
        """
        self.check_raises(TEST_CODE, TranslationError)

    def test_different_assignment_types(self):
        code = """
        def test(a):
            b=1
            b="one"

        def main():
            test(1)
        """
        self.check_raises(code, StaticTypeError)

    def test_unknown_variable(self):
        TEST_CODE = """
        def main():
            b = 1
            b = a
        """
        self.check_raises(TEST_CODE, TranslationError)

    def test_delete_not_valid(self):
        TEST_CODE = """
        def main():
            b = 1
            del b
        """
        self.check_raises(TEST_CODE, UnhandledNode)
