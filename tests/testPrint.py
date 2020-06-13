from tests.utils import PymboTest


class TestPrint(PymboTest):
    def test_basic_c_output_received(self):
        c_code = """
        #include <stdio.h>
        int main() {
            printf("34\\n");
        }
        """
        self.assertEqual("34\n", self.compile_and_run(c_code, check_result=False))

    def test_no_args(self):
        code = """
        def main():
            print()
        """
        self.assertEqual("\n", self.translate(code, check_result=False))

    def test_literal_arg(self):
        code = """
        def main():
            print(2)
        """
        self.assertEqual("2\n", self.translate(code, check_result=False))

    def test_variable_arg(self):
        code = """
        def main():
            a = 3
            print(a)
        """
        self.assertEqual("3\n", self.translate(code, check_result=False))

    def test_multiple_args(self):
        code = """
        def main():
            a = 3
            b = 5
            print(a, b)
        """
        self.assertEqual("3 5\n", self.translate(code, check_result=False))

    def test_str_arg(self):
        code = """
        def main():
            print("fred")
        """
        self.assertEqual("fred\n", self.translate(code, check_result=False))

    def test_str_var(self):
        code = """
        def main():
            a="george"
            print(a)
        """
        self.assertEqual("george\n", self.translate(code, check_result=False))

    def test_float_arg(self):
        code = """
        def main():
            print(3.2)
        """
        self.assertEqual("3.200000\n", self.translate(code, check_result=False))

    def test_float_var(self):
        code = """
        def main():
            a=3.45
            print(a)
        """
        self.assertEqual("3.450000\n", self.translate(code, check_result=False))
