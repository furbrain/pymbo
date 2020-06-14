from tests.utils import PymboTest


class TestFor(PymboTest):
    def test_simple(self):
        code = """
        def main():
            a = [1,3,5]
            b = 0
            for x in a:
                b  = b + x
            return b==9
            """
        self.translate(code)

    def test_nested(self):
        code = """
        def main():
            a = [[1,3,5], [2,4,6,8], [3,7]]
            b = 0
            for x in a:
                b = b + x[1]
            return b==14
            """
        self.translate(code)
