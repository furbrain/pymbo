import ast

from . import basics, builtins
import utils

class FunctionType(basics.InferredType):
    def __init__(self, name, args, returns, docstring):
        super().__init__()
        self.name = name
        self.args = args
        self.return_value = returns
        self.type = "FUNCTION"
        self.docstring = docstring

    @utils.do_not_recurse('...')
    def __str__(self):
        return "%s(%s) -> (%s)" % (self.name, ', '.join(self.args), self.return_values)

    def get_call_return(self, arg_types):
        type_mapping = {k: v for k, v in zip(self.args, arg_types)}
        if isinstance(self.return_value, basics.UnknownType):
            replacement_type = type_mapping.get(possible_type.type, basics.UnknownType())
            return replacement_type
        else:
            return self.return_value
