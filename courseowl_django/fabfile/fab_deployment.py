from __future__ import with_statement
from fabric.api import require
from fabric.contrib.project import rsync_project
from fabric.operations import prompt, run
from fabric.state import env


RSYNC_EXCLUDE = (
    '.idea',
    '.DS_Store',
    '.hg',
    '.svn',
    '.git',
    '*.pyc',
    '*.log',
    '*.example',
    '*.so',
    '*.o',
    'courseowl_django/settings/settings_personal.py',
)


def deploy():
    """ rsync code to remote host """
    require('root', provided_by='production_http')
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )

    uwsgi_supervisord = 'n'
    if env.env_var in ['production_http']:
        uwsgi_supervisord = prompt('Restart uwsgi? (y/N) ', 'n')
    if uwsgi_supervisord == 'y':
        uwsgi_supervisord_restart()


def uwsgi_supervisord_restart():
    """
    Restart uWSGI on remote host
    """
    require('root', provided_by='production_http')
    run('sudo /usr/bin/supervisorctl restart courseowl_uwsgi')


### HOST DEFINITIONS ###

def production_http():
    env.hosts = ['107.170.37.29:22']
    env.root = "/var/www"
    env.user = "deploy"
    env.env_var = "production_http"
