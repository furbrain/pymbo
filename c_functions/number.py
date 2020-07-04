# use https://en.cppreference.com/w/c/language/operator_precedence for priority levels

# noinspection PyStatementEffect
{
    "def": "",
    "methods": {},
    "inlines": {
        "__add__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 4,
            "template": "{args[0].as_value()} + {args[1].as_value()}",
        },
        "__sub__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 4,
            "template": "{args[0].as_value()} - {args[1].as_value()}"
        },
        "__mult__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 3,
            "template": "{args[0].as_value()} * {args[1].as_value()}"
        },
        "__div__": {
            "args": "{self}, {self}",
            "retval": "float",
            "priority": 3,
            "template": "(float) {args[0].as_value()} / {args[1].as_value()}"
        },
        "__floordiv__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 3,
            "template": "{args[0].as_value()} / {args[1].as_value()}"
        },
        "__mod__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 3,
            "template": "{args[0].as_value()} % {args[1].as_value()}"
        },
        "__lshift__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 5,
            "template": "{args[0].as_value()} << {args[1].as_value()}"
        },
        "__rshift__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 5,
            "template": "{args[0].as_value()} >> {args[1].as_value()}"
        },
        "__bitor__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 10,
            "template": "{args[0].as_value()} | {args[1].as_value()}"
        },
        "__bitxor__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 9,
            "template": "{args[0].as_value()} ^ {args[1].as_value()}"
        },
        "__bitand__": {
            "args": "{self}, {self}",
            "retval": "{self}",
            "priority": 8,
            "template": "{args[0].as_value()} & {args[1].as_value()}"
        },
        "__eq__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 7,
            "template": "{args[0].as_value()} == {args[1].as_value()}"
        },
        "__ne__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 7,
            "template": "{args[0].as_value()} != {args[1].as_value()}"
        },
        "__lt__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 6,
            "template": "{args[0].as_value()} < {args[1].as_value()}"
        },
        "__le__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 6,
            "template": "{args[0].as_value()} <= {args[1].as_value()}"
        },
        "__gt__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 6,
            "template": "{args[0].as_value()} > {args[1].as_value()}"
        },
        "__ge__": {
            "args": "{self}, {self}",
            "retval": "bool",
            "priority": 6,
            "template": "{args[0].as_value()} >= {args[1].as_value()}"
        },

    }
}
