from exceptions import StaticTypeError
from tests.utils import PymboTest


class TestLists(PymboTest):
    def test_basic(self):
        code = """
        def main():
            a = [1,2,3,4]
            return True
        """
        self.translate(code)

    def test_nested(self):
        code = """
        def main():
            a = [[1,2],[3,4],[5]]
            return True
        """
        self.translate(code)

    def test_type_combining(self):
        code = """
        def main():
            a = [1,2.0,3,4.0]
            return True
        """
        self.translate(code)

    def test_get(self):
        code = """
        def main():
            a = [1,2,1,4]
            return a[2]
        """
        self.translate(code)

    def test_get_nested(self):
        code = """
        def main():
            a = [[1,2],[1,4]]
            b = a[1]
            return b[1]==4
        """
        self.translate(code)

    def test_chained_subscript(self):
        code = """
        def main():
            a = [[[1,2],[1,4]]]
            return a[0][1][1]==4
        """
        self.translate(code)

    def test_assign(self):
        code = """
        def main():
            a = [1,2,3,4]
            a[3] = 1
            return a[3]
        """
        self.translate(code)

    def test_append(self):
        code = """
        def main():
            a = [1,2,3,4]
            a.append(1)
            return a[4]
        """
        self.translate(code)

    def test_subscript_errors_with_wrong_type(self):
        code = """
        def main():
            a = [1,2,3,4]
            b = a["b"]
            return b
        """
        self.check_raises(code, StaticTypeError)

    def test_subscript_assign_errors_with_wrong_index(self):
        code = """
        def main():
            a = [1,2,3,4]
            a["b"] = 5
        """
        self.check_raises(code, StaticTypeError)

    def test_subscript_assign_errors_with_wrong_value(self):
        code = """
        def main():
            a = [1,2,3,4]
            a[2] = "a"
        """
        self.check_raises(code, StaticTypeError)

    def test_raises_error_with_incompatible_elements(self):
        code = """
        def main():
            a = [2.0, "a"]
        """
        self.check_raises(code, StaticTypeError)

    def test_len_works(self):
        code = """
        def main():
            a = [1,2,3,4]
            b= a.len()
            return b - 3
        """
        self.translate(code)

    def test_function_with_list_arg_and_return_works(self):
        code = """
        def op(lst):
            a = [lst[1]]
            return a
            
        def main():
            b = [1,2,3,4]
            b = op(b)
            return b[0]==2
        """
        self.translate(code)
