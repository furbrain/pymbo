from typing import Set

import typed_ast.ast3 as ast

from context import Context, Code
from exceptions import UnhandledNode, UnimplementedFeature, InvalidOperation, UnknownVariable, StaticTypeError
from itypes import TypeDB
from itypes.classes import ClassInstance
from itypes.functions import TypeSig
from itypes.lists import EmptyList
from parser import get_expression_code, annotations


# noinspection PyPep8Naming
class FunctionImplementation(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef, type_sig: "TypeSig", context: Context):
        self.body: str
        self.indent: int
        self.retval: Code
        self.all_paths_return: bool
        self.primary_node = node
        self.context = Context(context)
        self.args = []
        self.libraries: Set[str] = set()
        for arg, arg_type in zip(node.args.args, type_sig):
            code = Code(arg_type, is_arg=True, is_pointer=not arg_type.pass_by_value, code=arg.arg)
            self.context[arg.arg] = code
            self.args.append(code)
        self.generate_code()

    def is_init(self):
        if self.primary_node.name == "__init__":
            first_arg = self.args[0]
            if first_arg.code == "self" and isinstance(first_arg.tp, ClassInstance):
                return True
        return False

    # noinspection PyAttributeOutsideInit
    def generate_code(self):
        self.body = ""
        self.in_try_block = False
        self.indent = 4
        self.retval = Code(tp=None, code="_retval", is_pointer=True)
        self.all_paths_return = False
        self.context.clear_temp_vars()
        # clear struct if class init
        if self.is_init():
            self.start_line(f"*self = ({self.args[0].tp.c_type}){{0}};\n")
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
        if self.in_try_block:
            raise InvalidOperation("Cannot return from within try block")
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

    # noinspection PyAttributeOutsideInit
    def visit_For(self, node: ast.For) -> None:
        # create list to iterate over
        lst_name = self.context.get_temp_name()
        assign_node = ast.Assign(targets=[ast.Name(id=lst_name, ctx=ast.Store())],
                                 value=node.iter)
        self.visit(assign_node)

        lst = self.context[lst_name]
        index = self.context.get_temp_var(TypeDB.get_type_by_name("int"))
        length = lst.tp.get_method("len")
        length_code = length.get_code(self.context, lst).code

        # construct for statement
        self.start_line(f"for({index.code}=0; {index.code} < {length_code}; {index.code}++) {{\n")
        self.indent += 4
        assign_node = ast.Assign(targets=[node.target],
                                 value=ast.Subscript(value=ast.Name(id=lst_name, ctx=ast.Load()),
                                                     slice=ast.Index(value=ast.Name(id=index.code, ctx=ast.Load())),
                                                     ctx=ast.Load()))
        self.visit(assign_node)
        for statement in node.body:
            self.visit(statement)
        self.indent -= 4
        self.start_line("}\n")
        self.all_paths_return = False

    def visit_Assign(self, node: ast.Assign) -> None:
        right = self.get_expression_code(node.value)
        for n in node.targets:
            self.assign_target(n, right)

    def assign_target(self, node, value):
        if isinstance(value.tp, EmptyList):
            func_node = ast.Expr(value=ast.Call(func=ast.Attribute(value=node,
                                                                   attr="clear"),
                                                args=[]))
            try:
                self.visit(func_node)
            except UnknownVariable:
                raise StaticTypeError("Must specify a list type when assigning an empty list")
            return
        if isinstance(node, ast.Name):
            left = self.context.assign_type(node.id, value.tp)
            self.start_line("{} = {};\n".format(left.code, value.as_value()))
        elif isinstance(node, ast.Subscript):
            container = self.get_expression_code(node.value)
            if isinstance(node.slice, ast.Index):
                index = self.get_expression_code(node.slice.value)
                setter = container.tp.get_method("set_item")
                code = setter.get_code(self.context, container, index, value)
                self.start_line(f"{code.code};\n")
            else:
                raise UnimplementedFeature("Slices not yet implemented")
        elif isinstance(node, ast.Attribute):
            owner = self.get_expression_code(node.value)
            owner.tp.set_attr(node.attr, value)
            left = self.get_expression_code(node)
            self.start_line(f"{left.code} = {value.code};\n")

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            self.context.assign_type(node.target.id, annotations.get_type(node.annotation))
        if node.value is not None:
            value = self.get_expression_code(node.value)
            self.assign_target(node.target, value)

    def visit_Try(self, node: ast.Try):
        if node.orelse:
            raise UnimplementedFeature("Can't have an else section to try")
        if node.finalbody:
            raise UnimplementedFeature("Can't have an finally section to try")
        self.start_line("Try {\n")
        self.indent += 4
        self.in_try_block = True
        for n in node.body:
            self.visit(n)
        # noinspection PyAttributeOutsideInit
        self.in_try_block = False
        self.indent -= 4
        exception_name = self.context.get_temp_var(TypeDB.get_type_by_name("int"))
        self.start_line(f"}} Catch({exception_name.code}) {{\n")
        self.indent += 4
        self.start_line(f"switch ({exception_name.code}) {{\n")
        for handler in node.handlers:
            if handler.type is None:
                self.start_line("case default:\n")
            else:
                self.start_line(f"case {handler.type.id}:\n")
            self.indent += 4
            for n in handler.body:
                self.visit(n)
            self.start_line("break;\n")
            self.indent -= 4
        self.start_line("}")
        self.indent -= 4
        self.start_line("}")

    def visit_Pass(self, node):
        return

    def visit_Raise(self, node):
        self.start_line(f"Throw({node.exc.id});\n")

    def get_expression_code(self, node: ast.AST) -> Code:
        code, prepends = get_expression_code(node, self.context)
        for line in prepends:
            if isinstance(line, str):
                self.start_line(line)  # if is a string, add string
            else:
                self.visit(line)  # otherwise treat as a node
        self.libraries.update(code.libraries)
        return code

    def generic_visit(self, node):
        raise UnhandledNode(node)

    def get_variable_definitions(self):
        text = ""
        for name, var in self.context.locals():
            if not var.is_arg:
                text += var.tp.declare(name)
        return text
