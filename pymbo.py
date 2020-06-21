from textwrap import dedent

from parser.module import ModuleParser

INCLUDES = """
    #include <stdint.h>
    #include <stdbool.h>
    #include <string.h>
    #include "CExceptionConfig.h"
"""


def convert(code: str) -> str:
    p = ModuleParser()
    p.parse_string(code)
    return dedent(INCLUDES) + p.wrap_exception(p.create_code, include_type_funcs=True)
