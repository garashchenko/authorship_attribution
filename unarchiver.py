import os
import shutil
import uuid
import zipfile
# Распаковать все zip
# for (dirpath, dirnames, filenames) in os.walk('users'):
#     print(dirpath)
#     for filename in filenames:
#         if filename.endswith('.zip'):
#             with zipfile.ZipFile('%s\%s' % (dirpath,filename), "r") as zip_ref:
#                 zip_ref.extractall(dirpath)
#             os.remove('%s\%s' % (dirpath,filename))
# Удалить все не .py файлы
# for (dirpath, dirnames, filenames) in os.walk('users'):
#     print(dirpath)
#     for filename in filenames:
#         if not filename.endswith('.py'):
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


users = os.listdir('users')
os.chdir('users')

for user in users:
    contents = os.listdir("%s" % user)
    for c in contents:
        if os.path.isfile('%s/%s' % (user, c)) and os.path.getsize('%s/%s' % (user, c)) < 256:
            os.remove('%s/%s/%s' % (os.getcwd(), user, c))



