import itertools

import numpy
from typed_ast import ast27, ast3

from constants import keywords_dict, keywords_dict3, terms_ast27, terms_ast3


def get_max_tree_depth(node, depth=0):
    if not hasattr(node, 'body'):
        return depth
    else:
        if hasattr(node, 'body'):
            if isinstance(node.body, list):
                if len(node.body) == 0:
                    return depth
                return max(get_max_tree_depth(n, depth + 1) for n in node.body)
        return depth + 1


def process_node_depth(node, depth_info, depth):
    if node.__class__ in depth_info:
        if depth > depth_info[node.__class__]['max_depth']:
            depth_info[node.__class__]['max_depth'] = depth
        depth_info[node.__class__]['depth_sum'] += depth
        depth_info[node.__class__]['node_count'] += 1


def process_tree_level(level, depth_info, depth, is_ast3):
    if isinstance(level, list):
        for node in level:
            process_node_depth(node, depth_info, depth)
    next_level = []
    if hasattr(node, 'body'):
        if isinstance(node.body, list):
            for n in [node for node in level if hasattr(node, 'body')]:
                node_list = n.body
                if not isinstance(node_list, list):
                    node_list = [n.body]
                next_level.extend(node_list)
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
    term_dict = terms_ast27 if not is_ast3 else terms_ast3
    for term in term_dict:
        depth_info[term] = {}
        depth_info[term]['depth_sum'] = 0
        depth_info[term]['node_count'] = 0
        depth_info[term]['max_depth'] = 0
    depth = 0
    process_node_depth(tree, depth_info, depth)
    depth += 1
    level = tree.body
    while len(level) > 0:
        level = process_tree_level(level, depth_info, depth, is_ast3)
        depth += 1
    return depth_info


def get_avg_depth(depth_info, is_ast3):
    avg_depth = []
    for key, info in depth_info.items():
        if info['node_count'] > 0:
            avg_depth.append(info['depth_sum'] / info['node_count'])
        else:
            avg_depth.append(0)
    return avg_depth


def get_max_depths(depth_info):
    max_depths = []
    for key, info in depth_info.items():
        max_depths.append(info['max_depth'])
    return max_depths



def get_term_frequency(tree, is_ast3=False):
    tf_info = {}
    idf_info = {}
    total_count = 0
    term_dict = terms_ast27 if not is_ast3 else terms_ast3
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for term in term_dict:
        tf_info[term] = 0
        idf_info[term] = 0
    for node in tree_walk:
        # if not hasattr(node, 'body'):
        #     continue
        if node.__class__ in term_dict:
            total_count += 1
            tf_info[node.__class__] += 1
            idf_info[node.__class__] = 1

    if total_count > 0:
        tf_info = {k: v / total_count for k, v in tf_info.items()}

    return list(tf_info.values()), list(idf_info.values())


def get_keywords_count(tree, is_ast3=False):
    keywords_count = {}
    keyw_dict = keywords_dict if not is_ast3 else keywords_dict3
    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for node in tree_walk:
        keyword_nodes = [k for k in keyw_dict if k['ast_class'] == node.__class__]
        for k in keyword_nodes:
            if 'condition' not in k or k['condition'](node):
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


def get_bigrams_freq(tree, is_ast3=False):
    terms_combo = list(itertools.product(terms_ast27, repeat=2)) if not is_ast3 else list(itertools.product(terms_ast3, repeat=2))
    bigram_count = {}
    total_count = 0
    for terms in terms_combo:
        bigram_count[terms] = 0

    tree_walk = ast27.walk(tree) if not is_ast3 else ast3.walk(tree)
    for node in tree_walk:
        if hasattr(node, 'body'):
            try:
                if isinstance(node.body, list):
                    for n in node.body:
                        class_tuple = (node.__class__, n.__class__)
                        total_count += 1
                        bigram_count[class_tuple] += 1
                else:
                    class_tuple = (node.__class__, node.body.__class__)
                    total_count += 1
                    bigram_count[class_tuple] += 1
            except KeyError:
                continue
        elif hasattr(node, 'value'):
            try:
                if isinstance(node.value, list):
                    for n in node.value:
                        class_tuple = (node.__class__, n.__class__)
                        total_count += 1
                        bigram_count[class_tuple] += 1
                else:
                    class_tuple = (node.__class__, node.value.__class__)
                    total_count += 1
                    bigram_count[class_tuple] += 1
            except KeyError:
                continue


    if total_count > 0:
        bigram_count = {k: v / total_count for k, v in bigram_count.items()}

    return list(bigram_count.values())


def count_tfidf(documents_count, data):
    idfs = numpy.array([d['idf'] for d in data])
    idfs = numpy.sum(idfs, 0)
    idfs = numpy.log10(float(documents_count) / idfs)
    for d in data:
        tfs = numpy.array(d['tf'])
        tfidfs = tfs * idfs
        tfidfs[numpy.isnan(tfidfs)] = 0
        d['metrics'].extend(list(tfidfs))
    return data

