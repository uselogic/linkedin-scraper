FROM mcr.microsoft.com/playwright/python:latest

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
