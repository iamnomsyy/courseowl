from fabric.operations import run


def bootstrap_db_server():
    """
    Sets up a fresh Ubuntu 12.04 server to run PostgreSQL.
    Run with fab -H root@ip.ad.dr.ess bootstrap_db_server
    """
    bootstrap_server_common()
    run("apt-get install --yes postgresql postgresql-contrib")
    # TODO create database, user, password, privileges
    # TODO make the database listen on right IP/port
    print("Not implemented")


def bootstrap_http_server():
    """
    Sets up a fresh Ubuntu 12.04 server to run uWSGI + Nginx.
    Run with fab -H root@ip.ad.dr.ess bootstrap_http_server
    """
    bootstrap_server_common()
    run("apt-get install --yes libpq-dev python-dev python-pip")
    # TODO install uwsgi latest
    # TODO install nginx latest
    # TODO set up nginx and uwsgi config files
    # TODO set up virtualenv
    # TODO install pip packages
    run("pip install virtualenv virtualenvwrapper")
    print("Not implemented")


def bootstrap_server_common():
    """
    Sets up common things for Ubuntu 12.04 servers.
    """
    run("apt-get update")
    run("apt-get dist-upgrade --yes")
    run("apt-get install --yes ntp fail2ban monit htop")
    run("apt-get remove --purge whoopsie apport")

    # Set the timezone to UTC:
    run('echo "Etc/UTC" > /etc/timezone')
    run("dpkg-reconfigure -f noninteractive tzdata")
    run("service ntp restart")

    # Create deploy user:
    run("useradd -m -s /bin/bash deploy")
    run('echo "deploy:querty123" | chpasswd')


def bootstrap_server_common_postinstall():
    """
    Post-install scripts to run.
    """
    print("Finished setup.")
    print("Created user: deploy")
    print("With password: qwerty123")
    print("You should change this password to something more secure!")
