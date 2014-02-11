from __future__ import with_statement
import os
from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.context_managers import settings


def _setup_path():
    """
    Setup path
    """
    # Destination site for this push.
    env.site = env.environment + "." + env.domain
    # Root directory for project.  Default: {env.home}/www/{env.site}
    env.root = os.path.join(env.apps_dest, env.site)
    # Root directory for source code.  Default: {env.root}/{env.project}
    env.code_root = os.path.join(env.root, env.project)
    # Remote virtualenv directory. Default: {env.home}/.virtualenvs/{env.site}
    env.virtualenv_root = os.path.join(os.path.join(env.home, '.virtualenvs'), env.site)
    # Target project settings file. Default: {env.project}.settings
    env.settings = '%s.settings' % env.project


def production_http():
    env.hosts = ['107.170.37.29:22']
    _setup_path()
