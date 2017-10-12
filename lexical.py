import numpy

from typed_ast import ast27
from collections import namedtuple

from constants import keywords_dict


def count_comments(file):
    comment_count = 0
    multiline_count = 0

    is_string = False
    is_multiline = False
    string_delim = ''

    for line in file:

        if is_multiline and line.strip()[-3:] in ("'''", '"""'):
            is_multiline = False
            continue

        if not is_multiline and line.strip(' ')[:3] in ("'''", '"""'):
            is_multiline = True
            multiline_count += 1

        if is_multiline:
            continue

        for c in line:
            if not is_string and c in ('\'', '\"'):
                string_delim = c
                is_string = True
                continue

            if is_string and c == string_delim:
                string_delim = ''
                is_string = False

            if not is_string and c == '#':
                comment_count += 1
                break

    Comments_Count = namedtuple('CommentsCount', 'string multiline')
    return Comments_Count(string=comment_count, multiline=multiline_count)


def get_literals_count(tree):
    literals_count = 0
    is_literal = lambda node:    isinstance(node, ast27.Str) or isinstance(node, ast27.Num) \
                              or isinstance(node, ast27.List) \
                              or isinstance(node, ast27.Dict) or isinstance(node, ast27.Tuple) \
                              or isinstance(node, ast27.Set)
                             #or isinstance(node, ast27.NameConstant)

    for node in ast27.walk(tree):
        if is_literal(node):
            literals_count += 1
    return literals_count


def get_unique_keywords(tree):
    unique_keywords = []
    for node in ast27.walk(tree):
        keywords = [k for k in keywords_dict if k['ast_class'] == node.__class__]
        for k in (k for k in keywords if k['name'] not in unique_keywords):
            if 'condition' not in k and k['name']:
                unique_keywords.append(k['name'])
            elif k['condition'](node) and k['name']:
                unique_keywords.append(k['name'])
    return unique_keywords


def get_functions_info(tree):
    args_count = []
    funcs_count = 0
    for node in ast27.walk(tree):
        if isinstance(node, ast27.FunctionDef):
            funcs_count += 1
            args_count.append(len(node.args.args))
            print(node.name, len(node.args.args))
    FunctionsInfo = namedtuple('FunctionsInfo', 'func_count args_count')
    return FunctionsInfo(func_count=funcs_count, args_count=args_count)


def get_branching_factor(tree):
    child_count = 0
    nodes_count = 0
    for node in ast27.walk(tree):
        has_children = False
        for n in ast27.iter_child_nodes(node):
            has_children = True
            child_count += 1
        if has_children:
            nodes_count += 1
    return child_count / nodes_count


def get_func_args_avg(args_count):
    return numpy.array(args_count).mean()


def get_func_args_std(args_count):
    return numpy.array(args_count).std()


def get_line_lengths(file):
    line_lengths = []
    for line in file:
        line_lengths.append(len(line))
    return line_lengths


def get_avg_line_len(line_lengths):
    return numpy.array(line_lengths).mean()


def get_std_line_len(line_lengths):
    return numpy.array(line_lengths).std()


with open('test2.py') as f:
        content = f.read()
        tree = ast27.parse(content)
        print(ast27.dump(tree))
        print(get_branching_factor(tree))

print(get_literals_count('test2.py'))
