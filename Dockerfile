FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as poetry
# install git
RUN apt update
RUN apt install -y git
# install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry export -f requirements.txt --output ./requirements.txt
# RUN poetry build -f wheel -vvv
RUN pip download -r requirements.txt -d ./libraries

FROM python as runtime
# ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry ./app/libraries ./libraries
COPY --from=poetry ./app/open_precision ./open_precision
COPY --from=poetry ./app/LICENSE ./LICENSE
COPY --from=poetry ./app/config.yml ./config.yml
RUN pip install ./libraries/* --no-dependencies
RUN rm -rf ./libraries
EXPOSE 8000
# HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"
CMD python open_precision/__main__.py