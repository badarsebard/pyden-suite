import splunk


def test_create_dist_success(browser):
    splunk_test = splunk.SplunkTest(browser)
    results = splunk_test.run_search("""| getversions | lookup versionstatus version | where version="3.8.0" AND status>0""")
    if "Statistics (1)" in results:
        # version already exists, remove and try again
        assert False
    results = splunk_test.run_search("| createdist version=3.8.0")
    splunk_test.screenshot("create_dist_success_1.png")
    assert "Successfully compiled Python 3.8.0" in results


def test_create_dist_version_exists(browser):
    splunk_test = splunk.SplunkTest(browser)
    results = splunk_test.run_search("""| getversions | lookup versionstatus version | where version="3.8.0" AND status>0""")
    if "Statistics (0)" in results:
        results = splunk_test.run_search("| createdist version=3.8.0")
        assert "Successfully compiled Python 3.8.0"
    results = splunk_test.run_search("| createdist version=3.8.0")
    splunk_test.screenshot("create_dist_version_exists_1.png")
    assert "Version already exists" in results


def test_create_venv_success(browser):
    splunk_test = splunk.SplunkTest(browser)
    results = splunk_test.run_search("""| getversions | lookup versionstatus version | where version="3.8.1" AND status>0""")
    if "Statistics (0)" in results:
        results = splunk_test.run_search("| createdist version=3.8.1")
        splunk_test.screenshot("create_venv_success_0.png")
        assert "Successfully compiled Python 3.8.1" in results
    results = splunk_test.run_search("| createvenv name=py3 version=3.8.1")
    splunk_test.screenshot("create_venv_success_1.png")
    assert "Successfully created virtual environment py3 using Python 3.8.1" in results
