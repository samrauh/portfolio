from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.mouse import Button, Controller
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime


def subspersecond(liste):
    driver = webdriver.Chrome("chromedriver.exe")

    for x in liste:
        site = f"https://www.instagram.com/{x}/tagged"
        driver.get(site)

        if x == liste[0]:
            with open("data.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["profile", "subs per set", "subs total", "subs per sub"])

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

            try:
                later = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF"))
                )
                later.click()
            except:
                driver.quit()

            time.sleep(2)

        try:
            subs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.g47SY"))
            )
            subs_t1 = subs[1].get_attribute("title")
            subs_t1_format = subs_t1.replace(".", "")
        except:
            driver.quit()


        time.sleep(5)

        driver.refresh()

        time.sleep(1)


        try:
            subs2 = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.g47SY"))
            )
            subs_t2 = subs2[1].get_attribute("title")
            subs_t2_format = subs_t2.replace(".", "")
        except:
            driver.quit()

        gain = int(subs_t2_format) - int(subs_t1_format)


        print(f"{x} made {gain} new subs in 10 seconds")

        subs_per_sub = (gain/int(subs_t1_format))*10000000

        with open("data.csv", "a",) as f:
            writer = csv.writer(f)
            writer.writerow([x, gain, int(subs_t1_format), subs_per_sub])



    driver.quit()



liste = ["selenagomez", "kyliejenner", "instagram", "therock", "champagnepapi", "realcoleworld"]

subspersecond(liste)
