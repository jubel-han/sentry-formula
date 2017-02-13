# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *
import os.path

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
# You can swap out the engine for MySQL easily by changing this value
# to ``django.db.backends.mysql`` or to PostgreSQL with
# ``django.db.backends.postgresql_psycopg2``
# If you change this, you'll also need to install the appropriate python
# package: psycopg2 (Postgres) or mysql-python
      'ENGINE': 'django.db.backends.mysql',
      'NAME': '{{ pillar['sentry_server']['db_name'] }}',
      'USER': '{{ pillar['sentry_server']['db_user'] }}',
      'PASSWORD': '{{ pillar['sentry_server']['db_password'] }}',
      'HOST': 'localhost',
      'PORT': '',
      'OPTIONS': {
	      'init_command': 'SET storage_engine=INNODB'
      },
# If you're using Postgres, we recommend turning on autocommit
# 'OPTIONS': {
# 'autocommit': True,
# }
   }
}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# The administrative email for this installation.
# Note: This will be reported back to getsentry.com as the point of contact. See
# the beacon documentation for more information. This **must** be a string.

# SENTRY_ADMIN_EMAIL = 'your.name@example.com'
SENTRY_ADMIN_EMAIL = '{{ pillar['sentry_server']['sentry_email'] }}'

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True


#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

SENTRY_REDIS_OPTIONS = {
    'hosts': {
        {{ pillar['sentry_server']['redis_db'] }}: {
            'host': {{ pillar['sentry_server']['redis_host'] }},
            'port': {{ pillar['sentry_server']['redis_port'] }},
        }
    }
}

###########
## CACHE ##
###########

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

###########
## Queue ##
###########
# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.
# You can enable queueing of jobs by turning off the always eager setting:

CELERY_ALWAYS_EAGER = False
BROKER_URL = 'redis://localhost:6379'

###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

################
# File storage #
################

# Any Django storage backend is compatible with Sentry. For more solutions see
# the django-storages package: https://django-storages.readthedocs.org/en/latest/

SENTRY_FILESTORE = 'django.core.files.storage.FileSystemStorage'
SENTRY_FILESTORE_OPTIONS = {
    'location': '/home/{{ pillar['sentry_server']['user'] }}/sentry-files',
}

################
## Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = '{{ pillar['sentry_server']['sentry_url_prefix'] }}{{ pillar['sentry_server']['sentry_domain'] }}' # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# header, and uncomment the following setting
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SENTRY_WEB_HOST = 'localhost'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 3, # the number of gunicorn workers
    'limit_request_line': 0,
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}
ALLOWED_HOSTS = [{{ pillar['sentry_server']['allowed_hosts'] }}]

#################
## Mail Server ##
#################
# For more information check Django's documentation:
# https://docs.djangoproject.com/en/1.9/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{{ pillar['email']['host'] }}'
EMAIL_PORT = {{ pillar['email']['port'] }}
EMAIL_HOST_USER = '{{ pillar['email']['user'] }}'
EMAIL_HOST_PASSWORD = '{{ pillar['email']['password'] }}'
EMAIL_USE_TLS = {{ pillar['email']['tls'] }}
EMAIL_USE_SSL = {{ pillar['email']['ssl'] }}
# The email address to send on behalf of
SERVER_EMAIL = 'noreply@ylly.com'

# If you're using mailgun for inbound mail, set your API key and configure a
# route to forward to /api/hooks/mailgun/inbound/
# MAILGUN_API_KEY = ''

###########
## etc. ##
###########
# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = '{{ pillar['sentry_server']['secret_key'] }}'
