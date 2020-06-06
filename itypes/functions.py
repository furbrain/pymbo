from typing import List

import utils
from . import InferredType


class NativeFunction(InferredType):
    def __init__(self,
                 name: str,
                 args: List[InferredType],
                 returns: InferredType,
                 definition: str,
                 implementation: str):
        super().__init__()
        self.name = name
        self.args = args
        self.retval = returns
        self.definition = definition
        self.implementation = implementation
        self.type = "FUNCTION"

    @utils.do_not_recurse('...')
    def __str__(self):
        args = [str(arg) for arg in self.args]
        return f"{self.name}({', '.join(args)}) -> ({self.retval})"
