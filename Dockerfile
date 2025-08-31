# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories for uploads and outputs
RUN mkdir -p uploads outputs

# Set environment variables
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Command to run the application with Flask directly
CMD ["python", "web_app.py"]
