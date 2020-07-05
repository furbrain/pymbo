import typed_ast.ast3 as ast

from exceptions import UnhandledNode, StaticTypeError
from itypes import TypeDB


def get_type(node: ast.AST):
    parser = AnnotationParser()
    return parser.get_type(node)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class AnnotationParser(ast.NodeVisitor):
    def get_type(self, node: ast.AST):
        return self.visit(node)

    def visit_Name(self, node: ast.Name):
        return TypeDB.get_type_by_name(node.id)

    def process_list(self, subscript: ast.AST):
        if isinstance(subscript, ast.Index):
            return TypeDB.get_list([self.visit(subscript.value)])
        elif isinstance(subscript, ast.Slice):
            if isinstance(subscript.upper, ast.Num) and isinstance(subscript.upper.n, int):
                return TypeDB.get_list([self.visit(subscript.lower)], maxlen=subscript.upper.n)
            else:
                raise StaticTypeError("List length must be integer")

    def visit_Subscript(self, node: ast.Subscript):
        if isinstance(node.value, ast.Name):
            if node.value.id == "List":
                return self.process_list(node.slice)
        raise StaticTypeError("Annotation base must be List or Dict or Tuple")

    def generic_visit(self, node):
        raise UnhandledNode(node)
