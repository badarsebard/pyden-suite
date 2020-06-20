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


class ActivationError(Exception):
    pass


def activate_venv():
    if "pyden" in sys.executable:
        reload(os)
        reload(sys)
        return

    config = ConfigParser()
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    proc_out, proc_err = proc.communicate()
    buf = StringIO(proc_out)
    config.readfp(buf)
    script = sys.argv[0].split(os.path.sep)[-1]
    if script in config.sections():
        environment = config.get(script, 'environment')
    else:
        sys.exit(1)
    if environment in config.sections():
        py_exec = os.path.join(os.environ.get("SPLUNK_HOME", ""), config.get(environment, "executable"))
    else:
        raise ActivationError

    base = os.path.dirname(py_exec)
    path = base + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, {"PATH": path, "PYDEN_CONFIG": proc_out})


try:
    activate_venv()
except ActivationError:
    sys.exit(1)
