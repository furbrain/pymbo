import typed_ast.ast3 as ast
import functions
from typing import Dict


class Parser(ast.NodeVisitor):
    def __init__(self, funcs):
        self.funcs: functions.FuncDB = funcs
        self.code = ""


    def start_line(self, text: str) -> None:
        self.code += " " * self.indent
        self.code += text

    def visit_Module(self, node: ast.Module) -> None:
        print("Module found")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        print("Function found")
        if node.name == "main":
            self.code += self.funcs.get_implementation("main","")



def convert(code: str) -> str:
    tree = ast.parse(code)
    print(ast.dump(tree))
    funcs = functions.FuncDB()
    funcs.parse(tree)
    p = Parser(funcs = funcs)
    p.visit(tree)
    return p.code
