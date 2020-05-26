import splunk


def test_login(browser):
    splunk_test = splunk.SplunkTest(browser)
    splunk_test.login()
    assert "Home | Splunk" in browser.title


def test_create_dist(browser):
    splunk_test = splunk.SplunkTest(browser)
    splunk_test.login()
    splunk_test.open_pyden()
    splunk_test.screenshot("create_dist_1.png")
    assert "Search | Splunk" in browser.title
