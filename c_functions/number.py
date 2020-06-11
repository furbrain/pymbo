# noinspection PyStatementEffect
{
    "def": "",
    "methods": {},
    "inlines": {
        "__add__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} + {args[1].as_value()})"
        },
        "__sub__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} - {args[1].as_value()})"
        },
        "__mult__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} * {args[1].as_value()})"
        },
        "__div__": {
            "args": "{self}, {self}",
            "retval": "float",
            "template": "((float) {args[0].as_value()} / {args[1].as_value()})"
        },
        "__floordiv__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} / {args[1].as_value()})"
        },
        "__mod__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} % {args[1].as_value()})"
        },
        "__lshift__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} << {args[1].as_value()})"
        },
        "__rshift__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} >> {args[1].as_value()})"
        },
        "__bitor__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} | {args[1].as_value()})"
        },
        "__bitxor__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} ^ {args[1].as_value()})"
        },
        "__bitand__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "template": "({args[0].as_value()} & {args[1].as_value()})"
        },

    }
}
