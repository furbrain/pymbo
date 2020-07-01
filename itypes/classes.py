from textwrap import indent
from typing import Dict

from context import Code, Context
from exceptions import StaticTypeError
from itypes import InferredType
from itypes.functions import MultiFunction


class ClassType(InferredType):
    pass_by_value = False

    def __init__(self, name: str):
        super().__init__()
        self.class_vars = Context()
        self.members = Context(self.class_vars)
        self.class_var_initial: Dict[str, Code] = {}
        self.name = name
        self.spec_file = "classes.py"
        self.c_type = name
        self.instance = ClassInstance(self)
        self.retval = self.instance
        self.methods: Dict[str, MultiFunction] = {}

    def member_defs(self):
        text = "\n".join(code.tp.declare(name) for name, code in self.members.locals())
        return indent(text, " " * 4)

    def get_attr_code(self, attr: str, obj: Code) -> Code:
        if attr in self.class_vars:
            return self.class_vars[attr]
        else:
            raise AttributeError(f"Class {self.name} has no attribute {attr}")

    def get_code(self, context: Context, *args: Code):
        init_func = self.methods["__init__"]
        return init_func.get_code(context, *args)

    def set_attr(self, attr: str, obj: Code):
        attr_name = f"{self.name}__{attr}"
        self.class_vars.assign_type(attr, obj.tp, attr_name)
        self.class_var_initial[attr_name] = obj

    def add_method(self, name: str, f: MultiFunction):
        self.methods[name] = f

    def get_definitions(self):
        defs = super().get_definitions() + "\n"
        for name, value in self.class_var_initial.items():
            defs += f"{value.tp.c_type} {name} = {value.code};\n"

        for method in self.methods.values():
            defs += method.get_definitions()
        return defs

    def get_implementations(self):
        imps = super().get_implementations()
        for method in self.methods.values():
            imps += method.get_implementations() + "\n\n"
        return imps


class ClassInstance(InferredType):
    pass_by_value = False

    def __init__(self, cls: ClassType):
        super().__init__()
        self.cls = cls
        self.name = f"<{cls.name}>"
        self.c_type = cls.c_type

    def set_attr(self, attr: str, obj: Code):
        self.cls.members.assign_type(attr, obj.tp)

    def get_attr_code(self, attr: str, obj: Code) -> Code:
        if attr in self.cls.class_vars:
            return self.cls.class_vars[attr]
        else:
            try:
                val = self.cls.members[attr]
                text = f"{obj.as_accessor()}{attr}"
                return Code(tp=val.tp, code=text)
            except KeyError:
                raise StaticTypeError(f"Instance of {self.name} has no attribute {attr}")
