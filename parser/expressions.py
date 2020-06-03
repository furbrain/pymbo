import typed_ast.ast3 as ast
import warnings

import exceptions
from itypes import InferredType
from itypes.lister import Lister
from exceptions import UnhandledNode, UnimplementedFeature
import itypes
from typing import TYPE_CHECKING

from itypes.typedb import TypeDB

if TYPE_CHECKING:
    from parser.module import ModuleParser
    from context import Context

def get_expression_type_and_code(expression, module: "ModuleParser", context: "Context"):
    if isinstance(expression, str):
        expression = ast.parse(expression)
    parser = ExpressionParser(module, context)
    return parser.visit(expression)


class ExpressionParser(ast.NodeVisitor):
    FLOAT = itypes.get_type_by_name('<float>')
    INT = itypes.get_type_by_name('<int>')
    STR = itypes.get_type_by_name('<str>')
    BOOL = itypes.get_type_by_name('<bool>')
    NUMERIC_TYPES = (INT, FLOAT)
    CONSTANTS_MAP = {
        True: "true",
        False: "false",
        None: "null"
    }
    OPS_MAP = {
        "Add": "+",
        "Sub": "-",
        "Mult": "*",
        "Div": "/"
    }
    COMPS_MAP = {
        "Eq"   :"==",
        "NotEq":"!=",
        "Lt"   :"<",
        "LtE"  :"<=",
        "Gt"   :">",
        "GtE"  :">=",
    }

    def __init__(self, module: "ModuleParser", context: "Context"):
        self.module = module
        self.context = context
        self.funcs = module.funcs

    def as_function(self, function: InferredType, *args):
        pass

    def visit_Num(self, node):
        return itypes.get_type_by_value(node.n), str(node.n)

    def visit_Str(self, node):
        return itypes.get_type_by_value(node.s), '"' + node.s + '"'

    def visit_Bytes(self, node):
        return itypes.get_type_by_value(node.s), '"' + node.s + '"'

    def visit_Name(self, node):
        if node.id in self.context:
            return self.context[node.id].tp, node.id
        else:
            return itypes.UnknownType(), None

    def visit_NameConstant(self, node):
        return itypes.get_type_by_value(node.value), self.CONSTANTS_MAP[node.value]

    def visit_List(self, node):
        types_and_codes = [self.visit(n) for n in node.elts]
        tp = TypeDB.get_list([t[0] for t in types_and_codes])
        code = tp.as_literal([t[1] for t in types_and_codes])
        return tp, code

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
        args_code = [x[1] for x in args]
        if isinstance(node.func, ast.Name):
            name = node.func.id
            typesig = tuple([x[0] for x in args])
            func_type = self.funcs.get_func(name, typesig)
            func_name = self.funcs.get_func_name(name, typesig)
        elif isinstance(node.func, ast.Attribute):
            attr_type, code = self.visit(node.func.value)
            args_code = [code] + args_code
            func_type = attr_type.get_attr(node.func.attr)
            func_name = func_type.name
        else:
            func_name, func_type = self.visit(node.func)
        if func_type is None:
            raise exceptions.IdentifierNotFound(node.func)
        return func_type.retval, f"{func_name}({', '.join(args_code)})"

    # def visit_Lambda(self, node):
    #     arg_names = [arg.arg for arg in node.args.args]
    #     docstring = "Anonymous lambda function"
    #     return itypes.FunctionType('__lambda__', arg_names, self.get_type(node.body), docstring)
    #
    def visit_Attribute(self, node):
         attr_type, code = self.visit(node.value)
         return attr_type.get_attr(node.attr), code


    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Module(self, node):
        return self.visit(node.body[0])

    def visit_IfExp(self, node):
        test, body, orelse = [self.visit(x) for x in (node.test, node.body, node.orelse)]
        code = "%s ? %s : %s" % (test[1], body[1], orelse[1])
        return itypes.combine_types(body[0], orelse[0]), code

    def visit_BinOp(self, node):
        op = type(node.op).__name__
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.get_binary_op_type(left[0], right[0], op)
        if op in self.OPS_MAP:
            op = self.OPS_MAP[op]
        else:
            raise NotImplementedError(op)
        code = "({left} {op} {right})".format(left=left[1], op=op, right=right[1])
        return result, code

    def get_binary_op_type(self, left, right, op):
        if self.both_args_numeric(left, right):
            return itypes.combine_types(left, right)
        if left == self.STR and right == self.STR and op == "Add":
            return left
        if left == self.STR and right == self.INT and op == "Mult":
            return left
        if left == self.STR and op == "Mod":
            return left
        return TypeError

    def both_args_numeric(self, left, right):
        return left in self.NUMERIC_TYPES and right in self.NUMERIC_TYPES

    def both_args_strings(self, left, right):
        return left == self.STR and right == self.STR

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
        v_type, v_code = self.visit(node.value)
        slice_type = type(node.slice).__name__
        if slice_type == "Index":
            index = node.slice.value
            i_type, i_code = self.visit(node.slice.value)
            res_type, res_code = v_type.get_item(i_type)
            return res_type, f"{res_code}(&{v_code}, {i_code})"
        else:
            raise UnhandledNode("Slices not yet implemented")

    def visit_Compare(self, node: ast.AST):
        if len(node.ops) > 1:
            raise UnimplementedFeature("Multiple comparisons not yet implemented", node)
        op = type(node.ops[0]).__name__
        if op not in self.COMPS_MAP:
            raise UnimplementedFeature("Comparator %s not yet implemented" % op, node)
        left = self.visit(node.left)[1]
        right = self.visit(node.comparators[0])[1]

        code = "(%s %s %s)" % (left, self.COMPS_MAP[op], right)
        return self.BOOL, code

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
