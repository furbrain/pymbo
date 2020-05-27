import ast

from .. import itypes
from . import functions, classes, expressions, assignment, modules


def parse_statements(statements, scope=None, class_type=None):
    if isinstance(statements, str):
        statements = [ast.parse(statements)]
    parser = StatementBlockTypeParser(scope, class_type)
    return parser.parse_statements(statements)

class StatementBlockTypeParser(ast.NodeVisitor):
    def __init__(self, scope, class_type=None):
        self.scope = scope
        self.returns = itypes.TypeSet()
        self.class_type = class_type

    def parse_statements(self, nodes):
        for node in nodes:
            self.visit(node)
        return {'return': self.returns}

    def visit_Assign(self, node):
        for target in node.targets:
            assignment.assign_to_node(target, node.value, self.scope)

    def visit_AugAssign(self, node):
        op_node = ast.BinOp(node.target, node.op, node.value)
        assignment.assign_to_node(node.target, op_node, self.scope)

    def visit_For(self, node):
        iterator = expressions.get_expression_type(node.iter, self.scope).get_iter()
        assignment.assign_to_node(node.target, iterator, self.scope)
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.visit_For(node)

    def visit_With(self, node):
        for item in node.items:
            if item.optional_vars:
                assignment.assign_to_node(item.optional_vars, item.context_expr, self.scope)
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.visit_With(node)

    def visit_FunctionDef(self, node):
        func = functions.get_function_skeleton_from_node(node)
        if self.class_type is not None:
            func_scope = functions.create_member_scope_from_node(func, node, self.scope, self.class_type)
        else:
            func_scope = functions.create_function_scope_from_node(func, node, self.scope)
        results = parse_statements(node.body, func_scope)
        if results['return']:
            func.return_values = results['return']
        else:
            func.return_values = itypes.get_type_by_name('None')
        self.scope[node.name] = func        

    def visit_ClassDef(self, node):
        class_ = classes.get_class_skeleton_from_node(node, self.scope)
        self.scope[node.name] = class_
        class_scope = classes.create_class_scope_from_node(node, self.scope)
        parse_statements(node.body, class_scope, class_)
        classes.apply_scope_to_class(class_, class_scope)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.scope[name] = modules.module_from_name(alias.name, self.scope)

    def visit_ImportFrom(self, node):
        module = modules.module_from_name(node.module, self.scope, node.level)
        for alias in node.names:
            name = alias.asname or alias.name
            if not module.has_attr(alias.name):
                if hasattr(module, 'scope'):
                    module.set_attr(alias.name, modules.module_from_name(alias.name, module.scope, level=1))
            self.scope[name] = module.get_attr(alias.name)
            
    def visit_Return(self, node):
        if node.value:
            self.returns = self.returns.add_type(expressions.get_expression_type(node.value, self.scope))
        else:
            self.returns = self.returns.add_type(itypes.get_type_by_name('None'))
            

