import ast
from .. import itypes, scopes

def get_function_skeleton_from_node(node):
    arg_names = [arg.arg for arg in node.args.args]
    docstring = ast.get_docstring(node)
    return itypes.FunctionType(node.name, arg_names, itypes.UnknownType('return'), docstring)
        
def create_member_scope_from_node(func, node, parent_scope, owning_class):
    first_arg = None
    if node.args.args:  # exclude case where no args applied - likely staticmethod
        if any(node_is_classmethod(n) for n in node.decorator_list):
            first_arg = owning_class
        elif not any(node_is_staticmethod(n) for n in node.decorator_list):
            first_arg = owning_class.instance_type
        else:
            first_arg = None
    scope =  create_basic_scope_from_node(func, node, parent_scope.parent, first_arg)
    scope[owning_class.name] = owning_class
    return scope
    
def create_function_scope_from_node(func, node, parent_scope):
    return create_basic_scope_from_node(func, node, parent_scope)

def create_basic_scope_from_node(func, node, parent_scope, first_arg=None):
    if parent_scope is None:
        parent_scope = scopes.Scope('__test__', 0, -1)
    scope = scopes.Scope(node.name, node.lineno, node.col_offset, parent=parent_scope)
    args_dict = make_arg_dict(node.args)
    if first_arg is not None:
        args_dict[node.args.args[0].arg] = first_arg
    for name, arg_type in args_dict.items():
        scope[name] = arg_type
    if node.args.vararg:
        list_element_type = itypes.UnknownType(node.args.vararg.arg)
        inferred_list = itypes.create_list(list_element_type)
        scope[node.args.vararg.arg] = inferred_list
    if node.args.kwarg:
        inferred_dict = itypes.create_dict(keys=[itypes.get_type_by_name('<str>')],
                                             values=[itypes.UnknownType()])
        scope[node.args.kwarg.arg] = inferred_dict
    scope[node.name] = func
    return scope

def node_is_staticmethod(node):
    return getattr(node, "id", "") == "staticmethod"

def node_is_classmethod(node):
    return getattr(node, "id", "") == "classmethod"

def make_arg_dict(node):
    dct = {}
    for arg in node.args:
        name = arg.arg
        dct[name] = itypes.UnknownType(name)
    return dct
