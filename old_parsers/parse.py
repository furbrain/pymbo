import ast
import html
from . import document, expressions

def parse_text(text, location):
    return document.Document(text, location)

def get_suggestions(document, line, line_number):
    indent = len(line) - len(line.lstrip(' '))
    scope = document.scopes.get_scope(line_number, indent)
    if line:
        last_char = line[-1]
    else:
        last_char = ''
    if last_char.isidentifier() or last_char == '.':
        identifier = get_last_whole_identifier(line)
        obj, _, prefix = identifier.rpartition('.')
        if obj == '' and prefix == '':
            return []
        if obj:
            try:
                obj = expressions.get_expression_type(obj, scope)
                scope = obj.get_all_attrs()
            except SyntaxError:
                pass
        if prefix:
            return sorted((x, get_info(x, scope)) for x in scope if x.startswith(prefix))
        else:
            return sorted((x, get_info(x, scope)) for x in scope if not x.startswith('_'))
    else:
        return []


def get_last_whole_identifier(line):
    if line == '':
        return ''
    if line.endswith('.'):
        return get_last_whole_identifier(line[:-1]) + '.'
    if not (line[-1].isidentifier() or line[-1] in (']', '}', ')')):
        return ''
    for i in range(len(line)):
        try:
            result = ast.parse(line[i:], mode='eval')
        except SyntaxError:
            continue
        else:
            line = line[i:]
            body = result.body
            expr_type = type(body).__name__
            if expr_type == "BinOp":
                return get_line_part(line, body.right)
            elif expr_type == "UnaryOp":
                return get_line_part(line, body.operand)
            elif expr_type == "Compare":
                return get_line_part(line, body.comparators[-1])
            elif expr_type == "Tuple":
                return get_line_part(line, body.elts[-1])
            return line
    return ""

def get_line_part(line, node):
    line = line[node.col_offset:]
    return get_last_whole_identifier(line)

def get_info(var, scope):
    if var in scope:
        item = scope[var]
        if hasattr(item, 'docstring'):
            return "<b>{}</b>\n\n{}".format(html.escape(str(item)), html.escape(item.docstring or ''))
    return ''
