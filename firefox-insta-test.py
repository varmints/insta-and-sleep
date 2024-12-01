import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from pprint import pprint


def current_time():
    now = datetime.now()
    return print(now)


def probably(chance=.5):
    return random.random() < chance

# define the countdown func.


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


def convert_to_number(text):
    if 'M' in text and '.' in text:
        text = text.replace('.', '').replace('M', '00000')
    elif 'M' in text and '.' not in text:
        text = text.replace('M', '000000')
    elif 'K' in text and '.' in text:
        text = text.replace('.', '').replace('K', '00')
    elif 'K' in text and '.' not in text:
        text = text.replace('K', '000')
    elif ',' in text:
        text = text.replace(',', '')
    else:
        text
    return int(text)


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


def login(driver):
    with open("creds.txt", "r") as f:
        USERNAME, PASSWORD = f.read().splitlines()
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

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(15)

        saveCookies(driver)


options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')
firefox_service = FirefoxService(
    executable_path='./geckodriver', log_output='./geckodriver.log')
driver = webdriver.Firefox(service=firefox_service, options=options)

login(driver)

processed_accounts = 0

while True:
    to_skip = False
    with open('tofollow.txt') as f:
        first_line = f.readline().strip('\n')
    if first_line != '':
        print(first_line)
        driver.get(first_line)
        time.sleep(random.randint(5, 10))

        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "svg[aria-label='Notifications']")))
        except Exception as e:
            current_time()
            print(e)
            countdown(3600)
            login(driver)
            try:
                dismiss_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Dismiss']")))
                dismiss_btn.click()
            except:
                print("Can't find dismiss button.")
            continue

        try:
            follow_back_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow Back']")))
            follow_back_btn.click()
        except Exception as e:
            to_skip = False
            pass

        try:
            followers = driver.find_element(
                By.XPATH, "//a[text()[contains(.,'followers')]]/span/span").text
            following = driver.find_element(
                By.XPATH, "//a[text()[contains(.,'following')]]/span/span").text
            followers = convert_to_number(followers)
            following = convert_to_number(following)
            print(followers, following)
            if followers - following >= 5000 or following <= 50:
                to_skip = True
        except Exception as e:
            print("Error 1")
            print(e)
            pass

        try:
            follow_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow']")))
        except Exception as e:
            print("Can't find 'Follow' button.")
            print(e)
            to_skip = True
            pass

        try:
            username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2/span"))).text
            medias = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//a[starts-with(@href,'/"+username+"/p/')]")))
            # add reels in future
        except Exception as e:
            print("Can't fetch media.")
            print(e)
            to_skip = True
            pass

        # if not to_skip:
        #     new_post_counter = 0
        #     for post in medias:
        #         driver.execute_script(
        #             "arguments[0].scrollIntoView({block:'center'});", post)
        #         time.sleep(random.randint(5, 10))
        #         parent = post.find_element(By.XPATH, "..")
        #         ActionChains(driver).click(parent).perform()
        #         time.sleep(random.randint(5, 10))
        #         try:
        #             post_created_at = driver.find_element(
        #                 By.XPATH, "(//time)[last()]").get_attribute("datetime")
        #             n_days_ago = datetime.now() - timedelta(days=60)
        #             if (n_days_ago.timestamp() < dateutil.parser.parse(post_created_at).timestamp()):
        #                 new_post_counter += 1

        #         except Exception as e:
        #             print(e)
        #             pass

        #         try:
        #             close_btn = driver.find_element(
        #                 By.CSS_SELECTOR, "svg[aria-label='Close']")
        #             close_btn.click()
        #         except Exception as e:
        #             print(e)
        #             pass
        #     if new_post_counter < 10:
        #         to_skip = True

        if not to_skip:
            # posts = [media.get_attribute('href') for media in medias]
            current_time()
            # print(posts)
            for post in medias:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", post)
                time.sleep(random.randint(4, 8))
                parent = post.find_element(By.XPATH, "..")
                ActionChains(driver).click(parent).perform()
                time.sleep(random.randint(4, 8))
                try:
                    list_of_like_btn = driver.find_elements(
                        By.CSS_SELECTOR, "svg[aria-label='Like']")
                    list_of_like_btn[0].click()
                except Exception as e:
                    print("Error 3")
                    print(e)
                    pass
                time.sleep(random.randint(4, 8))
                try:
                    close_btn = driver.find_element(
                        By.CSS_SELECTOR, "svg[aria-label='Close']")
                    close_btn.click()
                except Exception as e:
                    print("Error 4")
                    print(e)
                    pass
                time.sleep(random.randint(4, 8))
            driver.get(first_line)
            time.sleep(random.randint(4, 8))
            try:
                follow_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow']")))
                follow_btn.click()
            except:
                print("Error 5")
                pass
            try:
                follow_back_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow Back']")))
                follow_back_btn.click()
            except:
                pass
    else:
        print('nok')
        time.sleep(3600)
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
    processed_accounts += 1
    if to_skip:
        if probably(0.95):
            time.sleep(random.randint(20, 60))
        else:
            time.sleep(random.randint(360, 720))
    else:
        time.sleep(random.randint(300, 600))

    if processed_accounts % 200 == 0:
        print("Time to break...")
        time.sleep(14400)
