from typing import TYPE_CHECKING

import typed_ast.ast3 as ast

from context import Context
from exceptions import InvalidOperation, UnhandledNode
from itypes.classes import ClassType, ClassInstance
from itypes.functions import MultiFunction
from parser.expressions import get_constant_code

if TYPE_CHECKING:
    from parser import ModuleParser


# noinspection PyPep8Naming
class ClassParser(ast.NodeVisitor):
    def __init__(self, node: ast.ClassDef, module: "ModuleParser"):
        self.main_node = node
        self.cls = ClassType(node.name)
        self.instance = ClassInstance(self.cls)
        self.module = module
        self.context = Context(module.context)
        if node.bases:
            raise InvalidOperation("Inheritance not allowed")
        if node.keywords:
            raise InvalidOperation("Keywords not allowed in class statement")
        for n in node.body:
            self.visit(n)
        if "__init__" not in self.cls.methods:
            func_node = ast.parse("def __init__(self):\n  pass")
            self.visit(func_node.body[0])

    def get_type(self):
        return self.cls

    def visit_Pass(self, node):
        return

    def visit_Assign(self, node: ast.Assign):
        right = get_constant_code(node.value, self.module.context)
        for t in node.targets:
            if isinstance(t, ast.Name):
                self.cls.set_attr(t.id, right)
            else:
                raise InvalidOperation("Class variables must be simple names")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        tp = MultiFunction(node, self.context, name=f"{self.cls.name}__{node.name}")
        self.cls.add_method(node.name, tp)

    def generic_visit(self, node):
        raise UnhandledNode(node)
