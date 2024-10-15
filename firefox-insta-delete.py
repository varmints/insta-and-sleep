import time
import random
import json
import os
import dateutil.parser
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
from pprint import pprint


def current_time():
    now = datetime.now()
    return print(now)


def saveCookies(driver):
    # Get and store cookies after login
    cookies = driver.get_cookies()

    # Store cookies in a file
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    print('New Cookies saved successfully')


def loadCookies():
    # Check if cookies file exists
    if 'cookies.json' in os.listdir():

        # Load cookies to a vaiable from a file
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)

        # Set stored cookies to maintain the session
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        print('No cookies file found')

    driver.refresh()  # Refresh Browser after login


with open("creds.txt", "r") as f:
    USERNAME, PASSWORD = f.read().splitlines()

options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')
firefox_service = FirefoxService(
    executable_path='./geckodriver', log_output='./geckodriver.log')
driver = webdriver.Firefox(service=firefox_service, options=options)

driver.get("http://instagram.com")

time.sleep(10)

loadCookies()

time.sleep(10)

try:
    driver.find_element(By.XPATH, "//a[text()='"+USERNAME+"']")
    print('Previous session loaded')
except:
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Allow all cookies']"))).click()
    except:
        pass

    time.sleep(10)

    driver.find_element(
        By.XPATH, "//input[@aria-label='Phone number, username, or email']").send_keys(USERNAME)

    time.sleep(3)

    driver.find_element(
        By.XPATH, "//input[@aria-label='Password']").send_keys(PASSWORD)

    time.sleep(2)

    driver.find_element(
        By.XPATH, "//button[@type='submit']").click()

    time.sleep(15)
    saveCookies(driver)

unfollowed_accounts = 0

while True:
    to_skip = False
    with open('todelete.txt') as f:
        first_line = f.readline().strip('\n')
    if first_line != '':
        print(first_line)
        driver.get("http://instagram.com/" + first_line)

        try:
            follow_back_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Following']")))
            follow_back_btn.click()
        except Exception as e:
            print(e)
            break

        with open(r'todelete.txt', 'r+') as fp:
            # read an store all lines into list
            lines = fp.readlines()
            # move file pointer to the beginning of a file
            fp.seek(0)
            # truncate the file
            fp.truncate()
            # start writing lines except the first line
            # lines[1:] from line 2 to last line
            fp.writelines(lines[1:])
        unfollowed_accounts += 1
        print(f'Unfollowed accounts: {unfollowed_accounts}')
