# -*- coding: utf-8 -*-
import os.path
from fabric.api import run, local, env, cd, prompt, settings
from config import GIT, PROJECT_NAME, LOCAL_USER, SUPERVISOR_CONFIG_PATH, DB_NAME, DB_USER, DB_PASSWORD

project = "test_task"
# the user to use for the remote commands
env.user = "test_task"
# the servers where the commands are executed
env.hosts = ['']

def reset():
	"""
	Сброс текущего окружения
	"""
	local("rm -rf .python-eggs")
	local("mkdir .python-eggs")


def setup():
	"""
	Настройка нового окружения.
	"""
	local("/usr/local/lib/python2.7.9/bin/virtualenv --no-site-packages env")
	activate_this = "env/bin/activate_this.py"
	execfile(activate_this, dict(__file__=activate_this))
	reset()
	local("pip install django")
	local("pip install django-filter")
	init_db()
	init_supervisor()
	local("python manage.py bower install")
	local("python manage.py createsuperuser")
	restart_app()


def debug():
	"""
	Запуск приложения для отладки.
	"""
	reset()
	local("python manage.py runserver")

def restart_app():
	"""
	перезапуск приложения production.
	"""
	local("sudo supervisorctl reread")
	local("sudo supervisorctl update")
	local("sudo supervisorctl restart test_task")

def init_supervisor():
	"""
	Настройка supervisor.
	"""
	local("sed -e \'s/__SRC_PATH__/{0}/g\' -e \'s/__PROJECT_NAME__/{1}/g\' {1}.conf > /etc/supervisor/conf.d/{1}.conf".format((os.path.abspath(os.path.dirname(__file__)).replace("/","\\/")), PROJECT_NAME))

def stop_app():
	"""
	Остановка supervisor.
	"""
	local("sudo supervisorctl stop {0}".format(PROJECT_NAME))

def init_db():
	"""
	Инициализация базы данных.
	"""
	local("su - postgres -c  \"CREATE ROLE '{0}' LOGIN ENCRYPTED PASSWORD '{1}'\"".format(DB_USER, DB_PASSWORD))
	local("su - postgres -c  \"CREATE DATABASE {0} OWNER {1} ENCODING 'UTF8'\"".format(DB_NAME, DB_USER))
	local("python manage.py migrate")

def copy_git_files():
	"""
	Копирование GIT.
	"""
	pass
