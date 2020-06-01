import typed_ast.ast3 as ast
from typing import TYPE_CHECKING
from old_parsers import get_expression_type_and_code
from itypes import get_type_by_value
from scopes import Scope
from exceptions import UnhandledNode

if TYPE_CHECKING:
    from context import TypeSig


class FunctionImplementation(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef, type_sig: "TypeSig", funcs: "FuncDB"):
        self.definition = ""
        self.body = ""
        self.retval = get_type_by_value(None)
        self.scope = Scope("test.py", 0, 0)
        self.args = []
        for arg, arg_type in zip(node.args.args, type_sig):
            self.scope[arg.arg] = arg_type
            self.args += [arg_type.as_c_type() + " "+ arg.arg]
        self.indent = 2
        self.type_sig = type_sig
        self.funcs = funcs
        for n in node.body:
            self.visit(n)

    def start_line(self, text: str) -> None:
        self.body += " " * self.indent
        self.body += text

    def visit_If(self, node: ast.If) -> None:
        itype, code = self.get_type_and_code(node.test)
        self.start_line("if ({}) {{\n".format(code))
        self.indent +=2
        for n in node.body:
            self.visit(n)
        if node.orelse:
            self.indent -=2
            self.start_line("} else {\n")
            self.indent +=2
            for n in node.orelse:
                self.visit(n)
        self.indent -= 2
        self.start_line("}\n")

    def visit_Return(self, node: ast.Return) -> None:
        itype, code = self.get_type_and_code(node.value)
        self.retval = itype #FIXME add error checking code here for multiple retvals
        self.start_line("return " + code + ";\n")

    def visit_Expr(self, node: ast.Expr) -> None:
        itype, code = self.get_type_and_code(node.value)
        self.start_line(code + ";\n")

    def visit_Assign(self, node: ast.Assign) -> None:
        right = self.get_type_and_code(node.value)
        for n in node.targets:
            self.scope[n.id] = right[0]
            left = self.get_type_and_code(n)
            self.start_line("{} = {};\n".format(left[1],right[1]))

    def get_type_and_code(self, node):
        type, code = get_expression_type_and_code(node, self.scope, self.funcs)
        return type, code

    def generic_visit(self, node):
        raise UnhandledNode(self.scope, node)

    def get_variable_definitions(self):
        text = ""
        for var, tp in self.scope.context.items():
            text += f"  {tp.as_c_type()} {var};\n"
        return text

