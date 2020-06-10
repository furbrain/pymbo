# noinspection PyStatementEffect
{
    "def": "",
    "methods": {},
    "inlines": {
        "__add__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} + {args[0].as_value()})"
        },
        "__sub__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} - {args[0].as_value()})"
        },
        "__mult__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} * {args[0].as_value()})"
        },
        "__div__": {
            "args": "float",
            "retval": "float",
            "template": "((float) {obj.as_value()} / {args[0].as_value()})"
        },
        "__floordiv__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} / {args[0].as_value()})"
        },
        "__mod__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} %% {args[0].as_value()})"
        },
        "__lshift__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} << {args[0].as_value()})"
        },
        "__rshift__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} >> {args[0].as_value()})"
        },
        "__bitor__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} | {args[0].as_value()})"
        },
        "__bitxor__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} ^ {args[0].as_value()})"
        },
        "__bitand__": {
            "args": "{self}",
            "retval": "{self}",
            "template": "({obj.as_value()} & {args[0].as_value()})"
        },

    }
}
