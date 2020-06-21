from itypes import InferredType


class StrType(InferredType):
    pass_by_value = False

    def __init__(self, maxlen: int):
        super().__init__()
        self.maxlen = maxlen
        self.type = str
        self.name = f"str:{maxlen:d}"
        self.spec_file = "strings.py"
        self.c_type = self.prefix()

    def prefix(self):
        return f"str__{self.maxlen:d}"

    def as_literal(self, value):
        return f'({self.c_type}){{"{value}"}}'
