import numpy

from typed_ast import ast27, ast3
from collections import namedtuple

from constants import keywords_dict, keywords_dict3


def count_comments(file_lines):

    comment_count = 0
    multiline_count = 0
    is_string = False
    is_multiline = False
    string_delim = ''

    for line in file_lines:

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


def get_literals_count(tree, is_ast3=False):
    literals_count = 0
    is_literal = lambda node: isinstance(node, ast27.Str) or isinstance(node, ast27.Num) \
                              or isinstance(node, ast27.List) \
                              or isinstance(node, ast27.Dict) or isinstance(node, ast27.Tuple) \
                              or isinstance(node, ast27.Set)

    is_literal3 = lambda node: isinstance(node, ast3.Str) or isinstance(node, ast3.Num) \
                               or isinstance(node, ast3.List) \
                               or isinstance(node, ast3.Dict) or isinstance(node, ast3.Tuple) \
                               or isinstance(node, ast3.Set)

    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    check_literal = is_literal if not is_ast3 else is_literal3
    for node in tree_walk:
        if check_literal(node):
            literals_count += 1
    return literals_count


def get_unique_keywords(tree, is_ast3=False):
    unique_keywords = []
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    keyw_dict = keywords_dict if not is_ast3 else keywords_dict3
    for node in tree_walk:
        keywords = [k for k in keyw_dict if k['ast_class'] == node.__class__]
        for k in (k for k in keywords if k['name'] not in unique_keywords):
            if 'condition' not in k and k['name']:
                unique_keywords.append(k['name'])
            elif k['condition'](node) and k['name']:
                unique_keywords.append(k['name'])
    return unique_keywords


def get_functions_info(tree, is_ast3=False):
    args_count = []
    name_lengths = []
    funcs_count = 0
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    func_def = ast27.FunctionDef if not is_ast3 else ast3.FunctionDef
    for node in tree_walk:
        if isinstance(node, func_def):
            funcs_count += 1
            args_count.append(len(node.args.args))
            name_lengths.append(len(node.name))
    FunctionsInfo = namedtuple('FunctionsInfo', 'func_count args_count name_lengths')
    return FunctionsInfo(func_count=funcs_count, args_count=args_count, name_lengths=name_lengths)


def get_branching_factor(tree, is_ast3=False):
    child_count = 0
    nodes_count = 0
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for node in tree_walk:
        has_children = False
        child_nodes = ast27.iter_child_nodes(node) if not is_ast3 else ast3.iter_child_nodes(node)
        for n in child_nodes:
            has_children = True
            child_count += 1
        if has_children:
            nodes_count += 1
    return child_count / nodes_count if nodes_count > 0 else 1


def get_func_args_avg(args_count):
    return numpy.array(args_count).mean() if len(args_count) > 0 else 0


def get_func_args_std(args_count):
    return numpy.array(args_count).std() if len(args_count) > 0 else 0


def get_line_lengths(file_lines):
    line_lengths = []
    for line in file_lines:
        line_lengths.append(len(line))
    return line_lengths


def get_names_lengths(tree, is_ast3=False):
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    result = []
    for node in tree_walk:
        if hasattr(node, 'id'):
            result.append(len(node.id))
    return result


def get_avg_line_len(line_lengths):
    return numpy.array(line_lengths).mean()


def get_std_line_len(line_lengths):
    return numpy.array(line_lengths).std()


def get_avg_function_name_length(name_lengths):
    return numpy.array(name_lengths).mean() if len(name_lengths) > 0 else 0


def get_std_function_name_length(name_lengths):
    return numpy.array(name_lengths).std() if len(name_lengths) > 0 else 0


def get_avg_name_lengths(name_lengths):
    return numpy.array(name_lengths).mean() if len(name_lengths) > 0 else 0


def get_std_name_lengths(name_lengths):
    return numpy.array(name_lengths).std() if len(name_lengths) > 0 else 0
