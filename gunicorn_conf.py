import os

def numCPUs():
	if not hasattr(os, "sysconf"):
		raise RuntimeError("No sysconf detected.")
	return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "127.0.0.1:8000"
worker_class = 'gevent'
workers = numCPUs() * 2 + 1
backlog = 2048
keepalive = 2
worker_connections = 1000
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
