from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
from splunk_logger import setup_logging
from utils import get_proxies


if __name__ == "__main__":
    logger = setup_logging()
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']
    proxies = get_proxies(session_key)
    download_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                                 sessionKey=session_key)[1]
    r = requests.get(download_url, proxies=proxies)
    version_pattern = r"""<a href\=\"\d(?:\.\d{1,2}){1,2}\/\"\>(?P<version>\d(?:\.\d{1,2}){1,2})"""
    all_versions = re.findall(version_pattern, r.text)
    # logger.debug(all_versions)
    compatible_versions = [version for version in all_versions if (version.startswith('2') and version > '2.7') or (
                version.startswith('3') and version > '3.5')]
    # logger.debug(compatible_versions)
    # sometime there are only pre release or release candidates so we need to check each compatible version for release
    for version in compatible_versions:
        url = download_url.rstrip().decode() + "{}/".format(version)
        logger.debug(url)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'}, proxies=proxies)
        source_pattern = r"""<a href=\"(?P<link>.*)\">Python-%s.tgz""" % version.replace('.', '\\.')
        # logger.debug(source_pattern)
        # logger.debug(r.text)
        match = re.findall(source_pattern, r.text)
        # logger.debug(match)
        if not match:
            # logger.debug(version)
            compatible_versions.remove(version)
    # logger.debug(compatible_versions)
    results = [{'version': version} for version in compatible_versions]
    Intersplunk.outputResults(results)
