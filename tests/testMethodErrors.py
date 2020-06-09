from exceptions import StaticTypeError
from tests.utils import PymboTest


class TestMethodErrors(PymboTest):
    def test_append_works(self):
        code = """
        def main():
            a = [4]
            a.append(1)
            return a[1]
        """
        self.translate(code)

    def test_error_with_not_enough_args(self):
        code = """
        def main():
            a = [1]
            a.append()
            return a[1]
        """
        self.check_raises(code, StaticTypeError)

    def test_error_with_too_many_args(self):
        code = """
        def main():
            a = [1]
            a.append(1,2)
            return a[1]
        """
        self.check_raises(code, StaticTypeError)

    def test_error_with_wrong_args(self):
        code = """
        def main():
            a = [1]
            a.append("a")
            return a[1]
        """
        self.check_raises(code, StaticTypeError)
