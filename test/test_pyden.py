from .drivers import splunk


def test_create_dist_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_dist_success")
    splunk_test.login()
    splunk_test.open_pyden_search()
    spl = """| getversions | lookup versionstatus version | where version="3.8.0" AND status>0"""
    results = splunk_test.run_search(spl)
    if "Statistics (0)" in results:
        assert True
    results = splunk_test.run_search("| createdist version=3.8.0")
    assert "Successfully compiled Python 3.8.0" in results


def test_create_dist_version_exists(browser):
    splunk_test = splunk.SplunkTest(browser, "create_dist_version_exists")
    splunk_test.login()
    splunk_test.open_pyden_search()
    spl = """| getversions | lookup versionstatus version | where version="3.8.0" AND status>0"""
    results = splunk_test.run_search(spl)
    if "Statistics (1)" in results:
        assert True
    results = splunk_test.run_search("| createdist version=3.8.0")
    assert "Version already exists" in results


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser, "create_venv_success")
    splunk_test.login()
    splunk_test.open_pyden_search()
    spl = """| getversions | lookup versionstatus version | where version="3.8.1" AND status>0"""
    results = splunk_test.run_search(spl)
    if "Statistics (0)" in results:
        results = splunk_test.run_search("| createdist version=3.8.1")
        assert "Successfully compiled Python 3.8.1" in results
    results = splunk_test.run_search("| createvenv name=py3 version=3.8.1")
    assert "Successfully created virtual environment py3 using Python 3.8.1" in results
