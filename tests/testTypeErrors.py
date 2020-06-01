from tests.utils import PymboTest
import unittest

from exceptions import TranslationError

class TestTypeErrors(PymboTest):
    @unittest.skip
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
        with self.assertRaises(TranslationError):
            self.translate(TEST_CODE)

    @unittest.skip
    def test_different_assignment_types(self):
        TEST_CODE = """
        def test(a):
            b=1
            b="one"

        def main():
            test(1)
        """
        with self.assertRaises(TranslationError):
            self.translate(TEST_CODE)


if __name__ == '__main__':
    unittest.main()
