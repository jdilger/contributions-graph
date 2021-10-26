# get_logs.py
import subprocess
import os

REPO_FOLDER = 'git_repos'
# todo: have this read from csv or txt or yml
repos = ['users/TEST/utils']
working_path = os.getcwd()
repos_path = os.path.join(working_path, REPO_FOLDER)
print('working path',working_path)
print('repos_path',repos_path)
if os.path.exists(repos_path):
    pass
else:
    os.mkdir(repos_path)

# clone each repo
for i in repos:
    r_name = i.split("/")[-1]
    subprocess.Popen(['git', 'clone', f'https://earthengine.googlesource.com/{i}',f"{REPO_FOLDER}/{r_name}"]).communicate()

ee_folders = os.listdir(REPO_FOLDER)
print(ee_folders,'ee folders')
all_logs = []
print(ee_folders)
# iterate through each repo and capture commits
for repo in ee_folders:
    os.chdir(f'{repos_path}/{repo}')
    print('loop cwd', os.getcwd())
    stdout, stderr = subprocess.Popen(['git','log',"--author=JohnJdilger",'--pretty=format:"%ad"', '--date=format:"%Y-%m-%d"'],text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    logs = stdout.splitlines()
    #logs2 = subprocess.run(['git','log',"--author=jdilger",'--pretty=format:"%ad"', '--date=format:"%Y-%m-%d"'],capture_output=True, text=True).stdout.splitlines()

    # clean up subprocess junk
    clean_logs = [i.replace('"',"") for i in logs]
#     clean_logs2 = [i.replace('"',"") for i in logs2]
    
    # add to log counter
    tmp = clean_logs #+ clean_logs2
    all_logs.extend(tmp)

log_dict = {i:all_logs.count(i) for i in all_logs}
print(log_dict)
os.chdir(working_path)
with open('repo_count.txt','w') as f:
    for k,v in log_dict.items():
        f.writelines(f"{k} {v}\n")
print(os.listdir(working_path))
