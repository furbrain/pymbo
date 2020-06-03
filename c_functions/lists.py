# noinspection PyStatementEffect
{
    "def": """
            struct {prefix} {{
                int len;
                {tp} items[{maxlen}];
            }}; 
    """,
    "get_item": {
        "def": """
            {tp} {prefix}__get_item(struct {prefix} *lst, int index);
        """ ,
        "imp": """
            {tp} {prefix}__get_item(struct {prefix} *lst, int index) {{
                if (index < lst->len) {{
                    return lst->items[index];
                }} else {{
                    //raise error here
                }}
            }}
        """,
    },
    "set_item": {
        "def": """
            void {prefix}__set_item(struct {prefix} *lst, int index, {tp} value);
        """ ,
        "imp": """
            void {prefix}__set_item(struct {prefix} *lst, int index, {tp} value) {{
                if (index < lst->len) {{
                    lst->items[index] = value;
                }} else {{
                    //raise error here
                }}
            }}
        """,
    },
}