# because of missing wheels for some arm architectures, the platform is set to linux/amd64
FROM --platform=linux/amd64 python:3-alpine as dependency_exporter
ENV PYTHONUNBUFFERED=true
WORKDIR /app
# install git
# RUN apt update
# RUN apt install -y git
# install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN poetry export -f requirements.txt --output ./requirements.txt --without-hashes

# install dependencies in seperate container because the final base image does not have git installed
FROM --platform=$TARGETPLATFORM python:3 as dependency_loader
ENV PYTHONUNBUFFERED=true
WORKDIR /app

COPY --from=dependency_exporter /app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --target=./libraries --no-dependencies

FROM node:14-alpine as frontend_builder
WORKDIR /app
COPY open_precision_frontend /app
RUN npm install
RUN npm run build



FROM --platform=$TARGETPLATFORM python:3-slim as runtime
ENV PYTHONUNBUFFERED=true
WORKDIR /app

# copy libraries
COPY --from=dependency_loader /app/libraries /app/libraries
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/libraries"

# copy frontend
COPY --from=frontend_builder /app/dist /app/open_precision_frontend

ENV PYTHONPATH="${PYTHONPATH}:/app"
COPY open_precision /app/open_precision
COPY LICENSE /app/LICENSE
COPY config.yml /app/open_precision/config.yml

EXPOSE 8000
# HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"
CMD python open_precision/__main__.py