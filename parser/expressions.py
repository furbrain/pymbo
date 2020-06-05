import typed_ast.ast3 as ast
import warnings

import exceptions
from itypes import InferredType
from itypes.lister import Lister
from exceptions import UnhandledNode, UnimplementedFeature
import itypes
from typing import TYPE_CHECKING
from itypes.typedb import TypeDB
from context import Context, Code

if TYPE_CHECKING:
    from parser.module import ModuleParser

def get_expression_code(expression, module: "ModuleParser", context: Context) -> Code:
    if isinstance(expression, str):
        expression = ast.parse(expression)
    parser = ExpressionParser(module, context)
    return parser.visit(expression)


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
        return Code(tp=TypeDB.get_type_by_value(node.n),code=str(node.n))

    def visit_Str(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.s), code='"' + node.s + '"')

    def visit_Bytes(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.s), code='"' + node.s + '"')

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
            args_code = [func.code] + args_code
            func_type = func.tp.get_attr(node.func.attr)
            func_name = func_type.name
        else:
            func = self.visit(node.func)
            func_type = func.tp
            func_name = func.code
        if func_type is None:
            raise exceptions.IdentifierNotFound(node.func)
        return Code(tp=func_type.retval, code=f"{func_name}({', '.join(args_code)})")

    # def visit_Lambda(self, node):
    #     arg_names = [arg.arg for arg in node.args.args]
    #     docstring = "Anonymous lambda function"
    #     return itypes.FunctionType('__lambda__', arg_names, self.get_type(node.body), docstring)
    #
    def visit_Attribute(self, node):
        value = self.visit(node.value)
        if value.is_pointer:
            code = f"{value.code}->{node.attr}"
        else:
            code = f"{value.code}.{node.attr}"
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
        op = type(node.op).__name__
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.get_binary_op_type(left.tp, right.tp, op)
        if op in self.OPS_MAP:
            op = self.OPS_MAP[op]
        else:
            raise NotImplementedError(op)
        code = "({left} {op} {right})".format(left=left.code, op=op, right=right.code)
        return Code(tp=result, code=code)

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
        value = self.visit(node.value)
        slice_type = type(node.slice).__name__
        if slice_type == "Index":
            index = self.visit(node.slice.value)
            accessor = value.tp.get_item(index.tp)
            return Code(tp=accessor.tp, code=f"{accessor.code}({value.as_pointer().code}, {index.code})")
        else:
            raise UnhandledNode("Slices not yet implemented")

    def visit_Compare(self, node: ast.AST):
        if len(node.ops) > 1:
            raise UnimplementedFeature("Multiple comparisons not yet implemented", node)
        op = type(node.ops[0]).__name__
        if op not in self.COMPS_MAP:
            raise UnimplementedFeature("Comparator %s not yet implemented" % op, node)
        left = self.visit(node.left).code
        right = self.visit(node.comparators[0]).code

        code = "(%s %s %s)" % (left, self.COMPS_MAP[op], right)
        return Code(tp=self.BOOL, code=code)

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
