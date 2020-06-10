import os
import subprocess
import sys
from splunk_logger import setup_logging
if sys.version < '3':
    from ConfigParser import ConfigParser
    from StringIO import StringIO
else:
    from configparser import ConfigParser
    from io import StringIO


util_logger = setup_logging()


def load_pyden_config():
    util_logger.debug("Loading Pyden config")
    pm_config = ConfigParser()
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    util_logger.debug("Reading config from btool")
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    buf = StringIO(proc_out.decode())
    pm_config.readfp(buf)
    util_logger.debug("Grabbing config attributes like location")
    pyden_location = pm_config.get('appsettings', 'location')
    local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([local_conf])
    util_logger.debug("Returning writable config object")
    return pm_config, config


def write_pyden_config(pyden_location, config, stanza, attribute, value):
    local_conf = os.path.join(pyden_location, 'local', 'pyden.conf')
    local_dir = os.path.dirname(local_conf)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    if not config.has_section(stanza):
        config.add_section(stanza)
    config.set(stanza, attribute, value)
    with open(local_conf, 'w') as f:
        config.write(f)


def get_proxies(session_key):
    import splunk.entity as entity
    util_logger.debug("Getting proxy settings")
    myapp = 'pyden-manager'
    user = ""
    password = ""
    util_logger.debug("Getting proxy password")
    try:
        entities = entity.getEntities(['admin', 'passwords'], namespace=myapp, owner='nobody', sessionKey=session_key)
    except Exception as e:
        util_logger.error("Could not obtain proxy credentials")
        raise Exception("Could not get %s credentials from splunk. Error: %s" % (myapp, str(e)))

    for i, c in entities.items():
        if 'pyden' in i:
            user, password = c['username'], c['clear_password']

    auth = "%s:%s@" % (user, password) if user else ""
    proxy = load_pyden_config()[0].get('appsettings', 'proxy')

    proxies = {
        "http": "http://%s%s/" % (auth, proxy),
        "https": "https://%s%s/" % (auth, proxy)
    } if proxy else {}
    return proxies
