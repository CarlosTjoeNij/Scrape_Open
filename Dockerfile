FROM python:3.10-slim

WORKDIR /app

# System packages for jobspy / lxml / playwright
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libgl1 \
    libglib2.0-0 \
    python3-dev \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run scraper
CMD ["python", "scrape_open_core.py"]
