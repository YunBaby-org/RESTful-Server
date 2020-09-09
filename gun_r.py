"""gunicorn_RESTful"""
import os
import multiprocessing

if not os.path.exists('log_rest'):
    os.mkdir('log_rest')

bind = '0.0.0.0:5001' 
chdir = './' 
workers = multiprocessing.cpu_count() * 2 + 1  
worker_class = 'gevent'
worker_connections = 1024 
backlog = 1024

debug = True
loglevel = 'debug'
pidfile = 'log_rest/gunicorn.pid'
logfile = 'log_rest/debug.log'
errorlog = 'log_rest/error.log'
accesslog = 'log_rest/access.log'

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #設置 gunicorn 訪問日誌格式，錯誤日誌無法設置