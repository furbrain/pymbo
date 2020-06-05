# noinspection PyStatementEffect
{
    "def": """
            struct {prefix} {{
                int len;
                {tp} items[{maxlen}];
            }}; 
    """,
    "methods": {
        "get_item": {
            "args": "int",
            "retval": "{tp}",
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
            "args": "int, {tp}",
            "retval": "None",
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
        "append": {
            "args": "{tp}",
            "retval": "None",
            "def": """
                void {prefix}__append(struct {prefix} *self, {tp} value);
            """,
            "imp": """
                void {prefix}__append(struct {prefix} *self, {tp} value) {{
                    if (self->len < {maxlen}) {{
                        self->items[self->len] = value;
                        self->len++;                    
                    }} else {{
                        //again raise an error here - ListFull
                    }}
                }}
            """
        }
    }
}