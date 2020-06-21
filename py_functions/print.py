from context import Code, Context
from itypes import TypeDB
from itypes.functions import ComputedFunction


class Print(ComputedFunction):
    def __init__(self):
        super().__init__("print", args=[], returns=TypeDB.get_type_by_value(None))

    def get_code(self, context: Context, *args: Code) -> Code:
        prepends = []
        format_strs = []
        codes = []
        for arg in args:
            if arg.tp == "int":
                format_strs.append("%d")
                codes.append(arg.code)
            elif arg.tp == "float":
                format_strs.append("%f")
                codes.append(arg.code)
            elif arg.tp.name.strip("str__"):
                format_strs.append("%s")
                codes.append(f"{arg.as_accessor()}text")

        codes = [f'"{" ".join(format_strs)}\\n"'] + codes
        return_code = Code(tp=TypeDB.get_type_by_value(None),
                           code=f"printf({', '.join(codes)})",
                           libraries=["stdio"],
                           prepends=prepends)
        return return_code
