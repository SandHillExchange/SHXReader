"""
Setup new ubuntu 14.04 server to run SHX Reader

make sure you have fabric install
$ pip install fabric

in the directory of the fabfile.py
$ fab -H user@host setup
to setup the host computer
"""
from fabric.api import run, local, sudo, env
from fabric.decorators import task, parallel
from fabric.colors import green, red, yellow
from fabric.context_managers import cd
from fabric.contrib.files import exists


@task
def setup():
    """Install dependencies"""
    sudo('apt-get update')
    sudo('apt-get install libtool autoconf automake uuid-dev build-essential lynx-cur -y')
    sudo('apt-get install python-pip -y')
    sudo('pip install ipython')
    setup_nltk()
    setup_db()
    setup_crawl()


@task
def setup_nltk():
    sudo('pip install nltk')


@task
def setup_db():
    sudo('apt-get install mariadb-server -y')
    sudo('apt-get install python-mysqldb -y')
    sudo('apt-get install redis-server -y')


@task
def setup_crawl():
    sudo('apt-get install python-lxml -y')
    sudo('pip install requests')
    sudo('pip install selenium')
    sudo('pip install beautifulsoup4')
    sudo('pip install rq')
    sudo('pip install rq-dashboard')
    sudo('pip install Celery')
