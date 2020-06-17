from exceptions import InvalidOperation
from tests.utils import PymboTest


class TestListComp(PymboTest):
    def test_basic(self):
        code = """
        def main():
            a = [1,2,3,4]
            b = [x*x for x in a]
            return b[2]==9
            """
        self.translate(code)

    def test_conditional(self):
        code = """
        def main():
            a = [1,2,3,4]
            b = [x for x in a if x % 2 ==0]
            return b[1]==4
            """
        self.translate(code)

    def test_multiple_comprehension_fails(self):
        code = """
        def main():
            a = [1,2,3,4]
            b = [x*y for x in a for y in a]
            return b[2]==9
            """
        self.check_raises(code, InvalidOperation)

    def test_multiple_if_fails(self):
        code = """
        def main():
            a = [1,2,3,4]
            b = [x for x in a if x < 2 if x > 0]
            return b[2]==9
            """
        self.check_raises(code, InvalidOperation)
