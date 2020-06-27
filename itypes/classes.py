from textwrap import indent
from typing import Dict

from context import Code
from itypes import InferredType


class ClassType(InferredType):
    def __init__(self, name: str):
        super().__init__()
        self.members: Dict[str, InferredType] = {}
        self.class_vars: Dict[str, Code] = {}
        self.class_var_initial: Dict[str, Code] = {}
        self.name = name
        self.spec_file = "classes.py"
        self.c_type = name

    def member_defs(self):
        text = "\n".join(tp.declare(name) for name, tp in self.members.items())
        return indent(text, " " * 4)

    def get_attr_code(self, attr: str, obj: Code) -> Code:
        if attr in self.class_vars:
            return self.class_vars[attr]
        else:
            raise AttributeError(f"Class {self.name} has no attribute {attr}")

    def add_class_var(self, name: str, code: Code):
        attr_name = f"{self.name}__{name}"
        self.class_vars[name] = Code(tp=code.tp, code=attr_name)
        self.class_var_initial[attr_name] = code

    def get_definitions(self):
        defs = super().get_definitions()
        for name, value in self.class_var_initial.items():
            defs += f"{value.tp.c_type} {name} = {value.code};\n"
        return defs
