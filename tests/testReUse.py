import unittest

import funcdb
import typed_ast.ast3 as ast
from itypes import get_type_by_name
from parser.module import ModuleParser
from tests.utils import PymboTest

TEST_CODE = """
def adder(a,b):
    return a + b
    
def main():
    adder(1,2)
    adder("fred", "george")
    return 1 + 2
"""

class TestReUse(PymboTest):
    def test_something(self):
        tree = ast.parse(TEST_CODE)
        m  = ModuleParser()
        m.visit(tree)
        f = m.funcs
        i = get_type_by_name("<int>")
        g = get_type_by_name("<float>")
        s = get_type_by_name("<str>")
        a = f.get_func_name("adder", (i, i))
        b = f.get_func_name("adder", (s, s))
        b = f.get_func_name("adder", (g, g))

    def test_conversion(self):
        self.translate(TEST_CODE)

if __name__ == '__main__':
    unittest.main()
