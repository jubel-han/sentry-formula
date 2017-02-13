### Install sentry specific packages
{% from 'modules/setup-macroses.sls' import setup_pip_packages with context %}
{{ setup_pip_packages('sentry-packages') }}
