from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pynput
from pynput.mouse import Button, Controller
import time
from datetime import datetime

mouse = Controller()

class InstaBot:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import pynput
    from pynput.mouse import Button, Controller
    import time
    from datetime import datetime

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def login(self, site):
        import time

        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(site)
        driver.maximize_window()

        time.sleep(1)

        mouse = Controller()
        mouse.position = (1000, 650)
        mouse.click(Button.left, 1)

        time.sleep(1)

        username = driver.find_element_by_name("username")
        username.send_keys(self.username)

        password = driver.find_element_by_name("password")
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

        time.sleep(3)

        later = driver.find_element_by_css_selector("button.sqdOP.yWX7d.y3zKF")
        later.click()


    def tagged(self, profile):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        import pynput
        from pynput.mouse import Button, Controller
        import time


        driver = webdriver.Chrome("chromedriver.exe")
        site = f"https://www.instagram.com/{profile}/tagged/"
        InstaBot.login(self, site)
        x = 0
        while x < 6:
            mouse.scroll(0, -100)
            time.sleep(1)
            x += 1

        pictures = driver.find_elements_by_css_selector("div.Nnq7C.weEfm")

        print(len(pictures))

        picture = pictures[10].find_element_by_css_selector("div.v1Nh3.kIKUG._bz0w")
        prelink = picture.find_element_by_tag_name("a")
        link = prelink.get_attribute("href")
        time.sleep(1)
        driver.get(link)
        time.sleep(2)
        time = driver.find_element_by_tag_name("time")
        datetime = time.get_attribute("datetime")
        InstaBot.timecal(datetime)

    def timecal(self, datetime):


        post_date = datetime
        now = str(datetime.now())

        year = int(now[0:4]) - int(post_date[0:4]+1)
        month = int(now[5:7]) - int(post_date[5:7])
        day = int(now[8:10]) - int(post_date[8:10])

        hours = int(now[11:13]) - int(post_date[11:13])
        minutes = int(now[14:16]) - int(post_date[14:16])
        seconds = int(now[17:19]) - int(post_date[17:19])

        print(f"years:{year}, moths:{month}, days:{day}")
        print(f"hours:{hours}, minutes:{minutes}, seconds:{seconds}")

