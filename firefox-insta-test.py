import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint

with open("creds.txt", "r") as f:
    USERNAME, PASSWORD = f.read().splitlines()

options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')
firefox_service = FirefoxService(executable_path='./geckodriver')
driver = webdriver.Firefox(service=firefox_service, options=options)

driver.get("http://instagram.com")

time.sleep(5)

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

while True:
    to_skip = False
    with open('tofollow.txt') as f:
        first_line = f.readline().strip('\n')
    if first_line != '':
        print(first_line)
        driver.get(first_line)
        try:
            medias = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//a[starts-with(@href,'/p/')]")))

            posts = [media.get_attribute('href') for media in medias]
            print(posts)
            for post in posts:
                driver.get(post)
                time.sleep(10)
                try:
                    list_of_like_btn = driver.find_elements(
                        By.CSS_SELECTOR, "svg[aria-label='Like']")
                    list_of_like_btn[-1].click()
                except Exception as e:
                    print(e)
                    pass
                time.sleep(15)

            driver.get(first_line)

            try:
                follow_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[text()='Follow']")))
                follow_btn.click()
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            to_skip = True
            pass
    else:
        print('nok')
        continue

    with open(r'tofollow.txt', 'r+') as fp:
        # read an store all lines into list
        lines = fp.readlines()
        # move file pointer to the beginning of a file
        fp.seek(0)
        # truncate the file
        fp.truncate()
        # start writing lines except the first line
        # lines[1:] from line 2 to last line
        fp.writelines(lines[1:])
        
    if to_skip:
        time.sleep(36)
    else:
        time.sleep(3600)
