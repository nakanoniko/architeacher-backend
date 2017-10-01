import multiprocessing
import os

bind = '127.0.0.1:5000'
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = os.path.abspath(os.path.dirname(__file__)) + '/error.log'
accesslog = os.path.abspath(os.path.dirname(__file__)) + '/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s"'
