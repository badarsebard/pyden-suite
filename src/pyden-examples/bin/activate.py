import os
import subprocess
import sys
if sys.version < '3':
    from ConfigParser import ConfigParser
    from StringIO import StringIO
else:
    from configparser import ConfigParser
    from importlib import reload
    from io import StringIO


pyden_config = ConfigParser()
if 'PYDEN_CONFIG' in os.environ:
    proc_out = os.environ["PYDEN_CONFIG"]
else:
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    proc_out, proc_err = proc.communicate()
buf = StringIO(proc_out)
pyden_config.readfp(buf)


class ActivationError(Exception):
    pass


def activate_venv(environment):
    if environment in pyden_config.sections():
        py_exec = os.path.join(os.environ.get("SPLUNK_HOME", ""), pyden_config.get(environment, "executable"))
    else:
        raise ActivationError

    if "pyden" in sys.executable:
        reload(os)
        reload(sys)
        return

    base = os.path.dirname(py_exec)
    path = base + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, {"PATH": path, "PYDEN_CONFIG": proc_out})


def activate_venv_or_die(env=False):
    if not env:
        env = pyden_config.get('default-pys', 'environment')
    try:
        activate_venv(env)
    except ActivationError:
        sys.exit(1)
