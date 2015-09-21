"""
    Fabric deployment script for Webfaction
"""
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files


# UPDATE THESE SETTINGS TO MATCH YOUR WEBFACTION ACCOUNT
env.user = 'USER_NAME'  # WEBFACTION / SSH USERNAME
env.hosts = [env.username + '.webfactional.com']  # WEBFACTION HOST NAME
env.app_name = 'WEBFACTION_APP_NAME'  # WEBFACTION APPLICATION NAME
env.django_settings_module = 'DJANGO_SETTINGS_MODULE'  # YOUR DJANGO SETTINGS MODULE


# set virtual environment name to match the webfaction app name
env.ve_name = env.app_name

# Web App, Apache, and Django App Directory Settings
env.home_dir = '/home/' + env.user
env.django_root = env.home_dir + '/webapps/' + env.app_name
env.django_code_dir = env.django_root + '/code'
env.apache_dir = env.django_root + '/apache2/bin'

# Remote GIT Repo Directory and name
env.remote_repos_dir = env.home_dir + '/repos/'
env.remote_project_repo_dir = env.remote_repos_dir + env.app_name + '.git'


# Virtual Environment Settings
env.ve_directory_name = '/.virtualenvs'
env.ve_root_directory = env.home_dir + env.ve_directory_name
env.ve_activate = 'workon ' + env.ve_name


# Django Production settings
env.django_prod_settings = '--settings=' + env.django_settings_module

# Bash Profile
env.bash_profile = env.home_dir + '/.bash_profile'


# NON TASK HELPER FUNCTIONS
#############################
def setup_python_alias():
    print 'Setting up Python Alias in .bash_profile'
    if not files.exists(env.bash_profile):
        abort("%s does not exist." % env.bash_profile)

    ALIAS_CMD = "alias python=python2.7"
    if files.append(env.bash_profile, ALIAS_CMD):
        print '    Python Alias appended to %s' % (env.bash_profile,)
    else:
        print '    %s already contains Python Alias' % (env.bash_profile,)


def install_virtualenvironment():
    print "Attemping to install virtualenv"
    run('pip install virtualenv')

    print "Attempting to install virtualenvwrapper"
    run('pip install --install-option="--user" virtualenvwrapper')

    print "Make virtual enviroment directory"
    run('mkdir -p ' + env.ve_root_directory)

    VIRTUAL_ENV_BASH_PROFILE_SETTINGS = [
        'export WORKON_HOME=$HOME' + env.ve_directory_name,
        'export VIRTUALENVWRAPPER_TMPDIR=$WORKON_HOME/tmp',
        'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7',
        'source $HOME/bin/virtualenvwrapper.sh',
        'export PIP_VIRTUALENV_BASE=$WORKON_HOME',
        'export PIP_RESPECT_VIRTUALENV=true']

    print "Attempting to add Virtual Env settings to .bash_proflie"
    if files.append(env.bash_profile, VIRTUAL_ENV_BASH_PROFILE_SETTINGS):
        print "   Added Virtual Env settings to %s" % (env.bash_profile,)
    else:
        print "    Virtual Env settings already exist in %s" % (
            env.bash_profile,)


def create_project_ve():
    if not files.exists(env.ve_root_directory + "/" + env.ve_name):
        print 'Making %s VirtualEnv' % (env.ve_name,)
        run('mkvirtualenv ' + env.ve_name)
    else:
        print '%s VirtualEnv Already Exists' % (env.ve_name,)


def setup_webfaction_remote_repo():
    print 'Attempting to setup a remote repo on Webfaction'

    run('mkdir -p ' + env.remote_project_repo_dir)
    with cd(env.remote_project_repo_dir):
        run('git init --bare')

    add_webfaction_remote()


# TASKS HELPER FUNCTIONS
#############################
@task
def run_tests():
    local("python manage.py test")


@task
def push_production():
    local("git push webfaction")
    with cd(env.django_code_dir):
        run('git pull')


@task
def collectstatic():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py collectstatic --noinput ' + env.django_prod_settings)


@task
def syncdb():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py syncdb ' + env.django_prod_settings)


@task
def migratedb():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py migrate ' + env.django_prod_settings)


@task
def update_database():
    syncdb()
    migratedb()


@task
def deploy(test="No"):
    if test.upper()[0] == "Y":
        run_tests()
    push_production()
    collectstatic()


@task
def restart_apache():
    run(env.apache_dir + '/restart', pty=False)


@task
def stop_apache():
    run(env.apache_dir + '/stop', pty=False)


@task
def start_apache():
    run(env.apache_dir + '/start', pty=False)


@task
def add_webfaction_remote():
    print "Adding remote repo to local git as 'webfaction'"
    with settings(warn_only=True):
        local('git remote add webfaction ssh://' + env.user + '@' +
              env.hosts[0] + env.remote_project_repo_dir)


@task
def bootstrap():
    if not confirm('Running this method may delete existing files. Are you sure you want to do this?', default=False):
        abort("Aborting bootstrap.")

    print 'Attempting to bootstrap application'
    setup_python_alias()

    print 'Installing PIP'
    run('easy_install-2.7 pip')

    install_virtualenvironment()

    create_project_ve()

    setup_webfaction_remote_repo()
