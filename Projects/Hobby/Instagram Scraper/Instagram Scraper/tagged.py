from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pynput
from pynput.mouse import Button, Controller
import time
from datetime import datetime


name = "selenagomez"

site = f"https://www.instagram.com/{name}/tagged"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(site)
driver.maximize_window()

time.sleep(1)

mouse = Controller()
mouse.position = (1000, 650)
mouse.click(Button.left, 1)

time.sleep(1)

username = driver.find_element_by_name("username")
username.send_keys("datascrapexyz01")

password = driver.find_element_by_name("password")
password.send_keys("MineMine123")
password.send_keys(Keys.RETURN)


time.sleep(3)


later = driver.find_element_by_css_selector("button.sqdOP.yWX7d.y3zKF")
later.click()

time.sleep(3)

x = 0
while x < 7:
    mouse.scroll(0, -100)
    time.sleep(1)
    x += 1

pictures = driver.find_elements_by_css_selector("div.Nnq7C.weEfm")

print(len(pictures))

picture = pictures[13].find_element_by_css_selector("div.v1Nh3.kIKUG._bz0w")
prelink = picture.find_element_by_tag_name("a")
link = prelink.get_attribute("href")
time.sleep(1)
driver.get(link)
time.sleep(2)
time = driver.find_element_by_tag_name("time")
datetime_post = time.get_attribute("datetime")
print(datetime_post)

post_date = datetime_post

now = str(datetime.now())

year = int(now[0:4]) - int(post_date[0:4])
month = int(now[5:7]) - int(post_date[5:7])
day = int(now[8:10]) - int(post_date[8:10])

hours = int(now[11:13]) - (int(post_date[11:13])+1)
minutes = int(now[14:16]) - int(post_date[14:16])
seconds = int(now[17:19]) - int(post_date[17:19])

if month < 0:
    year -= 1
    month_new = 12 + month
    month = month_new

if day < 0:
    month -= 1
    day_new = 30 + day
    day = day_new

if hours < 0:
    day -= 1
    hours_new = 24 + hours
    hours = hours_new

if minutes < 0:
    hours -= 1
    minutes_new = 60 + minutes
    minutes = minutes_new

if seconds < 0:
    minutes -= 1
    seconds_new = 60 + seconds
    seconds = seconds_new

print(f"years:{year}, moths:{month}, days:{day}")
print(f"hours:{hours}, minutes:{minutes}, seconds:{seconds}")

driver.quit()
