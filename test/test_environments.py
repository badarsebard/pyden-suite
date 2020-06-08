from .drivers import splunk
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.8.0")
    assert "Successfully compiled Python 3.8.0" in results
    results = splunk_test.run_search("| createvenv name=py-env-0 version=3.8.0")
    assert "Successfully created virtual environment py-env-0 using Python 3.8.0" in results


def test_create_venv_no_name(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_no_name")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createvenv version=3.8.0")
    assert "No name for the new environment was provided." in results


def test_create_venv_name_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_name_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createvenv name=py-env-0 version=3.8.0")
    assert "Virtual environment name py-env-0 already exists" in results


def test_create_venv_version_not_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_version_not_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createvenv name=py-env-1 version=4.0")
    assert "Python version not found in pyden.conf" in results


def test_create_venv_ui_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_ui_success")
    splunk_test.open_pyden_environments()
    text_box = browser.find_element_by_xpath('//*[@id="input1"]/div/div/input')
    text_box.send_keys(Keys.CONTROL, "a")
    text_box.send_keys(Keys.DELETE)
    text_box.send_keys("py-env-1")
    text_box.send_keys(Keys.ENTER)
    table = browser.find_element_by_id("statistics")
    while "py-env-1" not in table.text:
        time.sleep(1)
    dropdown = browser.find_element_by_xpath('//*[@id="input2"]/div/div[1]/div/div')
    dropdown.click()
    option = browser.find_element_by_xpath('//button[@value="3.8.0"]')
    option.click()
    button = browser.find_element_by_class_name("icon-plus-circle")
    button.click()
    while "form.env_name" not in browser.current_url:
        time.sleep(1)
    table = browser.find_element_by_id("statistics")
    while "py-env-1" not in table.text:
        time.sleep(1)
    splunk_test.screenshot()
    assert "py-env-1" in table.text


def test_delete_venv_ui_success(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_venv_ui_success")
    splunk_test.open_pyden_environments()
    rows = browser.find_elements_by_xpath('//*[@id="statistics"]/table/tbody/tr')
    button = None
    for i, row in enumerate(rows):
        if "py-env-1" in row.text:
            xpath = f'//*[@id="statistics"]/table/tbody/tr[{i+1}]/td[1]/i'
            button = browser.find_element_by_xpath(xpath)
            break
        splunk_test.screenshot()
    if not button:
        print("Couldn't find correct button")
    button.click()
    splunk_test.screenshot()
    while "form.env_name" not in browser.current_url:
        time.sleep(1)
        splunk_test.screenshot()
    table = browser.find_element_by_id("statistics")
    while "Create new environment" not in table.text:
        time.sleep(1)
        splunk_test.screenshot()
    table = browser.find_element_by_id("statistics")
    splunk_test.screenshot()
    assert "py-env-1" not in table.text


def test_delete_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_venv_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| pydelete py-env-0")
    assert "Successfully deleted venv py-env-0" in results


def test_delete_venv_name_not_exist(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_venv_name_not_exist")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| pydelete py-env-0")
    assert "Version or environment py-env-0 not found in configuration" in results


def test_view_venv_module_success(browser):
    splunk_test = splunk.SplunkTest(browser, "add_venv_module_success")
    splunk_test.open_pyden_search()
    splunk_test.run_search("| createvenv name=py-env-2 version=3.8.0")
    splunk_test.run_search("| pip environment=py-env-2 install requests")
    splunk_test.open_pyden_environments()
    environments = browser.find_elements_by_xpath('//*[@id="statistics"]/table/tbody/tr')
    environment = None
    for i, env in enumerate(environments):
        if "py-env-2" in env.text:
            xpath = f'//*[@id="statistics"]/table/tbody/tr[{i + 1}]/td[2]'
            environment = browser.find_element_by_xpath(xpath)
            break
    if not environment:
        print("Couldn't find correct environment")
    environment.click()
    splunk_test.screenshot()
    progress = False
    while not progress:
        try:
            progress = browser.find_elements_by_class_name("progress-animation")[1]
        except IndexError:
            progress = False
    while "display: none" not in progress.get_attribute("style"):
        time.sleep(1)
    assert "requests" in browser.page_source
