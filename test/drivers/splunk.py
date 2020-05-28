from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def wait_until(browser: webdriver.Chrome, url: str):
    WebDriverWait(browser, 10).until(expected_conditions.url_contains(url))


class TestFailure(Exception):
    pass


class SplunkTest:
    def __init__(self, browser: webdriver.Chrome):
        self.browser = browser

    def login(self):
        if self.browser.get_cookie("splunkd_8000"):
            return
        i = 0
        while True:
            self.browser.get("http://pyden-splunk:8000")
            session_cookie = self.browser.get_cookie("splunkweb_uid")
            time.sleep(1)
            if session_cookie:
                break
            if i > 120:
                print("Problem loading login screen")
                raise TestFailure
            i += 1
        self.screenshot("fml.png")
        self.browser.find_element_by_id("username").send_keys("admin")
        self.browser.find_element_by_id("password").send_keys("changeme1")
        self.browser.find_element_by_class_name("splButton-primary").click()
        wait_until(self.browser, "/en-US/app/launcher/home")

    def open_pyden(self):
        session_cookie = self.browser.get_cookie("splunkd_8000")
        if not session_cookie:
            self.login()
        self.browser.get("http://pyden-splunk:8000/en-US/app/pyden-manager/search")
        wait_until(self.browser, "/en-US/app/pyden-manager/search")

    def run_search(self, spl: str):
        if "pyden-manager/search" not in self.browser.current_url:
            self.open_pyden()
        search_bar = self.browser.find_element_by_class_name("ace_text-input")
        search_bar.send_keys(Keys.CONTROL, "a")
        search_bar.send_keys(Keys.DELETE)
        search_bar.send_keys(spl)
        self.browser.find_element_by_class_name("search-button").click()
        stop_button = self.browser.find_element_by_class_name("stop")
        while "disabled" not in stop_button.get_attribute("class"):
            time.sleep(1)
        return self.browser.page_source

    def screenshot(self, target):
        self.browser.save_screenshot(f"/app/screenshots/{target}")
