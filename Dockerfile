FROM python:3.11-slim

# Install system dependencies for scapy
RUN apt-get update && apt-get install -y \
    tcpdump \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create attacks directory if it doesn't exist
RUN mkdir -p attacks

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
