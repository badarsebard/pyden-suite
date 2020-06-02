import docker
import os
import pytest
import requests
import sys
import time


print("Waiting for Splunk to be ready")
time.sleep(45)
i, waiting = 0, True
while waiting:
    try:
        r = requests.get("http://pyden-splunk:8000")
    except:
        pass
    else:
        if r.ok:
            print("Splunk is ready")
            waiting = False
    finally:
        if i > 120:
            print("Splunk did not come up within 2 minutes")
            sys.exit(1)
        i += 1
        time.sleep(1)

print("Beginning automated tests")
code = pytest.main([os.path.join(os.environ['CI_PROJECT_DIR'], "test")])
sys.exit(code)
