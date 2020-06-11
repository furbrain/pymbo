import inspect
import traceback

from typed_ast import ast3 as ast

from context import Context, Code
from exceptions import PymboError, UnhandledNode, StaticTypeError, InvalidOperation
from funcdb import FuncDB
from itypes.typedb import TypeDB
from parser.expressions import get_constant_code


# noinspection PyPep8Naming
class ModuleParser(ast.NodeVisitor):
    def __init__(self):
        self.funcs = FuncDB(self)
        self.context = Context()
        self.text = ""
        self.name = ""
        self.globals = []

    def parse_string(self, text: str):
        self.text = text
        self.name = "<string>"
        self.parse()

    def parse_file(self, fname: str):
        with open(fname, 'r') as f:
            self.text = f.read()
        self.name = fname
        self.parse()

    def parse(self):
        tree = ast.parse(self.text, self.name)
        self.wrap_exception(self.visit, tree)

    def wrap_exception(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except PymboError as exc:
            tb = exc.__traceback__
            for frame in reversed(list(traceback.walk_tb(tb))):
                if frame[0].f_code.co_name.startswith("visit_") \
                        or frame[0].f_code.co_name == "generic_visit":
                    args = inspect.getargvalues(frame[0])
                    node: ast.AST = args.locals["node"]
                    message = f'{exc.args[0]}\n  at File "{self.name}", line {node.lineno:d}\n'
                    message += '    ' + self.text.splitlines()[node.lineno - 1]
                    exc.args = (message,)
                    raise exc
            raise exc

    def create_code(self, include_type_funcs=False):
        self.funcs.get_implementation("main", ())
        code = ""
        if include_type_funcs:
            for t in TypeDB.types.values():
                code += t.get_type_def()
        code += ''.join(self.globals)
        if include_type_funcs:
            for t in TypeDB.types.values():
                code += t.get_definitions()
                code += t.get_implementations()
        code += "\n".join(self.funcs.get_all_definitions())
        code += "\n"
        code += "\n\n".join(self.funcs.get_all_implementations())
        return code

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # ignore any inner function defs - not supported...
        self.funcs.add_function(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        # ignore any defs within classes
        pass

    def visit_Module(self, node):
        super().generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        right = get_constant_code(node.value, self)
        for n in node.targets:
            if isinstance(n, ast.Name):
                if n.id in self.context:
                    raise StaticTypeError("Cannot redefine global variables")
                self.context[n.id] = Code(tp=right.tp, code=n.id)
                left = self.context[n.id]
                self.globals += [f"{left.tp.c_type} {n.id} = {right.as_value()};\n"]
            else:
                raise InvalidOperation("Can only initialise global variables")

    def generic_visit(self, node):
        raise UnhandledNode(node)
