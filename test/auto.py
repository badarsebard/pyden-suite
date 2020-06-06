import docker
import os
import pytest
import sys
import time


ci = os.environ.get("CI")
if not ci:
    print("Waiting for Splunk to be ready", end="")
    i, waiting = 0, True
    client = docker.APIClient()
    while waiting:
        status = client.inspect_container("pyden-splunk-1")['State']['Health']['Status']
        if "healthy" in status:
            print("\nSplunk is ready")
            waiting = False
            continue
        else:
            print(".", end="")
        if i > 120:
            print("\nSplunk did not come up within 2 minutes")
            sys.exit(1)
        i += 1
        time.sleep(1)

print("Beginning automated tests")
code = pytest.main([os.path.join(os.environ['CI_PROJECT_DIR'], "test"), "--verbose"])
sys.exit(code)
