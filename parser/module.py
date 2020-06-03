import typed_ast.ast3 as ast
from typed_ast import ast3 as ast

from context import Context
from exceptions import UnhandledNode
from funcdb import FuncDB
from itypes.typedb import TypeDB


class ModuleParser(ast.NodeVisitor):
    def __init__(self):
        self.funcs = FuncDB(self)
        self.context = Context()
        self.types = TypeDB()

    def create_code(self, include_type_funcs=False):
        self.funcs.get_implementation("main", ())
        code = ""
        if include_type_funcs:
            print("TYPES:", self.types.types )
            for t in self.types:
                code += t.get_type_def()
                code += t.get_definitions()
                code += t.get_implementations()
        code += "\n".join(self.funcs.get_all_definitions())
        code += "\n"
        code += "\n\n".join(self.funcs.get_all_implementations())
        return code

    def visit_FunctionDef(self, node: ast.FunctionDef):
        #ignore any inner function defs - not supported...
        self.funcs.add_function(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        #ignore any defs within classes
        pass