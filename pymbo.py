import typed_ast.ast3 as ast

import context
import functions
from typing import Dict


class Parser(ast.NodeVisitor):
    def __init__(self, funcs):
        self.funcs: context.Context = funcs
        self.code = ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "main":
            self.funcs.get_implementation("main",())



def convert(code: str) -> str:
    tree = ast.parse(code)
    funcs = context.Context()
    try:
        funcs.parse(tree)
        p = Parser(funcs = funcs)
        p.visit(tree)
        code = "\n".join(funcs.get_all_definitions())
        code += "\n"
        code += "\n\n".join(funcs.get_all_implementations())
    except ZeroDivisionError:
        pass
    return code
