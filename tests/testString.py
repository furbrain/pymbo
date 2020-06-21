from tests.utils import PymboTest


class TestString(PymboTest):
    def test_assign(self):
        code = """
        def main():
            a = "abc"
            return True
        """
        self.translate(code)

    def test_equate(self):
        code = """
        def main():
            a = "abc"
            return a == "abc"
        """
        self.translate(code)

    def test_pass_as_arg(self):
        code = """
        def f(s):
            if s == "abc":
                return True
            else:
                return False
        
        def main():
            a = "abc"
            return f(a)
        """
        self.translate(code)

    def test_pass_as_literal(self):
        code = """
        def f(s):
            if s == "abc":
                return True
            else:
                return False

        def main():
            return f("abc")
        """
        self.translate(code)
