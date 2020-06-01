from tests.utils import PymboTest
import unittest

class TestLists(PymboTest):
    def test_basic(self):
        TEST_CODE = """
        def main():
            a = [1,2,3,4]
            return a[2]
        """
        self.translate(TEST_CODE)



if __name__ == '__main__':
    unittest.main()
