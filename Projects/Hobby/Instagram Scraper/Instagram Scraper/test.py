from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.mouse import Button, Controller
import time
from datetime import datetime


name = "selenagomez"

site = f"https://www.instagram.com/{name}/tagged"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(site)

time.sleep(1)

akzeptieren = driver.find_element_by_css_selector("button.aOOlW.bIiDR")
akzeptieren.click()