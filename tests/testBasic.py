from exceptions import InvalidOperation
from tests.utils import PymboTest


# noinspection PyPep8Naming
class TestBasics(PymboTest):
    def test_basic(self):
        TEST_CODE = """
        def main():
            return True
        """
        self.translate(TEST_CODE)

    def test_addition(self):
        TEST_CODE = """
        def main():
            return 1+0
        """
        self.translate(TEST_CODE)

    def test_ternary(self):
        TEST_CODE = """
        def main():
            return 1 if 3>2 else 4
        """
        self.translate(TEST_CODE)

    def test_if(self):
        TEST_CODE = """
        def main():
            if True:
                return 1
            if False:
                return 2
            else:
                return 3
        """
        self.translate(TEST_CODE)

    def test_nested_if(self):
        TEST_CODE = """
        def main():
            if True:
                if False:
                    return 2
                else:
                    return 1
            return 4
        """
        self.translate(TEST_CODE)

    def test_assignment(self):
        TEST_CODE = """
        def main():
            a = 1
            return 1
        """
        self.translate(TEST_CODE)

    def test_repeat_safe_assignment(self):
        TEST_CODE = """
        def main():
            a = 1
            a = 2
            return 1
        """
        self.translate(TEST_CODE)

    def test_cant_subscript_an_int(self):
        TEST_CODE = """
        def main():
            a = 1
            return a[0]
        """
        self.check_raises(TEST_CODE, InvalidOperation)

    def test_cant_subscript_assign_an_int(self):
        TEST_CODE = """
        def main():
            a = 1
            a[0] = 2
            return 1
        """
        self.check_raises(TEST_CODE, InvalidOperation)

    def test_cant_get_int_attr(self):
        TEST_CODE = """
        def main():
            a = 1
            b = a.b
            return 1
        """
        self.check_raises(TEST_CODE, InvalidOperation)
