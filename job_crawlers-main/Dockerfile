FROM python:3.11-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip \
    libglib2.0-0 libnss3 libfontconfig1 libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 \
    libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    libgbm1 libgtk-3-0 libasound2 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver
RUN CHROME_VER=$(google-chrome --version | grep -oP '[\d.]+') \
    && CHROME_MAJOR=$(echo $CHROME_VER | cut -d. -f1) \
    && DRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" \
        | python3 -c "
import sys, json
data = json.load(sys.stdin)
versions = [v for v in data['versions'] if v['version'].startswith('$(echo $CHROME_VER | cut -d. -f1).')]
dls = versions[-1]['downloads'].get('chromedriver', [])
print([x['url'] for x in dls if 'linux64' in x['url']][0])
") \
    && wget -q "$DRIVER_URL" -O /tmp/chromedriver.zip \
    && unzip -q /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver*

WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
