import ast

from . import expressions
from .. import itypes, scopes

def get_class_skeleton_from_node(node, scope):
    name = node.name
    parents = [expressions.get_expression_type(x, scope) for x in node.bases]
    docstring = ast.get_docstring(node)
    return itypes.ClassType(name, parents, docstring)
    
def create_class_scope_from_node(node, parent_scope):
    return scopes.Scope(node.name, line_start=node.lineno, indent=node.col_offset, parent=parent_scope)

def apply_scope_to_class(class_, scope):
    #class_.scope = scope
    for k, v in scope.context.items():
        class_.add_attr(k, v)


