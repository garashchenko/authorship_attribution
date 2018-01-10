import os
import shutil
import uuid
import zipfile
# Распаковать все zip
# for (dirpath, dirnames, filenames) in os.walk('users'):
#     print(dirpath)
#     for filename in filenames:
#         if filename.endswith('.zip'):
#             try:
#                 with zipfile.ZipFile('%s\%s' % (dirpath,filename), "r") as zip_ref:
#                     zip_ref.extractall(dirpath)
#                 os.remove('%s\%s' % (dirpath,filename))
#             except Exception:
#                 continue

# Удалить все не .py файлы
# for (dirpath, dirnames, filenames) in os.walk('users'):
#     print(dirpath)
#     for filename in filenames:
#         if not filename.endswith('.py') or filename in ('setup.py', 'settings.py', '__init__.py'):
#             os.remove('%s\%s' % (dirpath,filename))

# Копируем все .py файлы в директорию пользователя без разделения на репо
# users = os.listdir('users')
# os.chdir('users')
#
# for user in users:
#     for (dirpath, dirnames, filenames) in os.walk(user):
#         for filename in filenames:
#             shutil.copy('%s\%s\%s' % (os.getcwd(), dirpath, filename), '%s\%s\%s' % (os.getcwd(), user, str(uuid.uuid4())[:8]) + '.py')
#             print('%s\%s' % (dirpath, filename))


# users = os.listdir('users')
# os.chdir('users')
#
# for user in users:
#     contents = os.listdir("%s" % user)
#     for c in contents:
#         if os.path.isdir('%s/%s' % (user, c)):
#             shutil.rmtree('%s/%s' % (user, c))
#         # if os.path.isfile('%s/%s' % (user, c)) and os.path.getsize('%s/%s' % (user, c)) < 256:
#         #     os.remove('%s/%s/%s' % (os.getcwd(), user, c))
#
#
# users = os.listdir('users')
# os.chdir('users')
#
# for user in users:
#     contents = os.listdir("%s" % user)
#     for c in contents:
#         if os.path.isfile('%s/%s' % (user, c)):
#             try:
#                 with open('%s/%s' % (user, c), encoding='utf-8') as f:
#                     count = sum(1 for _ in f)
#                 if count < 20:
#                     print(c)
#                     os.remove('%s/%s/%s' % (os.getcwd(), user, c))
#             except Exception:
#                 continue
from typed_ast import ast27, ast3

from utils.file_utils import get_file_info

users = os.listdir('users')
os.chdir('users')

# for user in users:
#     contents = os.listdir(user)
#     for c in contents:
#         with open('%s/%s' % (user, c), encoding='latin-1') as f:
#             file_content = f.read()
#         try:
#             tree = ast27.parse(file_content)
#         except Exception as ex:
#             try:
#                 tree = ast3.parse(file_content)
#                 is_ast3 = True
#             except Exception as ex:
#                 print('file deleted')
#                 os.remove('%s/%s' % (user, c))


for user in users:
    contents = os.listdir(user)
    for c in contents:
        file_info = get_file_info('%s/%s' % (user, c))
        file_lines = file_info.lines
        if len(file_lines) == 0:
            os.remove('%s/%s' % (user, c))


for user in users:
    contents = os.listdir(user)
    if len(contents) < 8:
        print(user)
        shutil.rmtree(user)

#
# users = os.listdir('users')
# os.chdir('users')
#
# for user in users:
#     contents = os.listdir(user)
#     if len(contents) > 150:
#         print(user)
#         shutil.rmtree(user)
