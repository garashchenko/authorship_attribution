import os


def get_tabs_ratio(file_lines, total_length):
    if total_length == 0:
        return 0
    tabs = 0
    for line in file_lines:
        tabs += line.count('\t')
    return tabs / total_length


def get_spaces_ratio(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count(' ')
    return spaces / total_length


def get_spaces_before_equal(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count(' =')
    return spaces / total_length


def get_spaces_after_equal(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count('= ')
    return spaces / total_length


def get_spaces_after_comma(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count(', ')
    return spaces / total_length


def get_spaces_after_bracket(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count('( ')
    return spaces / total_length


def get_spaces_before_bracket(file_lines, total_length):
    if total_length == 0:
        return 0
    spaces = 0
    for line in file_lines:
        spaces += line.count(' (')
    return spaces / total_length


def get_empty_lines_ratio(file_lines):
    total_lines = 0
    empty_lines = 0
    for line in file_lines:
        total_lines += 1
        empty_lines = empty_lines + 1 if line.isspace() else empty_lines
    return empty_lines / total_lines if total_lines > 0 else 0


def get_whitespaces_ratio(file_lines, total_length):
    whitespaces = 0
    if total_length == 0:
        return 0
    for line in file_lines:
        whitespaces += len(line) - len(''.join(line.split()))
    return whitespaces / total_length
