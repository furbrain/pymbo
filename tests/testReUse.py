import unittest
import pymbo
import functions
import typed_ast.ast3 as ast

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
        a = f.get_func_name("adder", "int,int")
        b = f.get_func_name("adder", "str,str")
        print(f.get_definition("adder","int,int"))
        print(f.get_definition("adder","str,str"))

    def test_conversion(self):
        print(pymbo.convert(TEST_CODE))

if __name__ == '__main__':
    unittest.main()
