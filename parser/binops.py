from typed_ast import ast3 as ast

OPS_MAP = {
    ast.Add: "__add__",
    ast.Sub: "__sub__",
    ast.Mult: "__mult__",
    ast.FloorDiv: "__floordiv__",
    ast.Div: "__div__",
    ast.Mod: "__mod__",
    ast.LShift: "__lshift__",
    ast.RShift: "__rshift__",
    ast.BitOr: "__bitor__",
    ast.BitXor: "__bitxor__",
    ast.BitAnd: "__bitand__",
    ast.And: "__and__",
    ast.Or: "__or__",
    ast.Eq: "__eq__",
    ast.NotEq: "__ne__",
    ast.Lt: "__lt__",
    ast.LtE: "__le__",
    ast.Gt: "__gt__",
    ast.GtE: "__ge__",
    ast.Is: "__is__",
    ast.IsNot: "__isnt__",
    ast.In: "__contains__",
    ast.NotIn: "__ncontains__"

}
