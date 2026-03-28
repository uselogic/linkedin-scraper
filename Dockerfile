FROM mcr.microsoft.com/playwright/python:latest
# Chromium and all system-level browser dependencies are pre-installed in this
# base image — do NOT run `playwright install --with-deps` here, as it will
# fail trying to install system packages (e.g. ttf-unifont) that are already
# present or unavailable in this environment.

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p "linkedin text" "linkedin image" "linkedin video" "texts"

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "app.py"]
