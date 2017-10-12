from typed_ast import ast27

from constants import keywords_dict


def get_max_tree_depth(node, depth=0):
    if not hasattr(node, 'body') or len(node.body) == 0:
        return depth
    else:
        return max(get_max_tree_depth(n, depth + 1) for n in node.body)


def process_node_depth(node, depth_info, depth):
    if not hasattr(node, 'body') or len(node.body) == 0:
        return
    if node.__class__ not in depth_info:
        depth_info[node.__class__] = {'depth_sum': 1, 'node_count': 1}
    else:
        depth_info[node.__class__]['depth_sum'] += depth
        depth_info[node.__class__]['node_count'] += 1


def process_tree_level(level, depth_info, depth):
    for node in level:
        process_node_depth(node, depth_info, depth)
    next_level = []
    for n in [node for node in level if hasattr(node, 'body')]:
        next_level.extend(n.body)
    return next_level


def get_depth_info(tree):
    depth_info = {}
    depth = 0
    process_node_depth(tree, depth_info, depth)
    depth += 1
    level = tree.body
    while len(level) > 0:
        level = process_tree_level(level, depth_info, depth)
        depth += 1
    return depth_info


def get_avg_depth(depth_info):
    avg_depth = {}
    for key, value in depth_info.items():
        avg_depth[key] = value['depth_sum'] / value['node_count']
    return avg_depth


def get_term_frequency(tree):
    tf_info = {}
    total_count = 0
    for node in ast27.walk(tree):
        if not hasattr(node, 'body') or len(node.body) == 0:
            continue
        total_count += 1
        if node.__class__ not in tf_info:
            tf_info[node.__class__] = 1
        else:
            tf_info[node.__class__] += 1

    return {k: v / total_count for k, v in tf_info.items()}


def get_keywords_count(tree):
    keywords_count = {}
    for node in ast27.walk(tree):
        keywords = [k for k in keywords_dict if k['ast_class'] == node.__class__]
        for k in keywords:
            if k['name'] and 'condition' not in k or ('condition' in k and k['condition'](node)):
                if k['name'] not in keywords_count:
                    keywords_count[k['name']] = 1
                else:
                    keywords_count[k['name']] += 1

    return keywords_count


with open('test2.py') as f:
    content = f.read()
    tree = ast27.parse(content)
    print(get_term_frequency(tree))
    print(get_keywords_count(tree))
    print(get_avg_depth(get_depth_info(tree)))
