from tests.utils import PymboTest


class TestBasics(PymboTest):
    def test_basic(self):
        TEST_CODE = """
        def main():
            return 0
        """
        self.translate(TEST_CODE)

    def test_addition(self):
        TEST_CODE = """
        def main():
            return 1+2
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
                    return 3
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

if __name__ == '__main__':
    unittest.main()
