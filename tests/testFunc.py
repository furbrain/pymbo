from exceptions import InvalidOperation
from tests.utils import PymboTest


class TestFuncs(PymboTest):
    def testSimpleFunc(self):
        code = """
        def f():
            return True
        
        def main():
            return f()
        """
        self.translate(code)

    def testMultiFunc(self):
        code = """
        def f(a, b):
            return True

        def main():
            f(1,2)
            f("a","b")
            return True
        """
        self.translate(code)

    def test_error_with_vararg(self):
        code = """
        def f(*args):
            return True

        def main():
            return True
        """
        self.check_raises(code, InvalidOperation)
