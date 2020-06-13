from collections import defaultdict
from typing import Sequence, Dict, Optional, TYPE_CHECKING, Set

from typed_ast import ast3 as ast

from itypes import InferredType
from itypes.functions import PythonFunction, FunctionType
from parser.functions import FunctionImplementation

TypeSig = Sequence[InferredType]
if TYPE_CHECKING:  # pragma: no cover
    from parser.module import ModuleParser


class FuncDB:
    def __init__(self, module: "ModuleParser"):
        self.module = module
        self.func_nodes: Dict[str, ast.FunctionDef] = {}
        self.func_implementations: Dict[str, Dict[TypeSig, PythonFunction]] = defaultdict(dict)
        self.libraries: Set[str] = set()

    def get_func(self, name: str, typesig: TypeSig) -> Optional[FunctionType]:
        if name in self.func_nodes:
            if typesig not in self.func_implementations[name]:
                impl = FunctionImplementation(self.func_nodes[name], typesig, self.module)
                func_name = self.get_func_name(name, typesig)
                functype = PythonFunction(func_name,
                                          [param.tp for param in impl.params()],
                                          impl.retval.tp,
                                          definition=self.get_definition(func_name, impl),
                                          implementation=self.get_implementation(func_name, impl))
                self.libraries.update(impl.libraries)
                self.func_implementations[name][typesig] = functype
            return self.func_implementations[name][typesig]
        else:
            return None

    def get_func_name(self, name: str, typesig: TypeSig):
        if len(self.func_implementations[name]) == 0:
            return name
        elif typesig in self.func_implementations[name]:
            return self.func_implementations[name][typesig].name
        else:
            args = [str(x).strip("<>") for x in typesig]
            return name + "__" + '_'.join(args)

    @staticmethod
    def get_signature(func_name: str, impl: FunctionImplementation):
        params = ', '.join(x.as_param() for x in impl.params())
        text = f"{impl.retval_in_c()} {func_name}({params})"
        return text

    def get_implementation(self, func_name: str, impl: FunctionImplementation, regenerate=False):
        text = self.get_signature(func_name, impl) + " {\n"
        text += impl.get_variable_definitions()
        if regenerate:
            impl.generate_code()
        text += impl.body
        text += "}"
        return text

    def get_definition(self, func_name: str, impl: FunctionImplementation):
        return self.get_signature(func_name, impl) + ";\n"

    def get_all_definitions(self):
        results = []
        for func, sigs in self.func_implementations.items():
            results += [sig.definition for sig in sigs.values()]
        return results

    def get_all_implementations(self):
        results = []
        for func, sigs in self.func_implementations.items():
            results += [sig.implementation for sig in sigs.values()]
        return results

    def add_function(self, node: ast.FunctionDef):
        self.func_nodes[node.name] = node
