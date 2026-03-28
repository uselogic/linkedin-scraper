FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and dependencies
RUN playwright install-deps chromium
RUN playwright install chromium

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p "linkedin text" "linkedin image" "linkedin video" "texts"

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "app.py"]
