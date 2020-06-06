import unittest

from exceptions import UnhandledNode, TranslationError
from tests.utils import PymboTest


class TestNotImplemented(PymboTest):
    def test_eval(self):
        code = """
        def main():
            eval("1+2")
        """
        self.check_raises(code, TranslationError)

    @unittest.skip  # pragma: no cover
    def test_no_inheritance(self):
        code = """
        class A(list):
            pass
        """
        self.check_raises(code, TranslationError)

    def test_yield_not_valid(self):
        code = """
        def main():
            yield 1
        """
        self.check_raises(code, UnhandledNode)
