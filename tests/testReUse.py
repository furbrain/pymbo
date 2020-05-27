import unittest
import pymbo
import functions
import typed_ast.ast3 as ast
from itypes import get_type_by_name

TEST_CODE = """
def adder(a,b):
    return a + b
    
def main():
    adder(1,2)
    adder("fred", "george")
    return 1 + 2
"""

class MyTestCase(unittest.TestCase):
    def test_something(self):
        tree = ast.parse(TEST_CODE)
        f = functions.FuncDB()
        f.parse(tree)
        i = get_type_by_name("<int>")
        g = get_type_by_name("<float>")
        s = get_type_by_name("<str>")
        a = f.get_func_name("adder", (i, i))
        b = f.get_func_name("adder", (s, s))
        b = f.get_func_name("adder", (g, g))

    def test_conversion(self):
        print(pymbo.convert(TEST_CODE))

if __name__ == '__main__':
    unittest.main()
