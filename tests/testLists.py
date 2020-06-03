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



if __name__ == '__main__':
    unittest.main()
