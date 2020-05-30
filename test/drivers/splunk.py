from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def wait_until(browser: webdriver.Chrome, url: str):
    WebDriverWait(browser, 20).until(expected_conditions.url_contains(url))


class TestFailure(Exception):
    pass


def _screenshot(func):
    def wrapper(self, *args):
        self.screenshot()
        output = func(self, *args)
        self.screenshot()
        return output
    return wrapper


class SplunkTest:
    def __init__(self, browser: webdriver.Chrome, pic_name: str):
        self.browser = browser
        self.count = 0
        self.pic_name = pic_name

    def screenshot(self):
        self.browser.save_screenshot(f"/app/screenshots/{self.pic_name}-{self.count}.png")
        self.count += 1

    @_screenshot
    def login(self):
        if self.browser.get_cookie("splunkd_8000"):
            return
        i = 0
        while not self.browser.get_cookie("splunkweb_uid"):
            self.browser.get("http://pyden-splunk:8000")
            time.sleep(1)
            if i > 120:
                print("Problem loading login screen")
                raise TestFailure
            i += 1
        self.browser.find_element_by_id("username").send_keys("admin")
        self.browser.find_element_by_id("password").send_keys("changeme1")
        self.browser.find_element_by_class_name("splButton-primary").click()
        wait_until(self.browser, "/en-US/app/launcher/home")

    @_screenshot
    def open_pyden_search(self):
        self.browser.get("http://pyden-splunk:8000/en-US/app/pyden-manager/search")
        wait_until(self.browser, "/en-US/app/pyden-manager/search")

    @_screenshot
    def run_search(self, spl: str):
        search_bar = self.browser.find_element_by_class_name("ace_text-input")
        search_bar.send_keys(Keys.CONTROL, "a")
        search_bar.send_keys(Keys.DELETE)
        search_bar.send_keys(spl)
        self.browser.find_element_by_class_name("search-button").click()
        stop_button = self.browser.find_element_by_class_name("stop")
        while "disabled" not in stop_button.get_attribute("class"):
            time.sleep(1)
        return self.browser.page_source
