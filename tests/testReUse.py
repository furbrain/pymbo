import typed_ast.ast3 as ast

from itypes import TypeDB
from parser.module import ModuleParser
from tests.utils import PymboTest

TEST_CODE = """
def adder(a,b):
    return a + b

def main():
    adder(1,2)
    adder(2.3, 4.5)
    return 1
"""


class TestReUse(PymboTest):
    def test_something(self):
        tree = ast.parse(TEST_CODE)
        m = ModuleParser()
        m.visit(tree)
        TypeDB.get_type_by_name("int")
        TypeDB.get_type_by_name("float")
        TypeDB.get_string()

    def test_conversion(self):
        self.translate(TEST_CODE)
