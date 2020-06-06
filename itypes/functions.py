from typing import List

import utils
from context import Code
from exceptions import StaticTypeError
from . import InferredType, can_promote


class FunctionType(InferredType):
    def __init__(self, name: str, args: List[InferredType], returns: InferredType):
        super().__init__()
        self.name = name
        self.args = args
        self.retval = returns

    def get_code(self, obj: Code, args: List[Code]):
        raise NotImplementedError

    def check_code(self, args):
        if len(args) < len(self.args):
            raise StaticTypeError(f"Not enough arguments (needs {len(self.args)}")
        if len(args) > len(self.args):
            raise StaticTypeError(f"Too many arguments (needs {len(self.args)}")
        for i, (supplied, needed) in enumerate(zip(args, self.args)):
            if not can_promote(supplied.tp, needed):
                raise StaticTypeError(f"Argument {i + 1} should be {needed}, but is {supplied.tp} ")


class NativeMethod(FunctionType):
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

    @utils.do_not_recurse('...')
    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    def get_code(self, obj: Code, args: List[Code]) -> Code:
        self.check_code(args)
        arg_strings = [arg.as_function_arg() for arg in [obj] + args]
        return Code(tp=self.retval, code=f"{self.name}({', '.join(arg_strings)})")


class InlineNativeMethod(FunctionType):
    def __init__(self,
                 name: str,
                 args: List[InferredType],
                 returns: InferredType,
                 template: str):
        super().__init__(name, args, returns)
        self.template = template
        self.type = "NATIVE INLINE FUNCTION"

    @utils.do_not_recurse('...')
    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"

    def get_code(self, obj: Code, args: List[Code]) -> Code:
        self.check_code(args)
        # noinspection PyUnusedLocal
        arg_strings = [arg.as_function_arg() for arg in [obj] + args]
        return Code(tp=self.retval, code=eval(f"f'{self.template}'"))
