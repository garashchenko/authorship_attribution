import os

import requests
import shutil
from github import Github, Commit
import datetime

g = Github("user", "pass")

users = g.search_users(query='type:user language:Python type:user followers:10')

os.makedirs('users', exist_ok=True)
processed_users = os.listdir('users')

try:
    with open('ignore.txt') as f:
        ignore_list = f.read().splitlines()
except Exception:
    ignore_list = []
    print('No ignore file found')


rate_limit = g.get_rate_limit()

test = g.rate_limiting_resettime

print(datetime.datetime.fromtimestamp(int(test)).strftime('%Y-%m-%d %H:%M:%S'))

for user in users:
    found_repos = False

    if user.login in processed_users:
        continue

    if user.login in ignore_list:
        continue

    repos = user.get_repos()

    print('User: %s' % user.login)
    for repo in repos:
        if repo.language != 'Python' or repo.size < 2 or repo.size > 110000:
            print('%s %s %s' % (user.login, repo.language, repo.size))
            continue
        try:
            contributors = repo.get_stats_contributors()
            commits = repo.get_commits()
            is_single_commit = commits is Commit
        except Exception:
            print('%s: error on fetching repo data' % user.login)

        if contributors and len(contributors) == 1 and commits and not is_single_commit:
            found_repos = True
            os.makedirs('users/%s/%s' % (user.login, repo.name), exist_ok=True)
            if not os.path.exists("users/%s/%s/master.zip" % (user.login, repo.name)):
                url = 'https://github.com/%s/%s/archive/master.zip' % (user.login, repo.name)
                r = requests.get(url, verify=False, stream=True)
                r.raw.decode_content = True
                with open("users/%s/%s/master.zip" % (user.login, repo.name), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

    if not found_repos:
        with open('ignore.txt', 'a') as f:
            f.write(user.login + '\n')

# commits = first_repo  .get_commits(author=user.login)
#
# for c in commits:
#     for f in [f for f in c.files if f.filename[-3:] == '.py']:
#         print('%s %s %s' % (f.filename, f.additions, f.patch))

