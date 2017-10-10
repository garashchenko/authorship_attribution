import re
from typed_ast import ast27
import numpy
from collections import namedtuple

from constants import keywords_dict


def get_unique_keywords(filename):
    unique_keywords = []
    with open(filename) as f:
        content = f.read()
        tree = ast27.parse(content)
        print(ast27.dump(tree))
        for node in ast27.walk(tree):
            keywords = [k for k in keywords_dict if k['ast_class'] == node.__class__]
            for k in (k for k in keywords if k['name'] not in unique_keywords):
                if 'condition' not in k and k['name']:
                    unique_keywords.append(k['name'])
                elif k['condition'](node) and k['name']:
                    unique_keywords.append(k['name'])
    return unique_keywords


def get_keywords_count(filename):
    keywords_count = {}
    with open(filename) as f:
        content = f.read()
        tree = ast27.parse(content)
        print(ast27.dump(tree))
        for node in ast27.walk(tree):
            keywords = [k for k in keywords_dict if k['ast_class'] == node.__class__]
            for k in keywords:
                if k['name'] and 'condition' not in k or ('condition' in k and k['condition'](node)):
                    if k['name'] not in keywords_count:
                        keywords_count[k['name']] = 1
                    else:
                        keywords_count[k['name']] += 1

    return keywords_count


def count_comments(filename):
    with open(filename) as f:
        comment_count = 0
        multiline_count = 0

        is_string = False
        is_multiline = False
        string_delim = ''

        for line in f:

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


def get_functions_info(filename):
    with open(filename) as f:
        content = f.read()
        tree = ast27.parse(content)
        print(ast27.dump(tree))
        args_count = []
        funcs_count = 0
        for node in ast27.walk(tree):
            if isinstance(node, ast27.FunctionDef):
                funcs_count += 1
                args_count.append(len(node.args.args))
                print(node.name, len(node.args.args))
        FunctionsInfo = namedtuple('FunctionsInfo', 'func_count args_count')
        return FunctionsInfo(func_count=funcs_count, args_count=args_count)


def get_func_args_avg(args_count):
    return numpy.array(args_count).mean()


def get_func_args_std(args_count):
    return numpy.array(args_count).std()


def get_literals_count(filename):
    with open(filename) as f:
        content = f.read()
        tree = ast27.parse(content)
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


def get_line_lengths(filename):
    line_lengths = []
    with open(filename) as f:
        for line in f:
            line_lengths.append(len(line))
    return line_lengths


def get_avg_line_len(line_lengths):
    return numpy.array(line_lengths).mean()


def get_std_line_len(line_lengths):
    return numpy.array(line_lengths).std()


def get_tree_depth(node, depth=0):
    if not hasattr(node, 'body') or len(node.body) == 0:
        return depth
    else:
        return max(get_tree_depth(n, depth+1) for n in node.body)

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


with open('test2.py') as f:
        content = f.read()
        tree = ast27.parse(content)
        print(ast27.dump(tree))
        print(get_tree_depth(tree))
        print(get_branching_factor(tree))

print(get_literals_count('test2.py'))
print(get_keywords_count('test2.py'))
