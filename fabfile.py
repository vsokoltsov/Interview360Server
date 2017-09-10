from fabric.api import cd, run, sudo, env, put
from fabric.contrib.files import exists

PROJECT_NAME = 'interview_manager'
GITHUB_PROJECT = 'https://github.com/vforvad/InterviewManager.git'
env.user = 'root'
env.hosts = ['root@95.213.194.196']
env.home_dir = '/root'

def set_up():
    """ Setting up all dependencies """

    with cd(env.home_dir):
        put('setup.sh', '{}'.format(env.home_dir))
        run('bash setup.sh')

def pull_remote(branch):
    """ Pull app from the repo or change the branch """

    with cd(env.home_dir):
        if exists("{}/{}".format(env.home_dir, PROJECT_NAME)):
            run('cd {}/{} && git pull && git checkout {}'.format(env.home_dir, PROJECT_NAME, branch))
        else:
            run("git clone {} {}".format(GITHUB_PROJECT, PROJECT_NAME))

def restart_gunicorn():
    """ Restart gunicorn service """

    with cd(env.home_dir):
        sudo('systemctl restart gunicorn', pty=False)
        put('deploy/gunicorn.service', '{}'.format(env.home_dir))


def deploy(branch='master'):
    """ Base deploy method """

    pull_remote(branch)
    restart_gunicorn()
