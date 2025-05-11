# Agoda Scraper Docker Setup Guide

This guide explains how to run the Agoda Scraper application in Docker with Xvfb for headless browser automation.

## Project Overview

This project is a web scraper for Agoda.com that captures hotel information using Playwright. The application:

1. Accepts hotel search parameters
2. Generates a URL for the hotel page
3. Uses Playwright to navigate to the page and capture API responses
4. Parses the JSON data and returns structured hotel information

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone the repository if needed)

## Docker Setup

The project includes a Dockerfile and docker-compose.yml that handle all the necessary setup, including:

- Python 3.11 environment
- All required Python dependencies
- Playwright with Chromium browser
- Xvfb for virtual display support

## Running the Application

### 1. Build and Start the Docker Container

```bash
# Navigate to the project directory
cd "path/to/agooda scraper"

# Build and start the container
docker-compose up --build
```

This will:
- Build the Docker image with all dependencies
- Install Playwright and Chromium
- Configure Xvfb as a virtual display
- Start the FastAPI server on port 8080

### 2. Using the API

Once the container is running, you can access the API at http://localhost:8000

#### Test Endpoint

Verify the server is running:
```
GET http://localhost:8080/test
```

#### Trigger Scraper

Start a scraping job:
```
POST http://localhost:8000/trigger
```

With JSON body:
```json
{
  "destination": "Hotel Name",
  "location": "Hotel Address",
  "checkin": "YYYY-MM-DD",
  "checkout": "YYYY-MM-DD",
  "adults": 2,
  "children": 0,
  "rooms": 1
}
```

## How It Works

### Xvfb in Docker

The application uses Xvfb (X Virtual Framebuffer) to provide a virtual display for Playwright to run in non-headless mode inside the Docker container. This is necessary because:

1. Some websites detect and block headless browsers
2. Some functionality may behave differently in headless mode

The entrypoint script automatically:
1. Starts Xvfb on display :99
2. Sets the DISPLAY environment variable
3. Runs the application with this virtual display

### Key Components

- **Dockerfile**: Contains all setup instructions for the environment
- **docker-compose.yml**: Simplifies container management
- **entrypoint.sh**: Created during build to set up Xvfb
- **server.py**: FastAPI server that handles API requests
- **get_json_data.py**: Contains the Playwright logic for scraping

## Troubleshooting

### Common Issues

1. **Container exits immediately**:
   - Check Docker logs: `docker-compose logs`
   - Ensure all dependencies are correctly listed in requirments.txt

2. **Browser automation fails**:
   - Verify Xvfb is running in the container
   - Check if all browser dependencies are installed

3. **API returns errors**:
   - Examine the application logs for specific error messages
   - Verify the input parameters are correctly formatted

## Development

To make changes to the application while running in Docker:

1. The docker-compose.yml file mounts the current directory as a volume
2. Changes to Python files will be reflected in the container
3. The server runs with reload=True, so most changes take effect immediately

## Additional Notes

- The container exposes port 8000, make sure it's not in use on your host machine
- The scraper uses a non-headless browser with Xvfb, which consumes more resources than a headless setup
- For production deployment, consider adding proper error handling and logging