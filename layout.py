import os
import math

def get_tabs_ratio(filename):
    total_length = os.path.getsize(filename)
    tabs = 0
    with open(filename) as f:
        for line in f:
                tabs += line.count('\t')
    return tabs / total_length


def get_spaces_ratio(filename):
    total_length = os.path.getsize(filename)
    spaces = 0
    with open(filename) as f:
        for line in f:
            spaces += line.count(' ')
    return spaces / total_length


def get_empty_lines_ratio(filename):
    total_lines = 0
    empty_lines = 0
    with open(filename) as f:
        for line in f:
            total_lines += 1
            empty_lines = empty_lines + 1 if line.isspace() else empty_lines
    return empty_lines / total_lines


def get_whitespaces_ratio(filename):
    whitespaces = 0
    total = os.path.getsize(filename)
    with open(filename) as f:
        for line in f:
            whitespaces += len(line) - len(''.join(line.split()))
    return whitespaces / total

print(get_whitespaces_ratio('test.txt'))