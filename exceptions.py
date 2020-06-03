import typed_ast.ast3 as ast
import scopes
class PymboError(Exception):
    """Base error class for Pymbo"""

class TranslationError(PymboError):
    pass

class UnhandledNode(TranslationError):
    def __init__(self, node: ast.AST) -> None:
        message = "Unhandled language feature {}".format(type(node).__name__)
        super().__init__(message)


class UnimplementedFeature(TranslationError):
    pass

class IdentifierNotFound(TranslationError):
    def __init__(self, node: ast.AST) -> None:
        message = "Identifier '{}' not found".format(node.id)
        super().__init__(message)

class InvalidOperation(TranslationError):
    pass