FROM python:3.11-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip \
    libglib2.0-0 libnss3 libfontconfig1 libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 \
    libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    libgbm1 libgtk-3-0 libasound2 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (modern GPG method for Debian 12+)
RUN wget -q -O /usr/share/keyrings/google-chrome.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver via helper script
COPY install_chromedriver.sh /tmp/install_chromedriver.sh
RUN chmod +x /tmp/install_chromedriver.sh && /tmp/install_chromedriver.sh

WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
