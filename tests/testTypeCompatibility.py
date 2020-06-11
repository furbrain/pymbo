from itypes import TypeDB
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


class TestTypeEquivalence(PymboTest):
    def test_ints(self):
        a = TypeDB.get_type_by_value(1)
        b = TypeDB.get_type_by_value(int)
        c = TypeDB.get_type_by_name("int")
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(a, a)
        self.assertEqual(a, int)

    def test_int_equality_fails_with_bad_comparator(self):
        a = TypeDB.get_type_by_value(1)
        self.assertFalse((a == self))
