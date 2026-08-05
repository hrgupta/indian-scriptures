# Indian Scriptures — data pipeline (scrape → process)
#
# Multi-platform: python:3.14-slim publishes linux/amd64 and linux/arm64
# images, and every dependency (scrapy, pandas, numpy, jupyter) ships
# wheels for both architectures — the same Dockerfile builds identically
# on Intel and Apple Silicon.

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The spiders resolve their FEEDS output paths relative to
# scriptures/spiders/ (../../data/raw/...)
WORKDIR /app/scriptures/spiders

# Default: run the full refresh pipeline (spiders, then notebooks)
ENTRYPOINT ["/app/docker-entrypoint.sh"]
