from typing import TYPE_CHECKING, Optional

import typed_ast.ast3 as ast

import exceptions
import itypes
from context import Context, Code
from exceptions import UnhandledNode, UnimplementedFeature, StaticTypeError, InvalidOperation
from itypes.typedb import TypeDB
from parser.binops import OPS_MAP

if TYPE_CHECKING:  # pragma: no cover
    from parser.module import ModuleParser


def get_expression_code(expression, module: "ModuleParser", context: Optional[Context]) -> Code:
    if isinstance(expression, str):
        expression = ast.parse(expression)
    if context is None:
        context = module.context
    parser = ExpressionParser(module, context)
    return parser.visit(expression)


# noinspection PyPep8Naming,PyMethodMayBeStatic
class ExpressionParser(ast.NodeVisitor):
    FLOAT = TypeDB.get_type_by_name('float')
    INT = TypeDB.get_type_by_name('int')
    STR = TypeDB.get_type_by_name('str')
    BOOL = TypeDB.get_type_by_name('bool')
    NUMERIC_TYPES = (INT, FLOAT)
    CONSTANTS_MAP = {
        True: "true",
        False: "false",
        None: "null"
    }

    def __init__(self, module: "ModuleParser", context: "Context"):
        self.module = module
        self.context = context
        self.funcs = module.funcs

    def visit_Num(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.n), code=str(node.n))

    def visit_Str(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.s), code='"' + node.s + '"')

    def visit_Bytes(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.s), code='"' + str(node.s, 'utf-8') + '"')

    def visit_Name(self, node):
        if node.id in self.context:
            return self.context[node.id]
        else:
            raise exceptions.TranslationError(f"Unknown Variable: {node.id}")

    def visit_NameConstant(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.value), code=self.CONSTANTS_MAP[node.value])

    def visit_List(self, node):
        types_and_codes = [self.visit(n) for n in node.elts]
        tp = TypeDB.get_list([t.tp for t in types_and_codes])
        code = tp.as_literal([t.code for t in types_and_codes])
        return Code(tp=tp, code=code)

    # not yet implemented
    # def visit_Tuple(self, node):
    #     items = self.get_sequence_items(node.elts)
    #     return itypes.create_tuple(*items)
    #
    # def visit_Set(self, node):
    #     items = self.get_sequence_items(node.elts)
    #     return itypes.create_set(*items)
    #
    # def get_sequence_items(self, node_list):
    #     items = []
    #     for node in node_list:
    #         if utils.is_ast_starred(node):
    #             node_type = self.get_type(node.value)
    #             items.extend(node_type.get_star_expansion())
    #         else:
    #             items.append(self.get_type(node))
    #     return items
    #
    # def visit_Dict(self, node):
    #     keys = [self.get_type(key) for key in node.keys]
    #     items = [self.get_type(value) for value in node.values]
    #     return itypes.create_dict(keys, items)

    def visit_Call(self, node):
        args = [self.visit(n) for n in node.args]
        args_code = [x.code for x in args]
        if isinstance(node.func, ast.Name):
            name = node.func.id
            typesig = tuple([x.tp for x in args])
            func_type = self.funcs.get_func(name, typesig)
            func_name = self.funcs.get_func_name(name, typesig)
        elif isinstance(node.func, ast.Attribute):
            func = self.visit(node.func.value)
            func_type = func.tp.get_method(node.func.attr)
            return func_type.get_code(func, *args)
        else:
            raise UnimplementedFeature("running function from subscripted arg??")
        if func_type is None:
            raise exceptions.IdentifierNotFound(node.func)
        return Code(tp=func_type.retval.tp, code=f"{func_name}({', '.join(args_code)})")

    # def visit_Lambda(self, node):
    #     arg_names = [arg.arg for arg in node.args.args]
    #     docstring = "Anonymous lambda function"
    #     return itypes.FunctionType('__lambda__', arg_names, self.get_type(node.body), docstring)
    #
    def visit_Attribute(self, node):
        value = self.visit(node.value)
        code = f"{value.as_accessor()}{node.attr}"
        return Code(tp=value.tp.get_attr(node.attr), code=code)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Module(self, node):
        return self.visit(node.body[0])

    def visit_IfExp(self, node):
        test, body, orelse = [self.visit(x) for x in (node.test, node.body, node.orelse)]
        code = "%s ? %s : %s" % (test.code, body.code, orelse.code)
        return Code(tp=itypes.combine_types(body.tp, orelse.tp), code=code)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.get_binary_op_code(left, node.op, right)
        return result

    def get_binary_op_code(self, left, op, right):
        method_name = OPS_MAP[op.__class__]
        try:
            func = left.tp.get_method(method_name)
            result = func.get_code(left, right)
        except (StaticTypeError, InvalidOperation):
            try:
                func = right.tp.get_method(method_name)  # ok try using right as function origin...
                result = func.get_code(left, right)
            except (StaticTypeError, InvalidOperation):
                operation = op.__class__.__name__
                raise StaticTypeError(f"Arguments {left.tp}, {right.tp} not valid for operation {operation}")
        return result

    # def visit_UnaryOp(self, node):
    #     op = type(node.op).__name__
    #     if op == "Not":
    #         return self.BOOL
    #     if op == "Invert":
    #         return self.INT
    #     if op in ("UAdd", "USub"):
    #         result = itypes.TypeSet()
    #         for operand in self.evaluate(node.operand):
    #             if operand in self.NUMERIC_TYPES:
    #                 result = result.add_type(operand)
    #             else:
    #                 result = result.add_type(self.INT)
    #         return result
    #
    # def visit_BoolOp(self, node):
    #     return self.BOOL
    #
    def visit_Subscript(self, node):
        value = self.visit(node.value)
        slice_type = type(node.slice).__name__
        if slice_type == "Index":
            index = self.visit(node.slice.value)
            accessor = value.tp.get_method("get_item")
            return accessor.get_code(value, index)
        else:
            raise UnimplementedFeature("Slices not yet implemented")

    def visit_Compare(self, node: ast.AST):
        if len(node.ops) > 1:
            raise UnimplementedFeature("Multiple comparisons not yet implemented", node)
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        return self.get_binary_op_code(left, node.ops[0], right)

    # def visit_ListComp(self, node):
    #     scope = self.get_scope_for_comprehension(node)
    #     target = get_expression_type(node.elt, scope)
    #     return itypes.create_list(target)
    #
    # def visit_SetComp(self, node):
    #     scope = self.get_scope_for_comprehension(node)
    #     target = get_expression_type(node.elt, scope)
    #     return itypes.create_set(target)
    #
    # def visit_DictComp(self, node):
    #     scope = self.get_scope_for_comprehension(node)
    #     key_target = get_expression_type(node.key, scope)
    #     value_target = get_expression_type(node.value, scope)
    #     return itypes.create_dict([key_target], [value_target])
    #
    # def visit_GeneratorExp(self, node):
    #     scope = self.get_scope_for_comprehension(node)
    #     target = get_expression_type(node.elt, scope)
    #     return itypes.InferredIterator(target)
    #
    # def get_scope_for_comprehension(self, node):
    #     from .assignment import assign_to_node
    #     scope = self.scope
    #     for generator in node.generators:
    #         scope = scopes.Scope('__listcomp__', node.lineno, node.col_offset, parent=scope)
    #         iterator = get_expression_type(generator.iter, scope)
    #         assign_to_node(generator.target, iterator.get_iter(), scope)
    #     return scope

    def generic_visit(self, node):
        raise UnhandledNode(node)
