from collections import defaultdict
from typing import Sequence, Dict, Optional

from typed_ast import ast3 as ast

from functions import FunctionImplementation
from itypes import InferredType

TypeSig = Sequence[InferredType]


class Context:
    def __init__(self):
        self.func_nodes: Dict[str, ast.FunctionDef] = {}
        self.func_implementations: Dict[str, Dict[str, FunctionImplementation]] = defaultdict(dict)

    def get_func(self, name: str, typesig: TypeSig) -> Optional[FunctionImplementation]:
        if name in self.func_nodes:
            if typesig not in self.func_implementations[name]:
                impl = FunctionImplementation(self.func_nodes[name], typesig, self)
                self.func_implementations[name][typesig] = impl
            return self.func_implementations[name][typesig]
        else:
            return None

    def get_func_name(self, name: str, typesig: TypeSig):
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
        text += func.get_variable_definitions()
        text += func.body
        text += "}"
        return text

    def get_definition(self, name: str, typesig: TypeSig):
        return self.get_signature(name, typesig) + ";\n"

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

    def add_function(self, node: ast.FunctionDef):
        self.func_nodes[node.name] = node
