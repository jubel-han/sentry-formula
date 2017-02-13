{% set db_name = pillar['sentry_server']['db_name'] %}
{% set db_user = pillar['sentry_server']['db_user'] %}
{% set db_password = pillar['sentry_server']['db_password'] %}

sentry-redis-config:
  file.replace:
    - name: /etc/redis/redis.conf
    - pattern: 'databases 16'
    - repl: 'databases 128'

redis-server-service:
  service.running:
    - name: redis-server
    - enable: True
    - reload: True

mysql-server-service:
  service.running:
    - name: mysql
    - enable: True
    - reload: True

mysql-sentry-user-creation:
  mysql_user.present:
    - host: localhost
    - name: {{ db_user }}
    - password: {{ db_password }}
    - connection_charset: utf8
    - saltenv:
      - LC_ALL: "en_US.utf8"
    - require:
      - service: mysql-server-service

mysql-sentry-user-permission:
  mysql_grants.present:
    - grant: all privileges
    - database: {{ db_name }}.*
    - user: {{ db_user }}
    - require:
      - mysql_user: {{ db_user }}

mysql-sentry-db-creation:
  mysql_database.present:
    - name: {{ db_name }}
    - require:
      - mysql_user: {{ db_user }}
