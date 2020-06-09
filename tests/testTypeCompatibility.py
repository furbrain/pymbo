from tests.utils import PymboTest


class TestTypeCompatibility(PymboTest):
    def test_compatible_assignment(self):
        code = """
            def main():
                a=1
                a=1.1
                return 1
        """
        self.translate(code)

    def test_reverse_compatible_assignment(self):
        code = """
            def main():
                a=1.1
                a=1
                return 1
        """
        self.translate(code)

    def test_mixed_returns(self):
        code = """
            def g():
                if True:
                    return 1
                else:
                    return 1.1
            
            def main():
                g()
                return True    
        """
        self.translate(code)
