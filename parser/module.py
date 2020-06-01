import typed_ast.ast3 as ast
from typed_ast import ast3 as ast

import context
from exceptions import UnhandledNode


class ModuleParser(ast.NodeVisitor):
    def __init__(self, funcs):
        self.funcs: context.Context = funcs
        self.code = ""

    def visit_FunctionDef(self, node: ast.FunctionDef):
        #ignore any inner function defs - not supported...
        self.funcs.add_function(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        #ignore any defs within classes
        pass