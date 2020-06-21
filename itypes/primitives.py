from itypes import InferredType


class IntType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = int
        self.name = "int"
        self.spec_file = "number.py"
        self.c_type = "int"

    def can_coerce_from(self, other: "InferredType") -> bool:
        if other in ("int", "bool"):
            return True
        return False


class FloatType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = float
        self.name = "float"
        self.spec_file = "number.py"
        self.c_type = "double"

    def can_coerce_from(self, other: "InferredType") -> bool:
        if other in ("float", "int", "bool"):
            return True
        return False


class BoolType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = bool
        self.name = "bool"
        self.spec_file = ""
        self.c_type = "bool"

    def can_coerce_from(self, other: "InferredType") -> bool:
        if other in ("float", "int", "bool"):
            return True
        return False


class NoneType(InferredType):
    def __init__(self):
        super().__init__()
        self.type = type(None)
        self.name = "None"
        self.spec_file = ""
        self.c_type = "void"
