from typing import TYPE_CHECKING, Set

import typed_ast.ast3 as ast

from context import Context, Code
from exceptions import UnhandledNode, UnimplementedFeature
from itypes import TypeDB
from parser import get_expression_code

if TYPE_CHECKING:  # pragma: no cover
    from funcdb import TypeSig
    from parser.module import ModuleParser


# noinspection PyPep8Naming
class FunctionImplementation(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef, type_sig: "TypeSig", module: "ModuleParser"):
        self.body: str
        self.indent: int
        self.retval: Code
        self.all_paths_return: bool
        self.primary_node = node
        self.module = module
        self.context = Context(module.context)
        self.funcs = module.funcs
        self.args = []
        self.libraries: Set[str] = set()
        for arg, arg_type in zip(node.args.args, type_sig):
            code = Code(arg_type, is_arg=True, is_pointer=not arg_type.pass_by_value, code=arg.arg)
            self.context[arg.arg] = code
            self.args.append(code)
        self.generate_code()

    # noinspection PyAttributeOutsideInit
    def generate_code(self):
        self.body = ""
        self.indent = 2
        self.retval = Code(tp=None, code="_retval", is_pointer=True)
        self.all_paths_return = False
        self.context.clear_temp_vars()
        for n in self.primary_node.body:
            self.visit(n)
        if not self.all_paths_return:
            self.retval.assign_type(TypeDB.get_type_by_value(None), " as return value")

    def retval_in_c(self):
        if self.retval.tp.pass_by_value:
            return self.retval.tp.c_type
        else:
            return "void"

    def params(self):
        if self.retval.tp.pass_by_value:
            return self.args
        else:
            return self.args + [self.retval]

    def start_line(self, text: str) -> None:
        self.body += " " * self.indent
        self.body += text

    # noinspection PyAttributeOutsideInit
    def visit_If(self, node: ast.If) -> None:
        test = self.get_expression_code(node.test)
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
        result = self.get_expression_code(node.value)
        self.retval.assign_type(result.tp, " as return value")
        if self.retval.tp.pass_by_value:
            self.start_line(f"return {result.code};\n")
        else:
            self.start_line(f"{self.retval.as_value()} = {result.code};\n")
            self.start_line("return;\n")
        # noinspection PyAttributeOutsideInit
        self.all_paths_return = True

    def visit_Expr(self, node: ast.Expr) -> None:
        result = self.get_expression_code(node.value)
        self.start_line(result.code + ";\n")

    def visit_Assign(self, node: ast.Assign) -> None:
        right = self.get_expression_code(node.value)
        for n in node.targets:
            if isinstance(n, ast.Name):
                left = self.context.setdefault(n.id, Code(tp=right.tp, code=n.id))
                if left.tp != right.tp:
                    left.assign_type(right.tp)
                self.start_line("{} = {};\n".format(left.code, right.as_value()))
            elif isinstance(n, ast.Subscript):
                value = self.get_expression_code(n.value)
                slice_type = type(n.slice).__name__
                if slice_type == "Index":
                    index = self.get_expression_code(n.slice.value)
                    setter = value.tp.get_method("set_item")
                    code = setter.get_code(self.context, value, index, right)
                    self.start_line(f"{code.code};\n")
                else:
                    raise UnimplementedFeature("Slices not yet implemented")

    def get_expression_code(self, node: ast.AST) -> Code:
        code = get_expression_code(node, self.module, self.context)
        for line in code.prepends:
            self.start_line(line)
        self.libraries.update(code.libraries)
        return code

    def generic_visit(self, node):
        raise UnhandledNode(node)

    def get_variable_definitions(self):
        text = ""
        for name, var in self.context.locals():
            if not var.is_arg:
                text += f"  {var.tp.c_type} {name};\n"
        return text
