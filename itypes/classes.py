import ast

from . import basics

class ClassType(basics.InferredType):
    def __init__(self, name,  parents, docstring=""):
        super().__init__()
        self.name = name
        for parent in parents:
            for tp in parent:
                self.attrs.update(tp.attrs)
        self.instance_type = InstanceType(self)
        self.return_values = self.instance_type
        
    def add_attr(self, attr, typeset):
        super().add_attr(attr, typeset)
        self.instance_type.add_attr(attr, typeset)

    def get_call_return(self, arg_list):
        return self.instance_type

class InstanceType(basics.InferredType):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.name = "<{}>".format(parent)
        self.attrs.update(parent.attrs)
