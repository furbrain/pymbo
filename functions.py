import typed_ast.ast3 as ast
from collections import defaultdict
from typing import Dict, Sequence
from parsers.expressions import get_expression_type_and_code
from itypes import InferredType, get_type_by_value

TypeSig = Sequence[InferredType]

class FunctionNotFound(ValueError):
    pass

class FunctionImplementation(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef, type_sig: TypeSig, funcs: "FuncDB"):
        self.definition = ""
        self.body = ""
        self.retval = get_type_by_value(None)
        self.scope = {}
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

    def visit_Return(self, node: ast.Return) -> None:
        itype, code = get_expression_type_and_code(node.value, self.scope, self.funcs)
        self.retval = itype #FIXME add error checking code here for multiple retvals
        self.start_line("return " + code + ";\n")

    def visit_Expr(self, node: ast.Expr) -> None:
        itype, code = get_expression_type_and_code(node.value, self.scope, self.funcs)
        self.start_line(code + ";\n")

    def generic_visit(self, node):
        raise NotImplementedError("%s nodes are not yet implemented" % type(node).__name__)

class FuncDB(ast.NodeVisitor):
    def __init__(self):
        self.func_nodes: Dict[str, ast.AST] = {}
        self.func_implementations: Dict[str, Dict[str, FunctionImplementation]] = defaultdict(dict)

    def get_func(self, name: str, typesig: TypeSig) -> FunctionImplementation:
        if name in self.func_nodes:
            if typesig not in self.func_implementations[name]:
                impl = FunctionImplementation(self.func_nodes[name], typesig, self)
                self.func_implementations[name][typesig] = impl
        else:
            raise FunctionNotFound(name)
        return self.func_implementations[name][typesig]

    def get_func_name(self, name: str, typesig: TypeSig):
        self.get_func(name, typesig)
        if len(self.func_implementations[name]) == 1:
            return name
        else:
            args = [str(x).strip("<>") for x in typesig]
            return name+"__"+'_'.join(args)

    def get_signature(self, name: str, typesig: TypeSig):
        func = self.get_func(name, typesig)
        text = func.retval.as_c_type() + " " + self.get_func_name(name, typesig) + "(" + ', '.join(func.args)+")"
        return text

    def get_implementation(self, name: str, typesig: TypeSig):
        func = self.get_func(name, typesig)
        text = self.get_signature(name, typesig) + " {\n"
        text += func.body
        text += "}"
        return text

    def get_definition(self, name: str, typesig: TypeSig):
        return self.get_signature(name, typesig) + ";\n"

    def parse(self, node: ast.AST):
        self.generic_visit(node)
        return self.func_nodes

    def get_all_definitions(self):
        results = []
        for func, sigs in self.func_implementations.items():
            results += [self.get_definition(func, sig) for sig in sigs]
        return results

    def get_all_implementations(self):
        results = []
        for func, sigs in self.func_implementations.items():
            results += [self.get_implementation(func, sig) for sig in sigs]
        return results

    def visit_FunctionDef(self, node: ast.FunctionDef):
        #ignore any inner function defs - not supported...
        self.func_nodes[node.name] = node

    def visit_ClassDef(self, node: ast.ClassDef):
        #ignore any defs within classes
        pass
