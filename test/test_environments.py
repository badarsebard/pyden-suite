from .drivers import splunk


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_success")
    splunk_test.open_pyden_search()
    results = splunk_test.run_search("| createdist version=3.8.0")
    assert "Successfully compiled Python 3.8.0" in results
    splunk_test.run_search("| getvenvs")
    results = splunk_test.run_search("| createvenv name=py-env-0 version=3.8.0")
    assert "Successfully created virtual environment py-env-0 using Python 3.8.0" in results


def test_create_venv_name_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_name_exists")
    splunk_test.open_pyden_search()
    splunk_test.run_search("| getvenvs")
    results = splunk_test.run_search("| createvenv name=py-env-0 version=3.8.0")
    assert "Virtual environment name py-env-0 already exists" in results
    splunk_test.run_search("| getvenvs")


def test_create_venv_version_not_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_version_not_exists")
    splunk_test.open_pyden_search()
    splunk_test.run_search("| getvenvs")
    results = splunk_test.run_search("| createvenv name=py-env-1 version=3.8.1")
    assert "Python version not found in pyden.conf" in results
    splunk_test.run_search("| getvenvs")
