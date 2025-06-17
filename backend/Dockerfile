FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY app/ /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]