from drivers import splunk


def test_create_dist_success(browser):
    splunk_test = splunk.SplunkTest(browser)
    splunk_test.screenshot("create_dist_success-1.png")
    splunk_test.open_pyden_search()
    splunk_test.screenshot("create_dist_success-2.png")
    spl = """| getversions | lookup versionstatus version | where version="3.8.0" AND status>0"""
    results = splunk_test.run_search(spl)
    splunk_test.screenshot("create_dist_success-3.png")
    if "Statistics (0)" in results:
        assert True
    results = splunk_test.run_search("| createdist version=3.8.0")
    splunk_test.screenshot("create_dist_success-4.png")
    assert "Successfully compiled Python 3.8.0" in results


def test_create_dist_version_exists(browser):
    splunk_test = splunk.SplunkTest(browser)
    splunk_test.screenshot("create_dist_version_exists-1.png")
    splunk_test.open_pyden_search()
    splunk_test.screenshot("create_dist_version_exists-2.png")
    spl = """| getversions | lookup versionstatus version | where version="3.8.0" AND status>0"""
    results = splunk_test.run_search(spl)
    splunk_test.screenshot("create_dist_version_exists-3.png")
    if "Statistics (1)" in results:
        assert True
    results = splunk_test.run_search("| createdist version=3.8.0")
    splunk_test.screenshot("create_dist_version_exists-4.png")
    assert "Version already exists" in results


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser)
    splunk_test.screenshot("create_venv_success-1.png")
    splunk_test.open_pyden_search()
    splunk_test.screenshot("create_venv_success-2.png")
    spl = """| getversions | lookup versionstatus version | where version="3.8.1" AND status>0"""
    results = splunk_test.run_search(spl)
    splunk_test.screenshot("create_venv_success-3.png")
    if "Statistics (0)" in results:
        results = splunk_test.run_search("| createdist version=3.8.1")
        splunk_test.screenshot("create_venv_success-3a.png")
        assert "Successfully compiled Python 3.8.1" in results
    results = splunk_test.run_search("| createvenv name=py3 version=3.8.1")
    splunk_test.screenshot("create_venv_success-4.png")
    assert "Successfully created virtual environment py3 using Python 3.8.1" in results
