from selenium import webdriver
from selenium.webdriver.firefox.service import Service

driver = webdriver.Firefox(service=Service("/usr/bin/geckodriver"))
driver.get("https://www.google.com")
input("Press Enter to close...")
driver.quit()
