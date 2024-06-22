import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint

options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')

driver = webdriver.Firefox(options=options)

driver.get("http://instagram.com")

time.sleep(5)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "//button[text()='Allow all cookies']"))).click()

time.sleep(10)

driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys("hdnodv")

time.sleep(3)

driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys("E86Ms#")

time.sleep(2)

driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button").click()

time.sleep(5)

try:
    driver.find_element(
        By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div[3]/div").click()
except NoSuchElementException:
    print("exception handled")

time.sleep(5)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div"))).click()

time.sleep(3)

# Wyłącz powiadomienia
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"))).click()

time.sleep(3)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div"))).click()

time.sleep(5)

try:
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[2]/div/div[1]/div[1]").click()
except NoSuchElementException:
    print("no posts")

time.sleep(5)

driver.get(driver.current_url + "liked_by/")

time.sleep(15)

liked_by_url = driver.current_url

try:
    likers = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div//div")
    # Get all the elements available with tag name 'p'
    pprint(likers)

    for l in likers:
        print(l.text)
except NoSuchElementException:
    print("no likers")
