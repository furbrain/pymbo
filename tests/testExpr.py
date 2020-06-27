import pymbo
from exceptions import UnimplementedFeature, StaticTypeError
from parser import get_expression_code
from parser.module import ModuleParser
from tests.utils import PymboTest

BASIC_TESTS = {
    "'a'": ("str:40", '(str__40){"a"}'),
    '"a"': ("str:40", '(str__40){"a"}'),
    'b"a"': ("str:40", '(str__40){"a"}'),
    "1": ("int", "1"),
    "2.3": ("float", "2.3"),
    "5.0": ("float", "5.0"),
    "True": ("bool", "true"),
    "False": ("bool", "false")
}

SIMPLE_OPS = {
    "1+2": ("int", '(1 + 2)'),
    "1+2.0": ("float", '(1 + 2.0)'),
    "1.0+2": ("float", '(1.0 + 2)'),
    "1 * 2": ("int", '(1 * 2)'),
    "4 / 2": ("float", '((float) 4 / 2)'),
    "5 - 3": ("int", '(5 - 3)'),
    "7 % 3": ("int", '(7 % 3)'),
    "3 << 2": ("int", '(3 << 2)'),
    "7 >> 2": ("int", '(7 >> 2)'),
}

IF_EXPR = {
    "3 if True else 5": ("int", "true ? 3 : 5"),
    "'fred' if False else 'george'": ("str:40", 'false ? (str__40){"fred"} : (str__40){"george"}'),
    "2.3 if 3 < 10 else 5.7": ("float", '(3 < 10) ? 2.3 : 5.7')
}

COMP_TESTS = {
    "1 < 2": ("bool", "(1 < 2)"),
    "2 == 3": ("bool", "(2 == 3)"),
    "1 <= 2": ("bool", "(1 <= 2)"),
    "2 != 3": ("bool", "(2 != 3)"),
    "1 > 2": ("bool", "(1 > 2)"),
    "2 >= 3": ("bool", "(2 >= 3)"),
}

COMP_NOT_IMPLEMENTED = (
    "'a' in 'abc'",
    "'f' not in 'fred'",
    "1 is not 7",
    "2 is True",
    "2 < 5 < 7"
)

COMP_TYPE_ERRORS = (
    '"a" < 2',
    '2 + "a"',
    '"a" + 2',
    '"a" if 3>2 else 2'
)


class TestExpressions(PymboTest):
    def run_passing_tests(self, params):
        for code, expected in params.items():
            with self.subTest(code=code):
                m = ModuleParser()
                results, _ = get_expression_code(code, m.context)
                self.assertEqual(expected[0], results.tp)
                self.assertEqual(expected[1], results.code)

    def compile_and_check_expressions(self, params):
        for code, expected in params.items():
            # FIXME - should work with all reasonable python expressions...
            if expected[0] != "str:40":
                with self.subTest(code=code):
                    m = ModuleParser()
                    results, _ = get_expression_code(code, m.context)
                    expected_result = str(eval(code)).lower()
                    test_code = f"{pymbo.INCLUDES}\nint main(){{\n    return {results.code}=={expected_result};}}"
                    self.compile_and_run(test_code)

    def run_failing_tests(self, params, expected_exception):
        for code in params:
            with self.assertRaises(expected_exception):
                m = ModuleParser()
                get_expression_code(code, m.context)

    def test_basics(self):
        self.run_passing_tests(BASIC_TESTS)
        self.compile_and_check_expressions(BASIC_TESTS)

    def test_binops(self):
        self.run_passing_tests(SIMPLE_OPS)
        self.compile_and_check_expressions(BASIC_TESTS)

    def test_if_expr(self):
        self.run_passing_tests(IF_EXPR)
        self.compile_and_check_expressions(BASIC_TESTS)

    def test_comp(self):
        self.run_passing_tests(COMP_TESTS)
        self.compile_and_check_expressions(BASIC_TESTS)

    def test_comp_fails(self):
        self.run_failing_tests(COMP_NOT_IMPLEMENTED, (StaticTypeError, UnimplementedFeature))

    def test_comp_type_errors(self):
        self.run_failing_tests(COMP_TYPE_ERRORS, StaticTypeError)

