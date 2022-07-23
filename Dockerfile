FROM docker-proxy.sberned.ru/python:3.10.5-slim as dependencies

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=10 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_NO_INTERACTION=1 \
  POETRY_INSTALLER_PARALLEL=false \
  POETRY_VERSION=1.1.7 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv" \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
WORKDIR /app

# we use make for lint / test / migrate commands
RUN /bin/sh -c set -ex; \
  apt-get update; \
  apt-get install -y --no-install-recommends curl build-essential; \
  curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python; \
  rm -rf /var/lib/apt/lists/*

# copy python dependencies
COPY poetry.lock pyproject.toml $PYSETUP_PATH/

# non-root user rights
RUN groupadd -r app && useradd --no-log-init -r -g app app && chown -R app /app

COPY --chown=app:app settings /app/settings
COPY --chown=app:app Makefile pyproject.toml /app/

# bump version from git tags
COPY --chown=app:app VERSION /app/
RUN poetry version $(cat VERSION)

# layer with dev dependencies installed
FROM dependencies as development

USER root
COPY .editorconfig flake8.tests.ini setup.cfg /app/

RUN cd $PYSETUP_PATH; \
  poetry export --dev --without-hashes --with-credentials -f requirements.txt -o requirements.txt; \
  pip install -U -r requirements.txt

COPY app /app/app
COPY tests /app/tests

FROM dependencies as production

# install prod dependencies
RUN cd $PYSETUP_PATH; \
  poetry export --without-hashes --with-credentials -f requirements.txt -o requirements.txt; \
  pip install -U -r requirements.txt

COPY --chown=app:app app /app/app
USER app
