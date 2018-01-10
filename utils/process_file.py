import os
import random
import threading

import numpy

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from typed_ast import ast27, ast3

from features.layout import *
from features.lexical import *
from features.syntactic import *
from utils.file_utils import get_file_info, get_file_total_length

lock = threading.Lock()


def process_file(filename):
    metrics = []

    with lock:
        file_info = get_file_info(filename)
        file_total_length = get_file_total_length(filename)

    file_lines = file_info.lines
    file_content = file_info.content

    if not file_lines:
        raise Exception

    # layout features
    tabs_ratio = get_tabs_ratio(file_lines, file_total_length)
    metrics.append(tabs_ratio)

    space_ratio = get_spaces_ratio(file_lines, file_total_length)
    metrics.append(space_ratio)

    empty_lines = get_empty_lines_ratio(file_lines)
    metrics.append(empty_lines)

    whitespaces_ratio = get_whitespaces_ratio(file_lines, file_total_length)
    metrics.append(whitespaces_ratio)

    before_bracket = get_spaces_before_bracket(file_lines, file_total_length)
    metrics.append(before_bracket)

    after_bracket = get_spaces_after_bracket(file_lines, file_total_length)
    metrics.append(after_bracket)

    after_equal = get_spaces_after_equal(file_lines, file_total_length)
    metrics.append(after_equal)

    before_equal = get_spaces_before_equal(file_lines, file_total_length)
    metrics.append(before_equal)

    after_comma = get_spaces_after_comma(file_lines, file_total_length)
    metrics.append(after_comma)

    # lexical features
    line_count = len(file_lines)
    if line_count == 0:
        raise Exception

    # get tree and is_ast3
    is_ast3 = False
    try:
        tree = ast27.parse(file_content)
    except Exception as ex:
        try:
            tree = ast3.parse(file_content)
            is_ast3 = True
        except Exception as ex:
            raise ex
    # end of tree generating

    comments_info = count_comments(file_lines)
    function_info = get_functions_info(tree, is_ast3)
    line_lengths = get_line_lengths(file_lines)
    name_lengths = get_names_lengths(tree, is_ast3)

    metrics.append(comments_info.string / line_count)
    metrics.append(comments_info.multiline / line_count)

    literals_count = get_literals_count(tree, is_ast3)
    metrics.append(literals_count / line_count)
    unique_keywords = get_unique_keywords(tree, is_ast3)
    metrics.append(len(unique_keywords) / line_count)

    metrics.append(function_info.func_count / line_count)

    branching_factor = get_branching_factor(tree, is_ast3)
    metrics.append(branching_factor)

    metrics.append(get_func_args_avg(function_info.args_count))
    metrics.append(get_func_args_std(function_info.args_count))

    metrics.append(get_avg_line_len(line_lengths))
    metrics.append(get_std_line_len(line_lengths))

    metrics.append(get_avg_function_name_length(function_info.name_lengths))
    metrics.append(get_std_function_name_length(function_info.name_lengths))

    metrics.append(get_avg_name_lengths(name_lengths))
    metrics.append(get_std_name_lengths(name_lengths))

    # syntactic features
    try:
        slices_count = get_slices_count(tree, is_ast3)
        metrics.append(slices_count / line_count)
    except Exception:
        print('Slices error')
    try:
        compreh_count = get_compreh_count(tree, is_ast3)
        metrics.append(compreh_count / line_count)
    except Exception:
        print('Compreh error')
    try:
        max_tree_depth = get_max_tree_depth(tree)
        metrics.append(max_tree_depth)
    except Exception:
        print('Depth error')
    try:
        depth_info = get_depth_info(tree, is_ast3)
        avg_depth = get_avg_depth(depth_info, is_ast3)
        metrics.extend(avg_depth)  # list
    except Exception:
        print('Avg depth error')
    try:
        max_depths = get_max_depths(depth_info)
        metrics.extend(max_depths)
    except Exception:
        print('Max depths error')
    try:
        keywords_avg = [k / line_count for k in get_keywords_count(tree, is_ast3)]
        metrics.extend(keywords_avg)  # list
    except Exception:
        print('Kw count error')
    try:
        tf_freq, idf_freq = get_term_frequency(tree, is_ast3)
        metrics.extend(tf_freq)
    except Exception:
        print('TF error')
    try:
        bigram = get_bigrams_freq(tree, is_ast3)
        metrics.extend(bigram)
    except Exception as ex:
        print('Bigram error')

    return metrics, tf_freq, idf_freq


def process_single_file(user, filename, data, targets, count):
    try:
        processed_code, tf_freq, idf_freq = process_file('users/%s/%s' % (user, filename))
    except Exception as ex:
        raise ex
    if processed_code:
        data.append({'metrics': processed_code, 'tf': tf_freq, 'idf': idf_freq})
        targets.append(user)
        count += 1
    return data, targets, count


def process_users(users_amount, test_percentage=0.1, user_list=None):
    users = os.listdir('users')

    training_data = []
    training_targets = []
    test_data = []
    test_targets = []
    user_count = 0
    documents_count = 0
    test_documents_count = 0

    result_list = users[:users_amount]
    if user_list:
        result_list = user_list

    for user in result_list:
        contents = os.listdir("users/%s" % user)
        user_count += 1
        test_share = int(len(contents) * test_percentage)
        for c in contents[:-test_share]:
            try:
                training_data, training_targets, documents_count = process_single_file(user, c, training_data,
                                                                                       training_targets,
                                                                                       documents_count)
            except Exception:
                continue
        for c in contents[-test_share:]:
            try:
                test_data, test_targets, test_documents_count = process_single_file(user, c, test_data, test_targets,
                                                                                    test_documents_count)
            except Exception:
                continue

    training_data = count_tfidf(documents_count, training_data)
    test_data = count_tfidf(test_documents_count, test_data)

    training_data_metrics = []
    test_data_metrics = []

    for data in training_data:
        training_data_metrics.append(data['metrics'])

    for data in test_data:
        test_data_metrics.append(data['metrics'])

    return numpy.array(training_data_metrics), numpy.array(training_targets), numpy.array(test_data_metrics), numpy.array(test_targets)


def classify(training_data, training_targets, test_data, test_targets):

    X_train = numpy.array(training_data).astype(numpy.float)
    y_train = numpy.array(training_targets).ravel()
    X_test = numpy.array(test_data).astype(numpy.float)
    y_test = numpy.array(test_targets).ravel()

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = SGDClassifier(alpha=0.04, shuffle=True, random_state=0)
    model = SelectFromModel(clf)
    model.fit(X_train, y_train)
    X_train = model.transform(X_train)
    X_test = model.transform(X_test)

    clf = RandomForestClassifier(max_depth=24, n_estimators=1000, n_jobs=-1, random_state=1,
                                 max_features='auto', bootstrap=True, oob_score=False)
    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)
    return accuracy_score(y_test, predicted)


def classify_batch(users_amount, users):
    training_data, training_targets, test_data, test_targets = process_users(users_amount, user_list=users)
    with lock:
        with open('results.txt', 'a') as file:
            file.write('%s\n' % classify(training_data, training_targets, test_data, test_targets))


def get_accuracy_for_batches(users_amount, batch_size, tries_count):
    users = os.listdir('users')
    users = users[:users_amount]
    random_list = []
    for i in range(tries_count):
        while True:
            combination = random.sample(users, batch_size)
            if combination not in random_list:
                break
        random_list.append(combination)

    with open('results.txt', 'w') as file:
        file.write('Results: \n')

    for users in random_list:
        thread = threading.Thread(target=classify_batch, args=(users_amount, users))
        thread.start()

get_accuracy_for_batches(50, 5, 5)