# openPrecision

## Installation

1. install Raspbian on your RaspberryPi
2. install Docker
3. TODO add instructions for the rest

## Building the Docker Image

Requirements:

- Docker
- buildx is setup

When using bno055 IMU, the following steps are recommended for the SBC to boot properly:

1. disable kernel serial port by running `sudo systemctl disable serial-getty@ttyAMA0.service`

1. Clone the repository
2. optional: run `docker buildx bake -f docker-compose.yml` to build the image (, then push it to whatever registry you
   want)
3. on the SBC, run `docker-compose up -d` to start the containers
4. 