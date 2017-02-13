/etc/nginx/sites-available/sentry:
  file.managed:
    - source: salt://sentry/files/nginx-conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644

/etc/nginx/sites-enabled/sentry:
  file:
    - symlink
    - target: /etc/nginx/sites-available/sentry
    - force: True

reload_nginx_service_jenkins:
  service.running:
    - name: nginx
    - reload: True
    - enable: True
    - watch:
      - file: /etc/nginx/sites-enabled/sentry
      - file: /etc/nginx/sites-available/sentry
