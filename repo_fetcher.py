import os
import requests
import shutil
from github import Github, Commit

g = Github("user", "pass")

users = g.search_users(query='type:user language:Python followers:>50')

os.makedirs('users', exist_ok=True)
processed_users = os.listdir('users')

for user in users:
    if user.login in processed_users:
        continue
    repos = g.search_repositories(query='language:Python size:10..1000 user:%s' % user.login)
    found_repos = False
    print('User: %s' % user.login)
    for repo in repos:
        contributors = repo.get_stats_contributors()
        commits = repo.get_commits()
        is_single_commit = commits is Commit
        if contributors and len(contributors) == 1 and commits and not is_single_commit:
            os.makedirs('users/%s/%s' % (user.login, repo.name), exist_ok=True)
            if not os.path.exists("users/%s/%s/master.zip" % (user.login, repo.name)):
                url = 'https://github.com/%s/%s/archive/master.zip' % (user.login, repo.name)
                r = requests.get(url, verify=False, stream=True)
                r.raw.decode_content = True
                with open("users/%s/%s/master.zip" % (user.login, repo.name), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

# commits = first_repo  .get_commits(author=user.login)
#
# for c in commits:
#     for f in [f for f in c.files if f.filename[-3:] == '.py']:
#         print('%s %s %s' % (f.filename, f.additions, f.patch))

