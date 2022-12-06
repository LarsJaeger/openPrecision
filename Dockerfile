FROM python:3 as base
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM base as dependency_loader
# install git
#RUN apt update
#RUN apt install -y git
# install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN poetry export -f requirements.txt --output ./requirements.txt --without-hashes
# RUN poetry build -f wheel -vvv
# RUN pip download -r requirements.txt -d ./libraries
RUN pip install -r requirements.txt --target=./libraries --no-dependencies

FROM base as runtime
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/libraries"
COPY open_precision /app/open_precision
COPY LICENSE /app/LICENSE
COPY config.yml /app/config.yml
COPY --from=dependency_loader /app/libraries /app/libraries
# RUN pip install ./libraries/* --no-dependencies
# RUN rm -rf ./libraries
EXPOSE 8000
# HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"
CMD python open_precision/__main__.py