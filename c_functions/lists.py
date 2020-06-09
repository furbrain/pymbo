# noinspection PyStatementEffect
{
    "def": """
            struct {self.prefix()} {{
                int len;
                {self.tp} items[{self.maxlen}];
            }}; 
    """,
    "methods": {
        "get_item": {
            "args": "int",
            "retval": "{self.tp}",
            "def": """
                {self.tp} {self.prefix()}__get_item(struct {self.prefix()} *lst, int index);
            """,
            "imp": """
                {self.tp} {self.prefix()}__get_item(struct {self.prefix()} *lst, int index) {{
                    if (index < lst->len) {{
                        return lst->items[index];
                    }} else {{
                        //raise error here
                    }}
                }}
            """,
        },
        "set_item": {
            "style": "method",
            "args": "int, {self.tp}",
            "retval": "None",
            "def": """
                void {self.prefix()}__set_item(struct {self.prefix()} *lst, int index, {self.tp} value);
            """,
            "imp": """
                void {self.prefix()}__set_item(struct {self.prefix()} *lst, int index, {self.tp} value) {{
                    if (index < lst->len) {{
                        lst->items[index] = value;
                    }} else {{
                        //raise error here
                    }}
                }}
            """,
        },
        "append": {
            "args": "{self.tp}",
            "retval": "None",
            "def": """
                void {self.prefix()}__append(struct {self.prefix()} *self, {self.tp} value);
            """,
            "imp": """
                void {self.prefix()}__append(struct {self.prefix()} *self, {self.tp} value) {{
                    if (self->len < {self.maxlen}) {{
                        self->items[self->len] = value;
                        self->len++;                    
                    }} else {{
                        //again raise an error here - ListFull
                    }}
                }}
            """
        },
    },
    "inlines": {
        "len": {
            "args": "",
            "retval": "int",
            "template": "{obj.as_accessor()}len"
        }
    }
}
