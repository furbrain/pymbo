from parser.module import ModuleParser


def convert(code: str) -> str:
    p = ModuleParser()
    p.parse_string(code)
    return p.wrap_exception(p.create_code, include_type_funcs=True)

