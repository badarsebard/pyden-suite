import sys
import os
import tarfile
from subprocess import call
from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
from splunk_logger import setup_logging
import shutil
from utils import load_pyden_config, write_pyden_config


def download_python(version, session_key, build_path):
    base_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                             sessionKey=session_key)[1]
    try:
        r = requests.get(base_url + "{0}/".format(version))
    except Exception as ex:
        Intersplunk.generateErrorResults("Exception thrown getting python: ({0}, {1})".format(type(ex), ex))
        sys.exit(1)
    else:
        if r.status_code in range(200, 300):
            python_link = [link for link in re.findall("href=\"(.*?)\"", r.content) if link.endswith('tgz')][0]
            r = requests.get(base_url + "{0}/{1}".format(version, python_link))
        else:
            Intersplunk.generateErrorResults(
                "Failed to reach www.python.org. Request returned - Status code: {0}, Response: {1}".format(
                    r.status_code, r.text))
            sys.exit(1)
    if r.status_code in range(200, 300):
        # save
        build_file = os.path.join(build_path, "Python-{0}.tgz".format(version))
        with open(build_file, "w") as download:
            download.write(r.content)
    else:
        Intersplunk.generateErrorResults(
            "Failed to download python. Request returned - Status code: {0}, Response: {1}".format(r.status_code,
                                                                                                   r.text))
        sys.exit(1)
    return build_file


def build_dist(version, download):
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']
    pyden_location, config = load_pyden_config()
    if version in config.sections():
        Intersplunk.generateErrorResults("Version already exists.")
        sys.exit(1)
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    build_path = os.path.join(os.getcwd(), 'build')
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
    if download is True:
        logger.debug("Downloading Python")
        build_file = download_python(version, session_key, build_path)
    else:
        logger.debug("Using existing archive")
        build_file = os.path.join(build_path, download)

    # unpack
    if os.path.isdir(build_file[:-4]):
        shutil.rmtree(build_file[:-4], ignore_errors=True)
    os.chdir(build_path)
    list_before_extraction = os.listdir(os.getcwd())
    logger.debug("Extracting archive")
    with tarfile.open(build_file, "r:gz") as tarball:
        tarball.extractall()
    list_after_extraction = os.listdir(os.getcwd())
    extracted_members = [member for member in list_after_extraction if member not in list_before_extraction]
    if len(extracted_members) == 1:
        extracted_member = extracted_members[0]
    else:
        Intersplunk.generateErrorResults("Archive contained more than one item. Please use archive with single member.")
        sys.exit(1)

    # configure and build
    pyden_prefix = os.path.join(pyden_location, 'local', 'lib', 'dist', version)
    if not os.path.isdir(pyden_prefix):
        os.makedirs(pyden_prefix)
    os.chdir(os.path.join(os.getcwd(), extracted_member))
    optimize_conf = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/app/optimize",
                                  sessionKey=session_key)[1]
    optimize = '--enable-optimizations' if optimize_conf in ['true', 'True', '1'] else ''
    logger.debug("Configuring source")
    call([os.path.join(os.curdir, 'configure'),
          optimize,
          '--with-ensurepip=install',
          '--prefix={0}'.format(pyden_prefix)])
    logger.debug("Making")
    call(['make'])
    logger.debug("Make install")
    call(['make', 'altinstall'])

    logger.debug("Determining binary of %s" % pyden_prefix)
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
    logger.debug("Found binary: %s" % py_exec)

    # Running get-pip and others
    logger.debug("Upgrading pip")
    call([py_exec, '-m', 'pip', 'install', '--upgrade', 'pip'])
    if version < '3':
        call([py_exec, '-m', 'pip', 'install', 'virtualenv'])
    logger.info("Finished building Python %s. Distribution available at %s." % (version, pyden_prefix))

    write_pyden_config(pyden_location, version, py_exec)
    return


if __name__ == "__main__":
    logger = setup_logging()
    download_arg = True
    dist_version = "3.7.1"  # latest version as of authoring
    for arg in sys.argv:
        if "version" in arg:
            dist_version = arg.split("=")[1]
        if "download" in arg:
            download_arg = arg.split("=")[1]
    logger.info("Creating Python distribution version %s" % dist_version)
    build_dist(dist_version, download_arg)
