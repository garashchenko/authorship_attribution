from typed_ast import ast27, ast3

from constants import keywords_dict, keywords_dict3, terms_ast27, terms_ast3


def get_max_tree_depth(node, depth=0):
    if not hasattr(node, 'body'):
        return depth
    else:
        if isinstance(node.body, list):
            if len(node.body) == 0:
                return depth
            return max(get_max_tree_depth(n, depth + 1) for n in node.body)
        return depth + 1


def process_node_depth(node, depth_info, depth, is_ast3):
    if not hasattr(node, 'body'):
        return
    keyw_dict = keywords_dict if not is_ast3 else keywords_dict3
    keywords = [k for k in keyw_dict if k['ast_class'] == node.__class__]
    for k in keywords:
        if k['name'] and 'condition' not in k or ('condition' in k and k['condition'](node)):
            if k['name'] not in depth_info:
                depth_info[k['name']] = {'depth_sum': 1, 'node_count': 1}
            else:
                depth_info[k['name']]['depth_sum'] += depth
                depth_info[k['name']]['node_count'] += 1


def process_tree_level(level, depth_info, depth, is_ast3):
    for node in level:
        process_node_depth(node, depth_info, depth, is_ast3)
    next_level = []
    if hasattr(node, 'body'):
        if isinstance(node.body, list):
            for n in [node for node in level if hasattr(node, 'body')]:
                next_level.extend(n.body)
        else:
            next_level.append(node.body)
    return next_level


def get_compreh_count(tree, is_ast3=False):
    count = 0
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    comp = (ast27.ListComp, ast27.SetComp, ast27.DictComp) if not is_ast3 else (ast3.ListComp, ast3.SetComp, ast3.DictComp)
    for node in tree_walk:
        if node.__class__ in comp:
            count += 1
    return count


def get_slices_count(tree, is_ast3=False):
    count = 0
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    slices = ast27.Slice if not is_ast3 else ast3.Slice
    for node in tree_walk:
        if node.__class__ == slices:
            count += 1
    return count

def get_depth_info(tree, is_ast3=False):
    depth_info = {}
    depth = 0
    process_node_depth(tree, depth_info, depth, is_ast3)
    depth += 1
    level = tree.body
    while len(level) > 0:
        level = process_tree_level(level, depth_info, depth, is_ast3)
        depth += 1
    return depth_info


def get_avg_depth(depth_info, is_ast3):
    avg_depth = []
    keyw_dict = keywords_dict if not is_ast3 else keywords_dict3
    for k in keyw_dict:
        if k['name'] in depth_info:
            avg_depth.append(depth_info[k['name']]['depth_sum']/depth_info[k['name']]['node_count'])
        else:
            avg_depth.append(0)
    return avg_depth


def get_term_frequency(tree, is_ast3=False):
    tf_info = {}
    total_count = 0
    term_dict = terms_ast27 if not is_ast3 else terms_ast3
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for term in term_dict:
        tf_info[term] = 0
    for node in tree_walk:
        # if not hasattr(node, 'body') or len(node.body) == 0:
        #    continue
        if node.__class__ in term_dict:
            total_count += 1
            tf_info[node.__class__] += 1

    tf_info = {k: v / total_count for k, v in tf_info.items()}
    return list(tf_info.values())


def get_keywords_count(tree, is_ast3=False):
    keywords_count = {}
    keyw_dict = keywords_dict if not is_ast3 else keywords_dict3
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for node in tree_walk:
        keywords = [k for k in keyw_dict if k['ast_class'] == node.__class__]
        for k in keywords:
            if k['name'] and 'condition' not in k or ('condition' in k and k['condition'](node)):
                if k['name'] not in keywords_count:
                    keywords_count[k['name']] = 1
                else:
                    keywords_count[k['name']] += 1

    result = []
    for k in keyw_dict:
        if k['name'] in keywords_count:
            result.append(keywords_count[k['name']])
        else:
            result.append(0)

    return result
