import typed_ast.ast3 as ast

import context

from parser.module import ModuleParser


def convert(code: str) -> str:
    tree = ast.parse(code)
    funcs = context.Context()
    p = ModuleParser(funcs = funcs)
    p.visit(tree)
    main = funcs.get_func("main", ())
    funcs.get_implementation("main", ())
    code = "\n".join(funcs.get_all_definitions())
    code += "\n"
    code += "\n\n".join(funcs.get_all_implementations())
    return code
