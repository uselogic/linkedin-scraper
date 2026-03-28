FROM python:3.11-slim

WORKDIR /app

# Install basic tools needed by Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser and all its system dependencies automatically
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p "linkedin text" "linkedin image" "linkedin video" "texts"

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "app.py"]
