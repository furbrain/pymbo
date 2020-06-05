from tests.utils import PymboTest
import unittest

class TestLists(PymboTest):
    def test_basic(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
        """
        self.translate(TEST_CODE)

    def test_get(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            return a[2]
        """
        self.translate(TEST_CODE)

    def test_assign(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            a[3] = 5
            return a[3]
        """
        self.translate(TEST_CODE)

    def test_append(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            a.append(5)
            return a[4]
        """
        self.translate(TEST_CODE)

    def test_subscript_errors_with_wrong_type(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            b = a["b"]
            return b
        """
        self.check_raises(TEST_CODE, ValueError)

    def test_subscript_assign_errors_with_wrong_index(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            a["b"] = 5
        """
        self.check_raises(TEST_CODE, ValueError)

    def test_subscript_assign_errors_with_wrong_value(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            a[2] = "a"
        """
        self.check_raises(TEST_CODE, ValueError)

if __name__ == '__main__':
    unittest.main()
