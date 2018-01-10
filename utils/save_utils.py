import csv
import os

import numpy


def save_data(training_data, training_targets, test_data, test_targets):

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