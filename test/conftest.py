import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from drivers import splunk
import time


class BrowserStartFailure:
    pass


def wait_until(browser: webdriver.Chrome, url: str):
    WebDriverWait(browser, 10).until(expected_conditions.url_contains(url))


@pytest.fixture()
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    splunk_test = splunk.SplunkTest(driver)
    splunk_test.screenshot("browser_startup-1.png")
    i = 0
    while not driver.get_cookie("splunkweb_uid"):
        driver.get("http://pyden-splunk:8000")
        time.sleep(1)
        if i > 120:
            print("Problem loading login screen")
            raise BrowserStartFailure
        i += 1
    driver.find_element_by_id("username").send_keys("admin")
    driver.find_element_by_id("password").send_keys("changeme1")
    driver.find_element_by_class_name("splButton-primary").click()
    wait_until(driver, "/en-US/app/launcher/home")
    splunk_test.screenshot("browser_startup-2.png")
    driver.find_element_by_class_name("btn-save").click()
    driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div[3]/button[1]").click()
    yield driver
    driver.quit()
