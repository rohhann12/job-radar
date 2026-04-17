#!/bin/bash
set -e

CHROME_VER=$(google-chrome --version | grep -oP '[\d.]+')
CHROME_MAJOR=$(echo $CHROME_VER | cut -d. -f1)

DRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
versions = [v for v in data['versions'] if v['version'].split('.')[0] == '$CHROME_MAJOR']
dls = versions[-1]['downloads'].get('chromedriver', [])
print([x['url'] for x in dls if 'linux64' in x['url']][0])
")

wget -q "$DRIVER_URL" -O /tmp/chromedriver.zip
unzip -q /tmp/chromedriver.zip -d /tmp/
mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf /tmp/chromedriver*
