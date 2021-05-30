# flake8: noqa
# Gunicorn Configuration File.
# See: http://docs.gunicorn.org/en/latest/settings.html
import os

bind = '0.0.0.0:8888'

# Send error logs to stderr
errorlog = '-'

worker_class = 'gthread'
workers = 2
threads = 2

# Workers silent for more than this many seconds are killed and restarted.
timeout = 60

# Restart workers once in a while, to limit memory leaks, if any.
max_requests = 2500
max_requests_jitter = 30

# By preloading an application you can save some RAM resources as well as speed up server boot times.
preload_app = True

# Workers accept connections from the TCP backlog and distribute it amongst the threads.
# Hence if it accepts more connections than the thread count, the remaining awaits in a queue within the worker
# and are picked up once a thread becomes free. Workers seem to be accepting connections independent of its
# load (size of its internal queue) and hence causing delayed response for few connections.
# So in order to evenly distribute the load amongst the workers we are setting the worker_connections value
# to be same as the thread count (workers won't accept connections if there are no threads to handle).
worker_connections = 5

# The number of seconds to wait for requests on a Keep-Alive connection (if any). The number of
# keep-alived connections = worker_connections - threads
keepalive = 65

# The Access log file to write to.
# '-' means log to stdout.
if os.getenv('ENABLE_GUNICORN_ACCESS_LOGS', 'False') == 'True':
    access_log_format = '%(h)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" x_fwd_host=%({x-forwarded-host}i)s x_fwd_proto=%({x-forwarded-proto}i)s response_duration=%(L)s'
    accesslog = '-'
