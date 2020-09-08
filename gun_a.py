# gunicorn.py
import os
import multiprocessing

if not os.path.exists('log_auth'):
    os.mkdir('log_auth')

bind = '0.0.0.0:5000' 
chdir = './'
workers = multiprocessing.cpu_count() * 2 + 1  
worker_class = 'gevent'
worker_connections = 2048
backlog = 2048 

debug = True
loglevel = 'debug'
pidfile = 'log_auth/gunicorn.pid'
logfile = 'log_auth/debug.log'
errorlog = 'log_auth/error.log'
accesslog = 'log_auth/access.log'

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #設置 gunicorn 訪問日誌格式，錯誤日誌無法設置