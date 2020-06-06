from .drivers.splunk import TestFailure
import os
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


class BrowserStartFailure:
    pass


@pytest.fixture()
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(60)
    if driver.get_cookie("splunkd_8000"):
        return
    i = 0
    while not driver.get_cookie("splunkweb_uid"):
        driver.get("http://pyden-splunk:8000")
        time.sleep(1)
        if i > 120:
            print("Problem loading login screen")
            raise TestFailure
        i += 1
    driver.find_element_by_id("username").send_keys("admin")
    driver.find_element_by_id("password").send_keys("changeme1")
    driver.find_element_by_class_name("splButton-primary").click()
    WebDriverWait(driver, 20).until(expected_conditions.url_contains("/en-US/app/launcher/home"))
    artifacts = os.path.join(os.environ['CI_PROJECT_DIR'], "artifacts")
    if not os.path.isdir(artifacts):
        os.makedirs(artifacts)
        os.makedirs(os.path.join(artifacts, "screenshots"))
        os.makedirs(os.path.join(artifacts, "results"))
    yield driver
    driver.quit()
