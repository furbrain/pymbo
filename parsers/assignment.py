import ast

from . import expressions
from .. import itypes, utils

def assign_to_node(target, value, scope):
    if isinstance(target, str):
        target = ast.parse(target, mode="eval").body
    if isinstance(value, str):
        value = ast.parse(value, mode="eval").body
    if utils.is_ast_sequence(target):
        if utils.is_ast_node(value) and utils.is_ast_sequence(value):
            values = []
            for elt in value.elts:
                if utils.is_ast_starred(elt):
                    values.extend(expressions.get_expression_type(elt.value, scope).get_star_expansion())
                else:
                    values.append(expressions.get_expression_type(elt, scope))
            for i, subtarget in enumerate(target.elts):
                if utils.is_ast_starred(subtarget):
                    assign_to_node(subtarget, itypes.create_list(*values[i:]), scope)
                else:
                    assign_to_node(subtarget, values[i], scope)
            return
        elif itypes.is_inferred_type(value):
            for i, subtarget in enumerate(target.elts):
                if utils.is_ast_starred(subtarget):
                    elements = value.get_slice_from(i)
                    element_list = itypes.create_list(*elements)
                    assign_to_node(subtarget, element_list, scope)
                else:
                    assign_to_node(subtarget, value.get_item(i), scope)
            return
    if utils.is_ast_node(value):
        value = expressions.get_expression_type(value, scope)
    parser = Assigner(scope, value)
    parser.visit(target)


class Assigner(ast.NodeVisitor):
    def __init__(self, scope, value):
        self.scope = scope
        self.value = value

    def visit_Name(self, node):
        name = node.id
        if name in self.scope:
            self.scope[name] = self.scope[name].add_type(self.value)
        else:
            self.scope[name] = self.value

    def visit_Attribute(self, node):
        types = expressions.get_expression_type(node.value, self.scope)
        attr = node.attr
        types.add_attr(attr, self.value)

    def visit_Subscript(self, node):
        types = expressions.get_expression_type(node.value, self.scope)
        slice_type = type(node.slice).__name__
        if slice_type == "Index":
            types.add_item(self.value)
        else:
            for val in self.value:
                if itypes.is_inferred_sequence(val):
                    types.add_item(val.get_item(0))

    def visit_Call(self, node):
        # do nothing as does  not affect scope or classes
        pass
