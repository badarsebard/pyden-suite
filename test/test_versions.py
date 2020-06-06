from .drivers import splunk
import time


def test_create_dist_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_dist_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.7.0")
    assert "Successfully compiled Python 3.7.0" in results


def test_create_dist_version_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_dist_version_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.7.0")
    assert "Version already exists" in results


def test_delete_dist_success(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_dist_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| pydelete 3.7.0")
    assert "Successfully deleted dist 3.7.0" in results


def test_delete_dist_version_not_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_dist_version_not_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| pydelete 3.7.0")
    assert "Version or environment 3.7.0 not found in configuration" in results


def test_create_dist_ui_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_dist_ui_success")
    splunk_test.open_pyden_versions()
    icon = browser.find_element_by_class_name("icon-plus-circle")
    icon.click()
    i = 0
    while "icon-minus-circle" not in icon.get_attribute("class") and i < 300:
        time.sleep(1)
        i += 1
    assert i < 300


def test_delete_dist_ui_success(browser):
    splunk_test = splunk.SplunkTest(browser, "delete_dist_ui_success")
    splunk_test.open_pyden_versions()
    icon = browser.find_element_by_class_name("icon-minus-circle")
    icon.click()
    i = 0
    while "icon-plus-circle" not in icon.get_attribute("class") and i < 300:
        time.sleep(1)
        i += 1
    assert i < 300