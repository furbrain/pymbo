from typing import List, Set, Union

import typed_ast.ast3 as ast
from typed_ast.ast3 import NodeVisitor

import exceptions
import itypes
from context import Context, Code
from exceptions import UnhandledNode, UnimplementedFeature, StaticTypeError, InvalidOperation, UnknownVariable
from itypes.functions import InlineCMethod, MultiFunction
from itypes.typedb import TypeDB
from parser.binops import OPS_MAP


def get_expression_code(expression, context: Context):
    if isinstance(expression, str):
        expression = ast.parse(expression)
    parser = ExpressionParser(context)
    code = parser.visit(expression)
    code.libraries = parser.libraries
    return code, parser.prepends


def get_constant_code(expression, context: Context) -> Code:
    if isinstance(expression, str):
        expression = ast.parse(expression)
    parser = ConstantParser(context)
    return parser.visit(expression)


# noinspection PyPep8Naming,PyMethodMayBeStatic
class ExpressionBaseParser(NodeVisitor):
    CONSTANTS_MAP = {
        True: "true",
        False: "false",
        None: "null"
    }

    # BOOL = TypeDB.get_type_by_name('bool')
    # STR = TypeDB.get_type_by_name('str')
    # INT = TypeDB.get_type_by_name('int')
    # FLOAT = TypeDB.get_type_by_name('float')
    # NUMERIC_TYPES = (INT, FLOAT)

    def __init__(self, context: "Context"):
        self.context = context
        self.prepends: List[Union[str, ast.AST]] = []
        self.libraries: Set[str] = set()

    def visit_Num(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.n), code=str(node.n))

    def visit_Str(self, node):
        tp = TypeDB.get_string()
        return Code(tp=tp, code=tp.as_literal(node.s))

    def visit_Bytes(self, node):
        tp = TypeDB.get_string()
        return Code(tp=tp, code=tp.as_literal(str(node.s, 'utf-8')))

    def visit_NameConstant(self, node):
        return Code(tp=TypeDB.get_type_by_value(node.value), code=self.CONSTANTS_MAP[node.value])

    def visit_List(self, node):
        types_and_codes = [self.visit(n) for n in node.elts]
        tp = TypeDB.get_list([t.tp for t in types_and_codes])
        code = tp.as_literal([t.code for t in types_and_codes])
        return Code(tp=tp, code=code)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def generic_visit(self, node):
        raise UnhandledNode(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.get_binary_op_code(left, node.op, right)
        return result

    def get_binary_op_code(self, left: Code, op: ast.AST, right: Code):  # pragma: no cover
        raise NotImplementedError


# noinspection PyPep8Naming,PyMethodMayBeStatic
class ExpressionParser(ExpressionBaseParser):

    def visit(self, node):
        result = super().visit(node)
        self.libraries.update(result.libraries)
        return result

    def visit_Name(self, node):
        try:
            return self.context[node.id]
        except KeyError:
            raise exceptions.UnknownVariable(f"Unknown Variable: {node.id}")

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
        if isinstance(node.func, ast.Name):
            try:
                func_type = self.visit(node.func).tp
            except UnknownVariable:
                raise exceptions.IdentifierNotFound(node.func)
        elif isinstance(node.func, ast.Attribute):
            func = self.visit(node.func.value)
            func_type = func.tp.get_method(node.func.attr)
            args = [func] + args
        else:
            raise UnimplementedFeature("running function from subscripted arg??")
        return self.call_function(func_type, *args)

    def call_function(self, func_type, *args):
        args = list(args)
        if isinstance(func_type, MultiFunction):
            func_type = func_type.get_fixed_function(*args)
        if not func_type.retval.pass_by_value:
            tmp = self.context.get_temp_var(func_type.retval)
            args.append(tmp)
            self.prepends.append(f"{func_type.get_code(self.context, *args).code};\n")
            return tmp
        else:
            return func_type.get_code(self.context, *args)

    # def visit_Lambda(self, node):
    #     arg_names = [arg.arg for arg in node.args.args]
    #     docstring = "Anonymous lambda function"
    #     return itypes.FunctionType('__lambda__', arg_names, self.get_type(node.body), docstring)
    #
    def visit_Attribute(self, node):
        value = self.visit(node.value)
        return value.tp.get_attr_code(node.attr, value)

    def visit_Module(self, node):
        return self.visit(node.body[0])

    def visit_IfExp(self, node):
        test, body, orelse = [self.visit(x) for x in (node.test, node.body, node.orelse)]
        code = "%s ? %s : %s" % (test.code, body.code, orelse.code)
        return Code(tp=itypes.combine_types(body.tp, orelse.tp), code=code)

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
            return self.call_function(accessor, value, index)
        else:
            raise UnimplementedFeature("Slices not yet implemented")

    def visit_Compare(self, node: ast.AST):
        if len(node.ops) > 1:
            raise UnimplementedFeature("Multiple comparisons not yet implemented", node)
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        return self.get_binary_op_code(left, node.ops[0], right)

    def visit_ListComp(self, node):
        from parser.functions import FunctionImplementation

        # calculate result type
        if len(node.generators) > 1:
            raise InvalidOperation("Only one for statement permitted in comprehensions")
        comp = node.generators[0]
        if len(comp.ifs) > 1:
            raise InvalidOperation("Only one if statement allowed in List Comprehension")
        assign_node = ast.Assign(targets=[comp.target],
                                 value=ast.Subscript(value=comp.iter,
                                                     slice=ast.Index(ast.Num(0))))
        return_node = ast.Return(value=node.elt)
        function_node = ast.FunctionDef(name="temp",
                                        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[],
                                                           kwarg=None, defaults=[]),
                                        body=[assign_node, return_node])
        function_interpreter = FunctionImplementation(function_node, (), self.context)
        result_type = TypeDB.get_list([function_interpreter.retval.tp])

        # create temp list to hold values
        result = self.context.get_temp_var(result_type)
        self.prepends.append(f"{result.code} = {result_type.as_literal([])};\n")
        # create for expression
        append_node = ast.Expr(ast.Call(func=ast.Attribute(value=ast.Name(id=result.code, ctx=ast.Load()),
                                                           attr="append",
                                                           ctx=ast.Load()),
                                        args=[node.elt],
                                        keywords=[]))
        if comp.ifs:
            body = ast.If(test=comp.ifs[0], body=[append_node], orelse=[])
        else:
            body = append_node
        for_node = ast.For(target=comp.target, iter=comp.iter, body=[body], orelse=[])
        self.prepends.append(for_node)
        return result

    def get_binary_op_code(self, left, op, right):
        method_name = OPS_MAP[op.__class__]
        try:
            func = left.tp.get_method(method_name)
            result = func.get_code(self.context, left, right)
        except (StaticTypeError, InvalidOperation):
            try:
                func = right.tp.get_method(method_name)  # ok try using right as function origin...
                result = func.get_code(self.context, left, right)
            except (StaticTypeError, InvalidOperation):
                operation = op.__class__.__name__
                raise StaticTypeError(f"Arguments {left.tp}, {right.tp} not valid for operation {operation}")
        return result


# noinspection PyPep8Naming,PyMethodMayBeStatic
class ConstantParser(ExpressionBaseParser):

    def get_binary_op_code(self, left: Code, op: ast.AST, right: Code):
        method_name = OPS_MAP[op.__class__]
        operation = op.__class__.__name__
        try:
            func = left.tp.get_method(method_name)
            if not isinstance(func, InlineCMethod):
                raise StaticTypeError(f"Can't use {operation} at module level")
            result = func.get_code(self.context, left, right)
        except (StaticTypeError, InvalidOperation):
            try:
                func = right.tp.get_method(method_name)  # ok try using right as function origin...
                if not isinstance(func, InlineCMethod):
                    raise StaticTypeError(f"Can't use {operation} at module level")
                result = func.get_code(self.context, left, right)
            except (StaticTypeError, InvalidOperation):
                raise StaticTypeError(f"Arguments {left.tp}, {right.tp} not valid for operation {operation}")
        return result

    def generic_visit(self, node):
        raise StaticTypeError(f"{node.__class__.__name__} not permitted in global definition")
