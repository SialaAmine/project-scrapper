FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Xvfb and browser dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirments.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy application code
COPY . .

# Create a script to run the application with Xvfb
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1280x720x16 &\nexport DISPLAY=:99\nexec "$@"' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run the FastAPI server
CMD ["python", "flask_server.py"]