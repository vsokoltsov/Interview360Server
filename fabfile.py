from fabric.api import cd, run, sudo, env, put, prefix
from fabric.contrib.files import exists

env.user = 'root'
env.hosts = ['root@95.213.194.196']
env.home_dir = '/root'

PROJECT_NAME = 'interview_manager'
PG_HBA_PATH = '/var/lib/pgsql/data/'
PROJECT_PATH = "{}/{}".format(env.home_dir, PROJECT_NAME)
GITHUB_PROJECT = 'https://github.com/vforvad/InterviewManager.git'

def set_up():
    """ Setting up all dependencies """

    with cd(env.home_dir):
        put('setup.sh', '{}'.format(env.home_dir))
        run('bash setup.sh')

def replace_hba_conf():
    """ Replace ph_hba.conf file on server with the current one"""

    with cd(PG_HBA_PATH):
        put('./deploy/pg_hba.conf', PG_HBA_PATH)
        sudo('systemctl restart postgresql')
        sudo('systemctl enable postgresql')

def set_virtualenvwrapper():
    """ Setting up virtual env wrapper """

    with cd(env.home_dir):
        run('pyenv virtualenvwrapper')
        with prefix('. $(pyenv which virtualenvwrapper.sh)'):
            run('mkvirtualenv interview_manager')

def pull_remote(branch):
    """ Pull app from the repo or change the branch """

    with cd(env.home_dir):
        if exists(PROJECT_PATH):
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
