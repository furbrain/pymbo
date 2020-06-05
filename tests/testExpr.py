import unittest
import typed_ast.ast3 as ast

from exceptions import UnimplementedFeature
from parser.expressions import ExpressionParser
from funcdb import FuncDB
from parser.module import ModuleParser
from scopes import Scope

BASIC_TESTS = {
    "'a'": ("<str>", '"a"'),
    '"a"': ("<str>", '"a"'),
    "1":   ("<int>", "1"),
    "2.3": ("<float>", "2.3"),
    "5.0": ("<float>", "5.0"),
    "True": ("<bool>", "true"),
    "False": ("<bool>", "false")
}

SIMPLE_OPS = {
    "1+2": ("<int>", '(1 + 2)'),
    "1+2.0": ("<float>", '(1 + 2.0)'),
    "1 * 2": ("<int>", '(1 * 2)'),
    "4 / 2": ("<int>", '(4 / 2)'),
    "5 - 3": ("<int>", '(5 - 3)')
}

IF_EXPR = {
    "3 if True else 5": ("<int>", "true ? 3 : 5"),
    "'fred' if False else 'george'": ("<str>", 'false ? "fred" : "george"'),
    "2.3 if 3 < 10 else 5.7": ("<float>", '(3 < 10) ? 2.3 : 5.7')
}

COMP_TESTS = {
    "1 < 2": ("<bool>", "(1 < 2)"),
    "2 == 3": ("<bool>", "(2 == 3)"),
    "1 <= 2": ("<bool>", "(1 <= 2)"),
    "2 != 3": ("<bool>", "(2 != 3)"),
    "1 > 2": ("<bool>", "(1 > 2)"),
    "2 >= 3": ("<bool>", "(2 >= 3)"),
}

COMP_NOT_IMPLEMENTED = (
    "'a' in 'abc'",
    "'f' not in 'fred'",
    "x is not 7",
    "y is True",
    "2 < 5 < 7"
)

class TestExpressions(unittest.TestCase):
    def run_passing_tests(self, params):
        for code, expected in params.items():
            with self.subTest(code=code):
                m = ModuleParser()
                p = ExpressionParser(m, None)
                tree = ast.parse(code)
                results = p.visit(tree)
                self.assertEqual(expected[0], results.tp)
                self.assertEqual(expected[1], results.code)

    def run_not_implemented_tests(self, params):
        for code in params:
            with self.assertRaises(UnimplementedFeature):
                m = ModuleParser()
                p = ExpressionParser(m, None)
                tree = ast.parse(code)
                p.visit(tree)

    def test_basics(self):
        self.run_passing_tests(BASIC_TESTS)

    def test_binops(self):
        self.run_passing_tests(SIMPLE_OPS)

    def test_if_expr(self):
        self.run_passing_tests(IF_EXPR)

    def test_comp(self):
        self.run_passing_tests(COMP_TESTS)

    def test_comp_fails(self):
        self.run_not_implemented_tests(COMP_NOT_IMPLEMENTED)

if __name__ == '__main__':
    unittest.main()
