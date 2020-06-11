from exceptions import StaticTypeError, InvalidOperation, UnhandledNode
from tests.utils import PymboTest


class TestModule(PymboTest):
    def test_module_level_int_var(self):
        code = """
        a = 3
        def main():
            return a==3
        """
        self.translate(code)

    def test_module_level_int_literal_calculation(self):
        code = """
        a = 3 + 2
        def main():
            return a==5
        """
        self.translate(code)

    def test_module_level_int_complicated_literal_calculation(self):
        code = """
        a = 3 + (10 / 5)
        def main():
            return a==5
        """
        self.translate(code)

    def test_module_level_list_var(self):
        code = """
        a = [1,2,3,4]
        def main():
            return a[1]==2
        """
        self.translate(code)

    def test_module_level_int_reuse_fails(self):
        code = """
        a = 3
        a = 4
        def main():
            return a==3
        """
        self.check_raises(code, StaticTypeError)

    def test_module_level_var_read_fails(self):
        code = """
        a = 3
        b = a + 2
        def main():
            return a==3
        """
        self.check_raises(code, StaticTypeError)

    def test_module_level_bad_opargs(self):
        code = """
        a = 3 + "a"
        def main():
            return a==3
        """
        self.check_raises(code, StaticTypeError)

    def test_module_level_bad_lval(self):
        code = """
        a.b = 3
        def main():
            return a==3
        """
        self.check_raises(code, InvalidOperation)

    def test_module_level_bad_node(self):
        code = """
        async def main():
            return a==3
        """
        self.check_raises(code, UnhandledNode)
