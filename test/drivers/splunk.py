import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def wait_until(browser: webdriver.Chrome, url: str):
    WebDriverWait(browser, 20).until(expected_conditions.url_contains(url))


class TestFailure(Exception):
    pass


class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.
    locator - used to find the element
    returns the WebElement once it has the particular css class
    """
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


def _screenshot(func):
    def wrapper(self, *args):
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
        full_pic_name = os.path.join(os.environ['CI_PROJECT_DIR'], "screenshots",
                                     f"{self.pic_name}-{self.count}.png")
        self.browser.save_screenshot(full_pic_name)
        self.count += 1

    def open_pyden(self, url):
        self.browser.get(f"http://pyden-splunk:8000/en-US/app/pyden-manager/{url}")
        wait_until(self.browser, f"/en-US/app/pyden-manager/{url}")

    @_screenshot
    def open_pyden_search(self):
        self.open_pyden("search")

    @_screenshot
    def open_pyden_versions(self):
        self.open_pyden("versions")
        wait = WebDriverWait(self.browser, 30)
        wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "icon-plus-circle")))

    @_screenshot
    def open_pyden_environments(self):
        self.open_pyden("virtual_environments")

    @_screenshot
    def open_pyden_pypi(self):
        self.open_pyden("pypi_hub")

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
