from . import modules

class Document:
    def __init__(self, text, location):
        self.text = text
        self.location = location
        self.module = modules.module_from_text(text, location, self)
        self.scopes = self.module.scope_list





