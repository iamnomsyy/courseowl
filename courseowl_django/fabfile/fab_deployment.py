import os
import datetime
from django.utils.encoding import force_unicode
from django.utils.text import slugify
from fabric.operations import prompt, local, run

def bootstrap_db_server():
    """
    Sets up a fresh Ubuntu 12.04 server to run PostgreSQL.
    Run with fab -H root@ip.ad.dr.ess bootstrap_db_server
    """
    bootstrap_server_common()
    run("apt-get install postgresql postgresql-contrib")
    # TODO create database, user, password, privileges
    # TODO make the database listen on right IP/port
    print("Not implemented")


def bootstrap_http_server():
    """
    Sets up a fresh Ubuntu 12.04 server to run uWSGI + Nginx.
    Run with fab -H root@ip.ad.dr.ess bootstrap_http_server
    """
    bootstrap_server_common()
    run("apt-get install libpq-dev python-dev python-pip")
    # TODO install uwsgi latest
    # TODO install nginx latest
    # TODO set up nginx and uwsgi config files
    # TODO set up virtualenv
    # TODO install pip packages
    print("Not implemented")


def bootstrap_server_common():
    """
    Sets up common things for Ubuntu 12.04 servers.
    """
    run("apt-get update")
    run("apt-get dist-upgrade")
    run("apt-get install ntp fail2ban monit htop")
