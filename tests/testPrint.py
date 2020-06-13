from tests.utils import PymboTest


class TestPrint(PymboTest):
    def test_basic_c_output_received(self):
        c_code = """
        #include <stdio.h>
        int main() {
            printf("34\\n");
            return 1;
        }
        """
        self.assertEqual("34\n", self.compile_and_run(c_code))

    def test_no_args(self):
        code = """
        def main():
            print()
            return True
        """
        self.assertEqual("\n", self.translate(code))

    def test_literal_arg(self):
        code = """
        def main():
            print(2)
            return True
        """
        self.assertEqual("2\n", self.translate(code))

    def test_variable_arg(self):
        code = """
        def main():
            a = 3
            print(a)
            return True
        """
        self.assertEqual("3\n", self.translate(code))

    def test_multiple_args(self):
        code = """
        def main():
            a = 3
            b = 5
            print(a, b)
            return True
        """
        self.assertEqual("3 5\n", self.translate(code))

    def test_str_arg(self):
        code = """
        def main():
            print("fred")
            return True
        """
        self.assertEqual("fred\n", self.translate(code))

    def test_str_var(self):
        code = """
        def main():
            a="george"
            print(a)
            return True
        """
        self.assertEqual("george\n", self.translate(code))
