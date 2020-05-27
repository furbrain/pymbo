import logging

from .. import itypes, scopes, utils
from . import module_finder


class ModuleRepository:
    known_modules = {}
    @classmethod
    def get_module_from_name(cls, name, scope, level=0):
        parent_module = scope.get_module()
        document = parent_module.document
        filename = module_finder.find_module(name, level, parent_module.filename, document.location)
        return cls.get_module_from_filename(filename, name, scope)
    
    @classmethod    
    def get_module_from_filename(cls, filename, name, scope):
        logging.info("Opening {} from {}".format(name, filename))
        if filename in cls.known_modules:
            mod = cls.known_modules[filename]
            logging.debug("attr for {}: {}".format(name, str(mod.attrs)))
            return mod
        parent_module = scope.get_module()
        mod = itypes.ModuleType(name, parent_module.document, filename)
        cls.known_modules[filename] = itypes.UnknownType()
        try:
            with open(filename) as f:
                mod = module_from_text(f.read(), filename, parent_module.document, name=name)
                cls.known_modules[filename] = mod
        except (IOError, TypeError) as e:
            logging.warn("Error opening {} as {}: {}".format(name, filename, e))
        logging.debug("attr for {}: {}".format(name, str(mod.attrs)))
        return mod
        
def module_from_name(name, scope, level=0):
    return ModuleRepository.get_module_from_name(name, scope, level)

def module_from_text(text, filename, document, name="__main__"):
    from . import statements
    mod = itypes.ModuleType(name, document, filename)
    scope = scopes.Scope('__main__', line_start=0, indent=-1, line_end=len(text.splitlines()))
    scope.module = mod
    mod_node = utils.get_matching_node(text, 'Module')
    statements.parse_statements(mod_node.body, scope)
    lines = scopes.IndentGetter.get_lines(mod_node)
    mod.scope_list = scope.create_scope_list(lines)
    mod.scope = scope
    for name, typeset in scope.context.items():
        mod.add_attr(name, typeset)
    return mod    
    
