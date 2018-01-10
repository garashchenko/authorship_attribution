import os
from collections import namedtuple


def get_file_total_length(filename):
    return os.path.getsize(filename)


def get_file_info(filename):
    file_lines = []
    with open(filename, encoding='latin-1') as f:
        for line in f:
            file_lines.append(line)
        f.seek(0)
        file_content = f.read()

    File_Info = namedtuple('FileInfo', 'content lines')
    return File_Info(content=file_content, lines=file_lines)
