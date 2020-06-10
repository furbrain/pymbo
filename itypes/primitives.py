from itypes import InferredType
from itypes.basics import get_type_name


class IntType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = int
        self.name = get_type_name(int)
        self.spec_file = "number.py"
        self.c_type = "int"


class FloatType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = float
        self.name = get_type_name(float)
        self.spec_file = "number.py"
        self.c_type = "double"
