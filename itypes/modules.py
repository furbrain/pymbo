from . import basics

class ModuleType(basics.InferredType):
    def __init__(self, name, document, filename):
        super().__init__()
        self.name = name
        self.document = document
        self.filename = filename

