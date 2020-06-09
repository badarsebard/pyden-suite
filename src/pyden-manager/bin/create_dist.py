import sys
import os
import tarfile
import json
import subprocess
from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
from splunk_logger import setup_logging
import shutil
from utils import load_pyden_config, write_pyden_config, get_proxies


def download_python(version, build_path):
    base_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                             sessionKey=session_key)[1].decode()
    try:
        dpr = requests.get(base_url + "{0}/".format(version), proxies=proxies)
    except Exception as ex:
        Intersplunk.generateErrorResults("Exception thrown getting python: ({0}, {1})".format(type(ex), ex))
        sys.exit(1)
    else:
        if dpr.status_code in range(200, 300):
            python_link = [link for link in re.findall("href=\"(.*?)\"", dpr.content.decode()) if link.endswith('tgz')][0]
            dpr = requests.get(base_url + "{0}/{1}".format(version, python_link), proxies=proxies)
        else:
            Intersplunk.generateErrorResults(
                "Failed to reach www.python.org. Request returned - Status code: {0}, Response: {1}".format(
                    dpr.status_code, dpr.text))
            sys.exit(1)
    if dpr.status_code in range(200, 300):
        # save
        build_file = os.path.join(build_path, "Python-{0}.tgz".format(version))
        with open(build_file, "wb") as download:
            download.write(dpr.content)
    else:
        Intersplunk.generateErrorResults(
            "Failed to download python. Request returned - Status code: {0}, Response: {1}".format(dpr.status_code,
                                                                                                   dpr.text))
        sys.exit(1)
    return build_file


def build_dist(version, download):
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    if version in config.sections():
        Intersplunk.generateErrorResults("Version already exists.")
        sys.exit(1)
    build_path = os.path.join(os.getcwd(), 'build')
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
    if download is True:
        logger.debug("Downloading Python")
        build_file = download_python(version, build_path)
    else:
        logger.debug("Using existing archive")
        build_file = os.path.join(build_path, download)

    # unpack
    if os.path.isdir(build_file[:-4]):
        shutil.rmtree(build_file[:-4], ignore_errors=True)
    os.chdir(build_path)
    # this was some dumb code
    # list_before_extraction = os.listdir(os.getcwd())
    logger.debug("Extracting archive")
    with tarfile.open(build_file, "r:gz") as tarball:
        extracted_members = tarball.getnames()
        for extracted_member in extracted_members:
            if extracted_members[0] not in extracted_member:
                Intersplunk.generateErrorResults(
                    "Archive contained more than one item. Please use archive with single member.")
                sys.exit(1)
        extracted_member = extracted_members[0]
        tarball.extractall()

    # configure and build
    pyden_prefix = os.path.join(pyden_location, 'local', 'lib', 'dist', version)
    if not os.path.isdir(pyden_prefix):
        os.makedirs(pyden_prefix)
    os.chdir(os.path.join(os.getcwd(), extracted_member))
    optimize_conf = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/appsettings/optimize",
                                  sessionKey=session_key)[1].decode()
    optimize = '--enable-optimizations' if optimize_conf in ['true', 'True', '1', 1] else ''
    # remove environment variables. needed to use host libraries instead of splunk's built-in.
    os.environ.pop('LD_LIBRARY_PATH', None)
    os.environ.pop('OPENSSL_CONF', None)
    os.environ.pop('PYTHONPATH', None)
    logger.debug("Configuring source")
    configure = subprocess.Popen([os.path.join(os.curdir, 'configure'),
                                  optimize,
                                  '--with-ensurepip=install',
                                  '--prefix={0}'.format(pyden_prefix)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True, env=os.environ)
    result, error = configure.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    if configure.returncode != 0:
        sys.exit(1)
    logger.debug("Making")
    make = subprocess.Popen(['make', '-j', '8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                            env=os.environ)
    result, error = make.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    if make.returncode != 0:
        sys.exit(1)
    logger.debug("Make install")
    install = subprocess.Popen(['make', 'altinstall'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True, env=os.environ)
    result, error = install.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    if install.returncode != 0:
        sys.exit(1)
    logger.debug("Determining binary of {}".format(pyden_prefix))
    bin_dir = os.path.join(pyden_prefix, 'bin')
    os.chdir(bin_dir)
    largest_size = 0
    py_exec = ""
    bins = os.listdir(bin_dir)
    for binary in bins:
        bin_size = os.path.getsize(binary)
        if bin_size > largest_size:
            py_exec = os.path.join(bin_dir, binary)
            largest_size = bin_size
    logger.debug("Found binary: {}".format(py_exec))

    # Running get-pip and others
    logger.debug("Upgrading pip")
    if proxies:
        os.environ['HTTP_PROXY'] = proxies['http']
        os.environ['HTTPS_PROXY'] = proxies['https']
    pip = subprocess.Popen([py_exec, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=os.environ)
    result, error = pip.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    pip = subprocess.Popen([py_exec, '-m', 'pip', 'install', 'virtualenv'], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True, env=os.environ)
    result, error = pip.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    logger.info("Finished building Python {}. Distribution available at {}.".format(version, pyden_prefix))

    # reloading config at last second to avoid race conditions during parallel processing
    pm_config, config = load_pyden_config()
    write_pyden_config(pyden_location, config, version, "executable", py_exec.lstrip(os.environ['SPLUNK_HOME']))
    if not config.has_section("default-pys") or not config.has_option("default-pys", "distribution"):
        write_pyden_config(pyden_location, config, 'default-pys', 'distribution', version)
    Intersplunk.outputResults([{"message": "Successfully compiled Python {}".format(version)}])
    return


if __name__ == "__main__":
    logger = setup_logging()
    download_arg = True
    settings = dict()
    if "--cli" in sys.argv:
        session_key = sys.stdin.read()
    else:
        Intersplunk.readResults(settings=settings)
        session_key = settings['sessionKey']
    proxies = get_proxies(session_key)
    latest_python_search = r"""
    | getversions 
    | rex field=version "(?<v_M>\d+)\.(?<v_m>\d+)\.(?<v_mm>\d+)" 
    | eval v_M=tonumber(v_M), v_m=tonumber(v_m), v_mm=tonumber(v_mm) 
    | sort -v_M, -v_m, -v_mm 
    | table version 
    | head 1
    """
    try:
        r = simpleRequest("/servicesNS/nobody/pyden-manager/search/jobs",
                          postargs={'search': latest_python_search, 'exec_mode': 'oneshot', 'output_mode': 'json'},
                          sessionKey=session_key)
        dist_version = json.loads(r[1])['results'][0]['version']
    except Exception as e:
        Intersplunk.generateErrorResults("Failed to find latest version of Python: {}.".format(e))
        sys.exit(1)
    for arg in sys.argv:
        if "version" in arg:
            dist_version = arg.split("=")[1]
        if "download" in arg:
            download_arg = arg.split("=")[1]
    logger.info("Creating Python distribution version {}".format(dist_version))
    build_dist(dist_version, download_arg)
