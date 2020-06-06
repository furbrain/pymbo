from typing import TYPE_CHECKING

import typed_ast.ast3 as ast

from context import Context, Code
from exceptions import UnhandledNode, UnimplementedFeature, StaticTypeError
from itypes import TypeDB, InferredType
from parser import get_expression_code

if TYPE_CHECKING:  # pragma: no cover
    from funcdb import TypeSig
    from parser.module import ModuleParser


# noinspection PyPep8Naming
class FunctionImplementation(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef, type_sig: "TypeSig", module: "ModuleParser"):
        self.module = module
        self.body = ""
        self.retval = None
        self.all_paths_return = False
        self.context = Context(module.context)
        self.funcs = module.funcs
        self.args = []
        for arg, arg_type in zip(node.args.args, type_sig):
            self.context[arg.arg] = Code(arg_type, is_arg=True, code=arg.arg)
            self.args += [arg_type.as_c_type() + " " + arg.arg]
        self.indent = 2
        self.type_sig = type_sig
        self.primary_node = node
        self.generate_code()

    def generate_code(self):
        self.body = ""
        self.indent = 2
        self.retval = None
        self.all_paths_return = False
        for n in self.primary_node.body:
            self.visit(n)
        if not self.all_paths_return:
            self.set_return_type(TypeDB.get_type_by_value(None))

    def start_line(self, text: str) -> None:
        self.body += " " * self.indent
        self.body += text

    def visit_If(self, node: ast.If) -> None:
        test = self.get_code(node.test)
        self.start_line("if ({}) {{\n".format(test.code))
        self.indent += 2
        for n in node.body:
            self.visit(n)
        body_returns = self.all_paths_return
        self.all_paths_return = False
        if node.orelse:
            self.indent -= 2
            self.start_line("} else {\n")
            self.indent += 2
            for n in node.orelse:
                self.visit(n)
            self.all_paths_return = body_returns and self.all_paths_return

        self.indent -= 2
        self.start_line("}\n")

    def visit_Return(self, node: ast.Return) -> None:
        result = self.get_code(node.value)
        self.set_return_type(result.tp)
        self.start_line("return " + result.code + ";\n")
        self.all_paths_return = True

    def set_return_type(self, tp: InferredType):
        if self.retval is None:
            self.retval = tp
        elif self.retval != tp:
            raise StaticTypeError(f"Function returns both {self.retval} and {tp}")

    def visit_Expr(self, node: ast.Expr) -> None:
        result = self.get_code(node.value)
        self.start_line(result.code + ";\n")

    def visit_Assign(self, node: ast.Assign) -> None:
        right = self.get_code(node.value)
        for n in node.targets:
            if isinstance(n, ast.Name):
                left = self.context.setdefault(n.id, Code(tp=right.tp, code=n.id))
                if left.tp != right.tp:
                    raise StaticTypeError(f"Assigning {right.tp} to {left.tp}")
                self.start_line("{} = {};\n".format(left.code, right.as_value().code))
            elif isinstance(n, ast.Subscript):
                value = self.get_code(n.value)
                slice_type = type(n.slice).__name__
                if slice_type == "Index":
                    index = self.get_code(n.slice.value)
                    res_code = value.tp.set_item(index.tp, right.tp)
                    self.start_line(f"{res_code}({value.as_pointer().code}, {index.code}, {right.code});\n")
                else:
                    raise UnimplementedFeature("Slices not yet implemented")

    def get_code(self, node: ast.AST) -> Code:
        return get_expression_code(node, self.module, self.context)

    def generic_visit(self, node):
        raise UnhandledNode(node)

    def get_variable_definitions(self):
        text = ""
        for name, var in self.context.locals():
            text += f"  {var.tp.as_c_type()} {name};\n"
        return text
