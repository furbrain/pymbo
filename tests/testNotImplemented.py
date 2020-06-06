from exceptions import UnhandledNode, TranslationError
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
        self.check_raises(TEST_CODE, TranslationError)


    @unittest.skip # pragma: no cover
    def test_no_inheritance(self):
        TEST_CODE = """
        class A(list):
            pass
        """
        self.check_raises(TEST_CODE, TranslationError)

    def test_yield_not_valid(self):
        TEST_CODE = """
        def main():
            yield 1
        """
        self.check_raises(TEST_CODE, UnhandledNode)
