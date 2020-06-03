import typed_ast.ast3 as ast

import funcdb

from parser.module import ModuleParser


def convert(code: str) -> str:
    tree = ast.parse(code)
    p = ModuleParser()
    p.visit(tree)
    return p.create_code(include_type_funcs=True)

