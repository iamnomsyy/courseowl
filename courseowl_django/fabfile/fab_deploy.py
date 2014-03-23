from __future__ import with_statement
from fabric.api import *
from fabric.contrib.project import rsync_project

RSYNC_EXCLUDE = (
    '.DS_Store',
    '.hg',
    '.svn',
    '.git',
    '*.pyc',
    '*.log',
    '*.example',
    'media/',
    'whoosh_index/',
    '.idea/',
    '*.so',
    '*.o'
)


def deploy():
    """
    rsync code to remote host.
    """
    require('root', provided_by='courseowl_http')

    extra_opts = '--omit-dir-times'

    rsync_project(
        remote_dir=env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )

    collectstatic_prompt = prompt('Collectstatic? (y/N) ')
    uwsgi_supervisord = prompt('Restart uwsgi? (y/N) ')

    if collectstatic_prompt == 'y':
        collectstatic()

    if uwsgi_supervisord == 'y':
        uwsgi_supervisord_restart()


def uwsgi_supervisord_restart():
    """
    Restart uWSGI on remote host.
    """
    require('root', provided_by='courseowl_http')
    run('sudo /usr/bin/supervisorctl restart courseowl_uwsgi')


def collectstatic():
    """
    Run manage.py collectstatic to copy static files into place on the server.
    """
    run('OWL_ENV="production_http" /home/deploy/.virtualenvs/owl/bin/python '
        '/var/www/courseowl_django/courseowl_django/manage.py collectstatic --noinput')


def courseowl_http():
    """
    Deploy to CourseOwl production server.
    """
    env.hosts = ['courseowl.com:22']
    env.user = 'deploy'
    env.root = '/var/www/courseowl_django/'
