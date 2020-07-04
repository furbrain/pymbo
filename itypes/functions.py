import re
from abc import ABCMeta, abstractmethod
from textwrap import indent
from typing import List, Dict, Sequence, TYPE_CHECKING, Union

import typed_ast.ast3 as ast

from context import Code, Context
from exceptions import StaticTypeError, InvalidOperation
from . import InferredType

if TYPE_CHECKING:
    from parser import FunctionImplementation


class FunctionType(InferredType):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @abstractmethod
    def get_code(self, context, *args: Code):
        pass


class FixedFunctionType(FunctionType, metaclass=ABCMeta):
    def __init__(self, name: str, args: List[InferredType], returns: InferredType):
        super().__init__(name)
        self.args = args
        self.retval = returns

    def check_code(self, args):
        if len(args) < len(self.args):
            raise StaticTypeError(f"Not enough arguments (needs {len(self.args)}), given {args}")
        if len(args) > len(self.args):
            raise StaticTypeError(f"Too many arguments (needs {len(self.args)})")
        for i, (supplied, needed) in enumerate(zip(args, self.args)):
            if not needed.can_coerce_from(supplied.tp):
                raise StaticTypeError(f"Argument {i + 1} should be {needed}, but is {supplied.tp} ")

    @classmethod
    @abstractmethod
    def from_dict(cls, name, dct):
        pass

    @classmethod
    def get_args_and_retval(cls, dct):
        from itypes.typedb import TypeDB
        args = [arg.strip() for arg in dct['args'].split(',')]
        if args == ['']:
            args = []
        else:
            args = [TypeDB.get_type_by_name(arg) for arg in args]
        retval = TypeDB.get_type_by_name(dct['retval'])
        return args, retval


class CMethod(FixedFunctionType):
    def __init__(self,
                 name: str,
                 args: List[InferredType],
                 returns: InferredType,
                 definition: str,
                 implementation: str):
        super().__init__(name, args, returns)
        self.definition = definition
        self.implementation = implementation
        self.type = "NATIVE FUNCTION"

    @classmethod
    def from_dict(cls, name: str, dct: Dict[str, str]):
        args, retval = cls.get_args_and_retval(dct)
        arg_names = [arg_name.strip() for arg_name in dct['arg_names'].split(',')]
        param_list = [f"{arg.fn_type()} {arg_name}" for arg, arg_name in zip(args, arg_names)]
        if retval.pass_by_value:
            signature = f"{retval.c_type} {name}({', '.join(param_list)})"
        else:
            param_list += [f"{retval.fn_type()} _retval"]
            signature = f"void {name}({', '.join(param_list)})"
            args.append(retval)
            dct['imp'] = re.sub(r"return (.*?);", r"*_retval = \1; return;", dct['imp'])
        implementation = f"{signature} {{{indent(dct['imp'], ' ' * 4)}}}\n"
        definition = f"{signature};\n"
        method = cls(name, args, retval, definition, implementation)
        return method

    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    def get_code(self, context, *args: Code) -> Code:
        self.check_code(args)
        arg_strings = [arg.as_function_arg() for arg in args]
        return Code(tp=self.retval, code=f"{self.name}({', '.join(arg_strings)})")


class InlineCMethod(FixedFunctionType):
    def __init__(self,
                 name: str,
                 args: List[InferredType],
                 returns: InferredType,
                 priority: int,
                 template: str):
        super().__init__(name, args, returns)
        self.template = template
        self.priority = priority
        self.type = "NATIVE INLINE FUNCTION"

    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    @classmethod
    def from_dict(cls, name: str, dct: Dict[str, Union[str, int]]):
        args, retval = cls.get_args_and_retval(dct)
        method = cls(name, args, retval, dct['priority'], dct['template'])
        return method

    def get_code(self, context, *args: Code) -> Code:
        self.check_code(args)
        # noinspection PyUnusedLocal
        for i, arg in enumerate(args):
            if i == 0:
                if arg.priority > self.priority:
                    arg.code = f"({arg.code})"
            else:
                if arg.priority >= self.priority:
                    arg.code = f"({arg.code})"
        return Code(tp=self.retval, code=eval(f"f'{self.template}'"), priority=self.priority)


class PythonFunction(CMethod):
    pass


class ComputedFunction(FixedFunctionType, metaclass=ABCMeta):
    @classmethod
    def from_dict(cls, name, dct):
        pass


TypeSig = Sequence[InferredType]


class MultiFunction(FunctionType):
    """This function represents a python function in the code to be translated
    It can be implemented in several different ways, and should possibly register itself with TypeDB"""

    def __init__(self, node: ast.FunctionDef, context: Context, name=None):
        if name is None:
            name = node.name
        super().__init__(name)
        if node.args.vararg:
            raise InvalidOperation("Variable number args not permitted")
        if node.args.kwarg:
            raise InvalidOperation("Arbitrary kwargs not permitted")
        if node.args.kwonlyargs:
            raise InvalidOperation("Keyword only arguments not permitted")
        self.arg_names = node.args.args
        self.implementations: Dict[TypeSig, PythonFunction] = {}
        self.node = node
        self.context = context

    def get_code(self, context, *args: Code):
        func = self.get_fixed_function(*args)
        return func.get_code(context, *args)

    def get_definitions(self):
        return "".join(imp.definition for imp in self.implementations.values())

    def get_implementations(self):
        return "".join(imp.implementation for imp in self.implementations.values())

    @staticmethod
    def get_signature(func_name: str, impl: "FunctionImplementation"):
        params = ', '.join(x.as_param() for x in impl.params())
        text = f"{impl.retval_in_c()} {func_name}({params})"
        return text

    def get_func_name(self, typesig: TypeSig):
        if len(self.implementations) == 0:
            return self.name
        elif typesig in self.implementations:
            return self.implementations[typesig].name
        else:
            args = [str(x.c_type) for x in typesig]
            return self.name + "__" + '_'.join(args)

    def get_implementation(self, func_name: str, impl: "FunctionImplementation", regenerate=False):
        text = self.get_signature(func_name, impl) + " {\n"
        text += indent(impl.get_variable_definitions(), " " * 4)
        if regenerate:
            impl.generate_code()
        text += impl.body
        text += "}"
        return text

    def get_definition(self, func_name: str, impl: "FunctionImplementation"):
        return self.get_signature(func_name, impl) + ";\n"

    def get_fixed_function(self, *args: Code):
        typesig = tuple(arg.tp for arg in args if arg.tp is not None)
        if typesig not in self.implementations:
            from parser import FunctionImplementation
            impl = FunctionImplementation(self.node, typesig, self.context)
            func_name = self.get_func_name(typesig)
            functype = PythonFunction(func_name,
                                      [param.tp for param in impl.params()],
                                      impl.retval.tp,
                                      definition=self.get_definition(func_name, impl),
                                      implementation=self.get_implementation(func_name, impl))
            # self.libraries.update(impl.libraries)
            self.implementations[typesig] = functype
        return self.implementations[typesig]
