@echo off

REM Script to build and run the Agoda scraper Docker container

REM Build the Docker image
echo Building Docker image...
docker-compose build

REM Run the container
echo Starting container...
docker-compose up

REM To run in detached mode, uncomment the following line instead
REM docker-compose up -d