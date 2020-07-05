import lib.typing as typing
from exceptions import StaticTypeError
from tests.utils import PymboTest


# noinspection PyUnusedLocal
class TestTypingInPython(PymboTest):
    def test_simple_annotation(self):
        a: typing.UInt8 = 3

    def test_list_annotation(self):
        a: typing.List[int:10] = [1, 2, 3, 4]


class TestTypingInPymbo(PymboTest):
    def test_simple_annotation(self):
        code = """
        def main():
            a: Int8 = 127
            return True
        """
        self.translate(code)

    def test_integer_overflow(self):
        code = """
        def main():
            a: Int8 = 127
            a = a + 1
            return a < 0
        """
        self.translate(code)

    def test_integer_overflow_unsigned(self):
        code = """
        def main():
            a: UInt8 = 255
            a = a + 1
            return a == 0
        """
        self.translate(code)

    def test_integer_to_float_fails(self):
        code = """
        def main():
            a: Int8 = 127
            a = 1.0
            return True
        """
        self.check_raises(code, StaticTypeError)

    def test_integer_promotion(self):
        code = """
        def main():
            a: Int8 = 100
            b: Int16 = 127
            a = b
            a = a +1
            return a < 0
        """
        self.translate(code)

    def test_list_typing(self):
        code = """
        def main():
            a: List[int:20] = []
            a.append(2)
            return a[0]==2
        """
        self.translate(code)

    def test_list_typing_no_maxlen(self):
        code = """
        def main():
            a: List[int] = []
            a.append(2)
            return a[0]==2
        """
        self.translate(code)

    def test_list_empty_without_annotation_raises_error(self):
        code = """
        def main():
            a = []
            a.append(2)
            return a[0]==2
        """
        self.check_raises(code, StaticTypeError)

    def test_list_empty_with_prior_annotation(self):
        code = """
        def main():
            a: List[int:20]
            a = []
            a.append(2)
            return a[0]==2
        """
        self.translate(code, StaticTypeError)
