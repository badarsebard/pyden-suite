import docker
from selenium import webdriver
import time

print("Connect to docker service")
client = docker.APIClient(base_url="unix://var/run/docker.sock")
i = 0
health = ""
while health != "healthy" and i < 120:  # max two minute wait time
    health = client.inspect_container("pyden-splunk-1")['State']['Health']['Status']
    time.sleep(1)
    i += 1
print("Beginning automated tests...")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://pyden-splunk:8000")
print(driver.title)
