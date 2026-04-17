# Patch webdriver.Chrome to always run headless on server deployments
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

_OriginalChrome = webdriver.Chrome


class _HeadlessChrome(_OriginalChrome):
    def __init__(self, *args, **kwargs):
        if 'options' not in kwargs:
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--window-size=1920,1080")
            kwargs['options'] = opts
        super().__init__(*args, **kwargs)


webdriver.Chrome = _HeadlessChrome
