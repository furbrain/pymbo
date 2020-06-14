import re
from abc import ABCMeta, abstractmethod
from textwrap import indent
from typing import List, Dict

from context import Code
from exceptions import StaticTypeError
from . import InferredType


class FunctionType(InferredType, metaclass=ABCMeta):
    def __init__(self, name: str, args: List[InferredType], returns: InferredType):
        super().__init__()
        self.name = name
        self.args = args
        self.retval = returns

    @abstractmethod
    def get_code(self, context, *args: Code):
        pass

    def check_code(self, args):
        if len(args) < len(self.args):
            raise StaticTypeError(f"Not enough arguments (needs {len(self.args)}), given {args}")
        if len(args) > len(self.args):
            raise StaticTypeError(f"Too many arguments (needs {len(self.args)}")
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


class CMethod(FunctionType):
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
        definition = f"{signature};\n\n"
        method = cls(name, args, retval, definition, implementation)
        return method

    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    def get_code(self, context, *args: Code) -> Code:
        self.check_code(args)
        arg_strings = [arg.as_function_arg() for arg in args]
        return Code(tp=self.retval, code=f"{self.name}({', '.join(arg_strings)})")


class InlineCMethod(FunctionType):
    def __init__(self,
                 name: str,
                 args: List[InferredType],
                 returns: InferredType,
                 template: str):
        super().__init__(name, args, returns)
        self.template = template
        self.type = "NATIVE INLINE FUNCTION"

    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    @classmethod
    def from_dict(cls, name: str, dct: Dict[str, str]):
        args, retval = cls.get_args_and_retval(dct)
        method = cls(name, args, retval, dct['template'])
        return method

    def get_code(self, context, *args: Code) -> Code:
        self.check_code(args)
        # noinspection PyUnusedLocal
        arg_strings = [arg.as_function_arg() for arg in args]
        return Code(tp=self.retval, code=eval(f"f'{self.template}'"))


class PythonFunction(CMethod):
    pass


class ComputedFunction(FunctionType, metaclass=ABCMeta):
    @classmethod
    def from_dict(cls, name, dct):
        pass
