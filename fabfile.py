from fabric.api import cd, run, sudo, env
from fabric.contrib.files import exists

PROJECT_NAME = 'interview_manager'
GITHUB_PROJECT = 'https://github.com/vforvad/InterviewManager.git'
env.user = 'root'
env.hosts = ['root@95.213.194.196']
env.home_dir = '/root'

def pull_remote():
    with cd(env.home_dir):
        if exists("{}/{}".format(env.home_dir, PROJECT_NAME)):
            run('cd {}/{} && git pull && git checkout add-deploy'.format(env.home_dir, PROJECT_NAME))
        else:
            run("git clone {} {}".format(GITHUB_PROJECT, PROJECT_NAME))
