import re
from . import basics, compound

FUNC_PATTERN = r"""(?xm)
                   ^(?P<fname>\w+) [ ]*             # function name
                   \( (?P<args>.*) \)               # arguments
                   [ ]* -> [ ]*                     # arrow
                   (?P<retval>.*)\n                 # return value
                   (?P<docstring> (?:[ ]{2}.*?\n)*) # following docstring"""

ATTRIBUTE_PATTERN = r"(?m)^(?P<attrname>\w+) = (?P<value>.*)$"

def split_on(text, split):
    """return a string split on "split" characters provided they are not within brackets"""
    bracket_queue = []
    brackets = {'}': '{',
                ']': '[',
                ')': '(',
                '>': '<'}
    result = [""]
    for i, char in enumerate(text):
        if char in brackets.values():
            bracket_queue.append(char)
        if char in brackets.keys():
            if bracket_queue and brackets[char] == bracket_queue[-1]:
                bracket_queue.pop()
            else:
                raise AttributeError('Unmatched bracket')
        if char == split and len(bracket_queue) == 0:
            result.append("")
        else:
            result[-1] += char
    return result

def is_bracketed(text, brackets):
    return text[0] == brackets[0] and text[-1] == brackets[-1]

def read_type(text, scope):
    text = text.strip()
    # first split on pipes...
    pipes = split_on(text, '|')
    if len(pipes) > 1:
        subtypes = [read_type(x, scope) for x in pipes]
        return basics.TypeSet(*subtypes)
    text = pipes[0].strip()

    # return tuples
    if is_bracketed(text, '()'):
        text = text[1:-1]
        subtypes = [read_type(x, scope) for x in split_on(text, ',')]
        return compound.InferredTuple(*subtypes)

    # return lists
    if is_bracketed(text, '[]'):
        text = text[1:-1]
        return compound.InferredList(read_type(text, scope))

    # return sets/dicts
    if is_bracketed(text, '{}'):
        text = text[1:-1]
        parts = split_on(text, ':')
        if len(parts) > 1:
            return compound.InferredDict([read_type(parts[0], scope)], [read_type(parts[1], scope)])
        else:
            return compound.InferredSet(read_type(text, scope))

    type_name = '<{}>'.format(text.strip())
    if type_name in scope:
        return scope[type_name]
    elif type_name == "<Unknown>":
        return basics.UnknownType()
    else:
        raise AttributeError('Unknown builtin type {}'.format(type_name))


def read_function(matching_regex, scope):
    from . import functions
    if matching_regex.group('docstring'):
        raw_docstring = matching_regex.group('docstring')
        raw_docstring_list = [x.strip() for x in raw_docstring.splitlines()]
        docstring = '\n'.join(raw_docstring_list)
    else:
        docstring = ''
    return functions.FunctionType(name=matching_regex.group('fname'),
                                  args=[x.strip() for x in matching_regex.group('args').split(',')],
                                  returns=read_type(matching_regex.group('retval'), scope),
                                  docstring=docstring)

def read_spec(text, scope):
    funcs = [read_function(x, scope) for x in re.finditer(FUNC_PATTERN, text)]
    funcs = {x.name: x for x in funcs}
    attributes = {x[0]: read_type(x[1], scope) for x in re.findall(ATTRIBUTE_PATTERN, text)}
    attributes.update(funcs)
    return attributes
