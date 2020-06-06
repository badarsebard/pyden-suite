from .drivers import splunk
import time


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.6.0")
    assert "Successfully compiled Python 3.6.0" in results
    results = splunk_test.run_search("| createvenv name=py-env-0 version=3.6.0")
    assert "Successfully created virtual environment py-env-0 using Python 3.6.0" in results


def test_create_venv_name_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_name_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.6.1")
    assert "Successfully compiled Python 3.6.1" in results
    results = splunk_test.run_search("| createvenv name=py-env-1 version=3.6.1")
    assert "Successfully created virtual environment py-env-1 using Python 3.6.1" in results
    results = splunk_test.run_search("| createvenv name=py-env-1 version=3.6.1")
    assert "Virtual environment name py-env-1 already exists" in results


def test_create_venv_version_not_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_version_not_exists")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createvenv name=py-env-2 version=3.6.2")
    assert "Python version not found in pyden.conf" in results
