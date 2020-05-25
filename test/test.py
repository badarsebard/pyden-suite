from selenium import webdriver


print("Beginning automated tests...")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://pyden-splunk:8000")
print(driver.title)
