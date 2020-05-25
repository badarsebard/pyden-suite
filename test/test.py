import requests
from selenium import webdriver
import sys
import time


print("Waiting for Splunk to be ready")
i, waiting = 0, True
while waiting:
    r = requests.get("http://pyden-splunk:8000")
    if r.ok:
        waiting = False
    if i < 120:
        print("Splunk did not come up within 2 minutes")
        sys.exit(1)
    i += 1
    time.sleep(1)

print("Beginning automated tests")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://pyden-splunk:8000")
print(driver.title)
