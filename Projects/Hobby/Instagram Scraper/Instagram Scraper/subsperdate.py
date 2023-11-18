from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.mouse import Button, Controller
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv

def subsperdate(liste):
    driver = webdriver.Chrome("chromedriver.exe")

    for x in liste:
        site = f"https://www.instagram.com/{x}/tagged"
        driver.get(site)

        if x == liste[0]:

            try:
                akzeptieren = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.aOOlW.bIiDR"))
                )
                akzeptieren.click()
            except:
                driver.quit()

            try:
                username = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                username.send_keys("datascrapexyz01")

                password = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password.send_keys("MineMine123")
                password.send_keys(Keys.RETURN)
            except:
                driver.quit()

            time.sleep(3)

            """
            try:
                later = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF"))
                )
                later.click()
            except:
                driver.quit()
            """

        time.sleep(2)

        try:
            subs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.g47SY"))
            )
            subs_t1 = subs[1].get_attribute("title")
            subs_t1_format = subs_t1.replace(".", "")
        except:
            driver.quit()

        time.sleep(2)
        now = datetime.now()

        print(f"{x} has {int(subs_t1_format)} subs on {now}")


        with open("subs_date.csv", "a", ) as f:
            writer = csv.writer(f)
            writer.writerow([x, int(subs_t1_format), now])

    driver.quit()


liste = ["selenagomez", "kyliejenner", "instagram", "therock", "champagnepapi", "realcoleworld"]

subsperdate(liste)