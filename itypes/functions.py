import ast
from typing import List

from . import InferredType
import utils

class NativeFunction(InferredType):
    def __init__(self, name: str, args: List[InferredType], returns: InferredType, definition: str, implementation: str):
        super().__init__()
        self.name = name
        self.args = args
        self.retval = returns
        self.definition = definition
        self.implementation = implementation
        self.type = "FUNCTION"

    @utils.do_not_recurse('...')
    def __str__(self):
        return "%s(%s) -> (%s)" % (self.name, ', '.join(self.args), self.return_values)
