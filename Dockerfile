FROM python:3.11-slim

# Install system dependencies (needed for pymupdf and nltk)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download nltk stopwords
RUN python -m nltk.downloader stopwords

# Copy the rest of the code
COPY . .

# Run script
CMD ["python", "scrape_open_core.py"]
