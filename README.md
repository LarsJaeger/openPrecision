# openPrecision

## Installation

1. install Raspbian on your RaspberryPi
2. install Docker
3. TODO add instructions for the rest

## Building the Docker Image

Requirements:

- Docker
- buildx is setup

Procedure:

1. disable kernel serial port by running `sudo systemctl disable serial-getty@ttyAMA0.service`

1. Clone the repository
2. optional: run `docker buildx bake -f docker-compose.yml` to build the image (, then push it to whatever registry you
   want)
3. on the SBC, run `docker-compose up -d` to start the containers

## Documentation

The generated documentation can be found in the `doc` folder.

More information on how to document the code can be found [here](https://pdoc.dev/docs/pdoc.html#how-can-i).

## Contributing

1. create issue to resolve
2. create branch following the naming convention `#[issue_number]_[branch_name]`
3. clone repository
4. if not already installed, [install poetry](https://python-poetry.org/docs/#installation)
5. to install the required dependencies run `poetry install --with dev`
6. run `poetry run pre-commit install`
7. if committing is rejected, run `poetry run nox` and check for errors / failures
   > This will format the code and run all tests (which will also happen automatically on commit, but the commit will be
   rejected if for example a test fails).
8. create pull request and wait for review