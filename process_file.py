import csv
import os
from collections import namedtuple

import numpy
from sklearn import learning_curve
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from typed_ast import ast27, ast3

from features.layout import get_tabs_ratio, get_spaces_ratio, get_empty_lines_ratio, get_whitespaces_ratio
from features.lexical import count_comments, get_literals_count, get_unique_keywords, get_functions_info, \
    get_branching_factor, get_func_args_avg, get_func_args_std, get_line_lengths, get_avg_line_len, get_std_line_len
from features.syntactic import get_max_tree_depth, get_avg_depth, get_depth_info, get_keywords_count, get_slices_count, \
    get_compreh_count, get_term_frequency


def process_file(filename):
    result = []
    # layout features
    result.append(get_tabs_ratio(filename))
    result.append(get_spaces_ratio(filename))
    result.append(get_empty_lines_ratio(filename))
    result.append(get_whitespaces_ratio(filename))
    # lexical features
    with open(filename, encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
        f.seek(0)
        file_content = f.read()
        is_ast3 = False
        try:
            tree = ast27.parse(file_content)
        except Exception as ex:
            try:
                tree = ast3.parse(file_content)
                is_ast3 = True
            except SyntaxError as se:
                print(se.args)
                return

        comments_info = count_comments(f)
        function_info = get_functions_info(tree, is_ast3)
        line_lengths = get_line_lengths(f)

        result.append(comments_info.string / line_count)
        result.append(comments_info.multiline / line_count)
        result.append(get_literals_count(tree, is_ast3) / line_count)
        result.append(len(get_unique_keywords(tree, is_ast3)) / line_count)
        result.append(function_info.func_count / line_count)
        result.append(get_branching_factor(tree, is_ast3))
        result.append(get_func_args_avg(function_info.args_count))
        result.append(get_func_args_std(function_info.args_count))
        result.append(get_avg_line_len(line_lengths))
        result.append(get_std_line_len(line_lengths))

        # # syntactic features
        result.append(get_slices_count(tree, is_ast3) / line_count)
        result.append(get_compreh_count(tree, is_ast3) / line_count)
        result.append(get_max_tree_depth(tree))
        result.extend(get_avg_depth(get_depth_info(tree, is_ast3), is_ast3))  # list
        result.extend([k / line_count for k in get_keywords_count(tree, is_ast3)])  # list
        result.extend(get_term_frequency(tree, is_ast3))

    return result


def process_users():
    users = os.listdir('users')
    os.chdir('users')
    training_data = []
    training_targets = []
    test_data = []
    test_targets = []
    for user in users:
        contents = os.listdir("%s" % user)
        if len(contents) < 15:
            continue
        print(user)
        test_share = int(len(contents) * 0.2)
        for c in contents[:-test_share]:
            try:
                processed_code = process_file('%s/%s' % (user, c))
                if processed_code:
                    training_data.append(processed_code)
                    training_targets.append(user)
            except Exception as ex:
                print(ex.args)
                print('Error occured for user %s in file %s' % (user, c))
        for c in contents[-test_share:]:
            try:
                processed_code = process_file('%s/%s' % (user, c))
                if processed_code:
                    test_data.append(processed_code)
                    test_targets.append(user)
            except Exception as ex:
                print(ex.args)
                print('Error occured for user %s in file %s' % (user, c))

    return numpy.array(training_data), numpy.array(training_targets), numpy.array(test_data), numpy.array(test_targets)


def save_data():
    training_data, training_targets, test_data, test_targets = process_users()

    os.chdir('..')

    with open("training_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(training_data)

    with open("training_targets.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(training_targets)

    with open("test_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(test_data)

    with open("test_targets.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(test_targets)


def restore_data():
    training_data = []
    training_targets = []
    test_data = []
    test_targets = []
    with open('training_data.csv', newline='', encoding='utf_8') as f:
        reader = csv.reader(f)
        training_data = list(reader)
    with open('training_targets.csv', newline='', encoding='utf_8') as f:
        reader = csv.reader(f)
        training_targets = list(reader)
    with open('test_data.csv', newline='', encoding='utf_8') as f:
        reader = csv.reader(f)
        test_data = list(reader)
    with open('test_targets.csv', newline='', encoding='utf_8') as f:
        reader = csv.reader(f)
        test_targets = list(reader)
    training_data = numpy.array(training_data).astype(numpy.float)
    training_targets = numpy.array(training_targets).ravel()
    test_data = numpy.array(test_data).astype(numpy.float)
    test_targets = numpy.array(test_targets).ravel()
    return training_data, training_targets, test_data, test_targets


save_data()
X_train, y_train, X_test, y_test = restore_data()
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

clf = MLPClassifier(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
                    beta_2=0.999, early_stopping=False, epsilon=1e-06,
                    hidden_layer_sizes=(850, 850), learning_rate='constant',
                    learning_rate_init=0.001, max_iter=6000, momentum=0.9,
                    nesterovs_momentum=True, power_t=0.5, random_state=1,
                    shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
                    verbose=10, warm_start=False)

history = clf.fit(X_train, y_train)
print(history.loss)
print("Training set score: %f" % clf.score(X_train, y_train))
print("Test set score: %f" % clf.score(X_test, y_test))

# Make a prediction
print("Making predictions...")
y_pred = clf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred)
print(acc_rf)

