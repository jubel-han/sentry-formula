{% set user = pillar['sentry_server']['user'] %}
{% set group = pillar['sentry_server']['group'] %}

system-sentry-user-group:
  group.present:
    - name: {{ group }}
  user.present:
    - name: {{ user }}
    - shell: /bin/bash
    - home: /home/sentry
    - gid_from_name: True
    - require:
      - group: {{ group }}

sentry-installation-requirements:
  file.managed:
    - name: /home/{{ user }}/requirements.txt
    - source: salt://sentry/files/requirements.txt
    - mode: 644
    - user: {{ user }}
    - group: {{ group }}

sentry-server-configuration:
  file.managed:
    - name: /home/{{ user }}/sentry.conf.py
    - source: salt://sentry/files/sentry.conf.py
    - template: jinja
    - mode: 600
    - user: {{ user }}
    - group: {{ group }}

sentry-python-virtualenv:
  virtualenv.managed:
    - name: /home/{{ user }}/venv
    - system_site_packages: False
    - user: {{ user }}
    - requirements: /home/{{ user }}/requirements.txt
    - no_chown: True
    - require:
      - file: sentry-server-configuration
      - file: sentry-installation-requirements

sentry-server-wsgi-file:
  file.managed:
    - name: /home/{{ user }}/wsgi.py
    - source: salt://sentry/files/wsgi.py
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755

sentry-server-wsgi-configuration:
  file.managed:
    - name: /home/{{ user }}/sentry.ini
    - source: salt://sentry/files/sentry.ini
    - template: jinja
    - user: {{ user }}
    - group: {{ group }}
    - mode: 644
    - require:
      - file: sentry-server-wsgi-file
    - context:
        user: {{ user }}

sentry-server-logs-directory:
  file.directory:
    - name: /home/{{ user }}/logs
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

sentry-server-start-script:
  file.managed:
    - name: /home/{{ user }}/start-sentry-server.sh
    - source: salt://sentry/files/start-sentry-server.sh
    - template: jinja
    - mode: 755
    - user: {{ user }}
    - group: {{ group }}
    - context:
        user: {{ user }}

sentry-db-migration:
  cmd.wait:
    - name: /home/{{ user }}/venv/bin/sentry --config=/home/{{ user }}/sentry.conf.py upgrade
    - user: {{ user }}
    - watch:
      - file: sentry-server-configuration

sentry-server-service-startup:
  file.managed:
    - name: /etc/init/sentry-uwsgi.conf
    - source: salt://sentry/files/sentry-uwsgi.conf
    - mode: 744
    - user: root
    - group: root
    - template: jinja
    - context:
        user: {{ user }}

sentry-worker-service-startup:
  file.managed:
    - name: /etc/init/sentry-worker.conf
    - source: salt://sentry/files/sentry-worker.conf
    - mode: 744
    - user: root
    - group: root
    - template: jinja
    - context:
        user: {{ user }}

sentry-server-service-enabled:
  cmd.wait:
    - name: restart sentry-uwsgi;
    - watch:
      - file: sentry-server-service-startup

sentry-worker-service-enabled:
  cmd.wait:
    - name: restart sentry-worker;
    - watch:
      - file: sentry-worker-service-startup
