from exceptions import TranslationError, UnhandledNode, StaticTypeError
from itypes import TypeDB
from tests.utils import PymboTest


class TestTypeErrors(PymboTest):
    def test_different_return_types(self):
        code = """
        def test(a):
            if a==1:
                return 1
            return "not one"
        
        def main():
            test(1)
        """
        self.check_raises(code, StaticTypeError)

    def test_error_falling_from_end_function_that_returns_int(self):
        code = """
        def test(a):
            if a==1:
                return 1

        def main():
            test(1)
        """
        self.check_raises(code, StaticTypeError)

    def test_no_error_falling_from_function(self):
        code = """
        def test(a):
            if a==1:
                return 1
            else:
                return 2
                
        def main():
            test(1)
        """
        self.translate(code)

    def test_different_assignment_types(self):
        code = """
        def test(a):
            b=1
            b="one"

        def main():
            test(1)
        """
        self.check_raises(code, StaticTypeError)

    def test_unknown_variable(self):
        code = """
        def main():
            b = 1
            b = a
        """
        self.check_raises(code, TranslationError)

    def test_delete_not_valid(self):
        code = """
        def main():
            b = 1
            del b
        """
        self.check_raises(code, UnhandledNode)

    def test_create_weird_type_fails(self):
        with self.assertRaises(AttributeError):
            TypeDB.get_type_by_name("fred")
