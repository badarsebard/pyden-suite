from .drivers import splunk
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


def test_pypi_install_success(browser):
    splunk_test = splunk.SplunkTest(browser, "pypi_install_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.8.2")
    assert "Successfully compiled Python 3.8.2" in results
    results = splunk_test.run_search("| createvenv name=pypi-env-0 version=3.8.2")
    assert "Successfully created virtual environment pypi-env-0 using Python 3.8.2" in results
    splunk_test.open_pyden_pypi()
    textbox = browser.find_element_by_xpath('//*[@id="input1"]/div/div/input')
    textbox.send_keys(Keys.CONTROL, "a")
    textbox.send_keys(Keys.DELETE)
    textbox.send_keys("requests")
    textbox.send_keys(Keys.ENTER)
    splunk_test.screenshot()
    while "Waiting for data" in browser.page_source:
        time.sleep(1)
    table = browser.find_element_by_xpath('//*[@id="statistics"]/table')
    while table.text == "":
        time.sleep(1)
    splunk_test.screenshot()
    assert "requests" in table.text
    cell = browser.find_element_by_xpath('//*[@id="statistics"]/table/tbody/tr/td')
    cell.click()
    splunk_test.screenshot()
    description = browser.find_element_by_id("description")
    while '<div class="panel-body html"></div>' == description.get_attribute("innerHTML"):
        time.sleep(1)
    splunk_test.screenshot()
    assert "is an elegant and simple HTTP library for Python" in browser.page_source
    splunk_test.screenshot()
    dropdown = browser.find_element_by_xpath('//*[@id="venv"]/div/div/div/div/button')
    dropdown.click()
    splunk_test.screenshot()
    option = browser.find_element_by_xpath('//button[@value="pypi-env-0"]')
    option.click()
    splunk_test.screenshot()
    time.sleep(1)
    install = browser.find_element_by_xpath('//*[@id="submit"]')
    install.click()
    splunk_test.screenshot()
    done = False
    i = 0
    while not done and i < 60:
        try:
            done = browser.find_element_by_id("done_icon")
        except NoSuchElementException:
            pass
    splunk_test.screenshot()
    assert "icon-check-circle" in done.get_attribute("innerHTML")
