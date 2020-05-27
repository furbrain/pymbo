import ast

class IndentGetter(ast.NodeVisitor):
    @classmethod
    def get_lines(cls, text_or_node):
        if isinstance(text_or_node,str):
            node = ast.parse(text_or_node)
        else:
            node = text_or_node
        parser = cls()
        return parser.process_text(node)

    def process_text(self, node):
        self.lines = {}
        self.visit(node)
        return sorted(list(self.lines.items()))

    def generic_visit(self, node):
        if hasattr(node, 'lineno'):
            if node.col_offset >= 0:  # docstrings have col_offset==-1 in cpython: a bug!
                if node.lineno in self.lines:
                    self.lines[node.lineno] = min(node.col_offset, self.lines[node.lineno])
                else:
                    self.lines[node.lineno] = node.col_offset
        super().generic_visit(node)            
