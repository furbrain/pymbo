# noinspection PyStatementEffect
{
    "def": """
            typedef struct {{
                int len;
                {self.tp.c_type} items[{self.maxlen}];
            }} {self.c_type}; 
    """,
    "methods": {
        "get_item": {
            "args": "{self}, int",
            "arg_names": "lst, index",
            "retval": "{self.tp}",
            "imp": """
                if (index < lst->len) {{
                    return lst->items[index];
                }} else {{
                    //raise error here
                }}
            """,
        },
        "set_item": {
            "style": "method",
            "args": "{self}, int, {self.tp}",
            "arg_names": "lst, index, value",
            "retval": "None",
            "imp": """
                if (index < lst->len) {{
                    lst->items[index] = value;
                }} else {{
                    //raise error here
                }}
            """,
        },
        "append": {
            "args": "{self}, {self.tp}",
            "arg_names": "self, value",
            "retval": "None",
            "imp": """
                if (self->len < {self.maxlen}) {{
                    self->items[self->len] = value;
                    self->len++;                    
                }} else {{
                    //again raise an error here - ListFull
                }}
            """
        },
    },
    "inlines": {
        "len": {
            "args": "{self}",
            "retval": "int",
            "template": "{args[0].as_accessor()}len"
        }
    }
}
