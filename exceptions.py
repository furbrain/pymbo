import typed_ast.ast3 as ast
import scopes
class PymboError(Exception):
    """Base error class for Pymbo"""

class TranslationError(PymboError):
    def __init__(self, message, node:ast.AST):
        location = "At: " + str(node.lineno)
        super().__init__(message, location)

class UnhandledNode(TranslationError):
    def __init__(self, node:ast.AST) -> None:
        message = "Unhandled language feature {}".format(type(node).__name__)
        super().__init__(message, node)


class UnimplementedFeature(TranslationError):
    pass

class FunctionNotFound(TranslationError):
    def __init__(self, node:ast.AST) -> None:
        message = "Function '{}' not found".format(node.id)
        super().__init__(message, node)
