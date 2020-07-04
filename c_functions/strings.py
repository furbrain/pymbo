# noinspection PyStatementEffect
{
    "def": """
            typedef struct {{
                char text[{self.maxlen}];
            }} {self.c_type}; 
    """,
    "methods": {},
    "inlines": {
        "len": {
            "args": "{self}",
            "retval": "int",
            "priority": 1,
            "template": "strnlen({args[0].as_accessor()}text, {args[0].tp.maxlen})"
        },
        "__eq__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 7,
            "template": "strncmp({args[0].as_accessor()}text, {args[1].as_accessor()}text, {args[0].tp.maxlen}) == 0"
        }
    }
}
