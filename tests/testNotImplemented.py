from tests.utils import PymboTest
import unittest

import exceptions

import tests.utils


class TestNotImplemented(PymboTest):
    def test_eval(self):
        TEST_CODE = """
        def main():
            eval("1+2")
        """
        with self.assertRaises(exceptions.TranslationError):
            self.translate(TEST_CODE)


    @unittest.skip
    def test_no_inheritance(self):
        TEST_CODE = """
        class A(list):
            pass
        """
        with self.assertRaises(exceptions.TranslationError):
            self.translate(TEST_CODE)

if __name__ == '__main__':
    unittest.main()
