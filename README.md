# openPrecision

## Documentation

Documentation of the main branch can be found [here](https://larsjaeger.github.io/openPrecision/)
For code that is still in development, generated documentation can be found in the `doc` folder after being generated
by `poetry run nox`.

More information on how to document the code can be found [here](https://pdoc.dev/docs/pdoc.html#how-can-i).

## Deployment

***TODO***


## Building the Docker Image

Prerequisites:
- [install Docker](https://docs.docker.com/engine/install/)
- [setup buildx](https://github.com/docker/buildx?tab=readme-ov-file#installing)

Steps:
1. clone repository using one of the following commands:
   - `git clone git@github.com:LarsJaeger/openPrecision.git --recurse_submodules`
   - `git clone https://github.com/LarsJaeger/openPrecision.git --recurse_submodules`
2. run `docker buildx bake -f docker-compose.yml` to build the image (, then push it to whatever registry you
   want)

## Contributing

1. create issue to resolve
2. create branch following the naming convention `#[issue_number]_[branch_name]`
3. clone repository using one of the following commands:
   - `git clone git@github.com:LarsJaeger/openPrecision.git --recurse_submodules`
   - `git clone https://github.com/LarsJaeger/openPrecision.git --recurse_submodules`
4. if not already installed, [install poetry](https://python-poetry.org/docs/#installation)
5. to install the required dependencies run `poetry install --with dev`
6. run `poetry run pre-commit install`
7. if committing is rejected, run `poetry run nox` and check for errors / failures
   > This will format the code and run all tests (which will also happen automatically on commit, but the commit will be
   rejected if for example a test fails).
8. create pull request and wait for review
