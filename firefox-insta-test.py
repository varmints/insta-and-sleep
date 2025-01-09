import time
import random
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import pprint
from simple_term_menu import TerminalMenu

username_without_special_characters = ""
driver = webdriver


def current_time():
    now = datetime.now()
    return print(now)


def probably(chance=0.5):
    return random.random() < chance


def remove_special_characters(username):
    global username_without_special_characters
    username_without_special_characters = re.sub(r"\W+", "", username)


def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print("{:02d}:{:02d}:{:02d}".format(hours, mins, secs), end="\r")
        time.sleep(1)
        seconds -= 1


def convert_to_number(text):
    if "M" in text and "." in text:
        text = text.replace(".", "").replace("M", "00000")
    elif "M" in text and "." not in text:
        text = text.replace("M", "000000")
    elif "K" in text and "." in text:
        text = text.replace(".", "").replace("K", "00")
    elif "K" in text and "." not in text:
        text = text.replace("K", "000")
    elif "," in text:
        text = text.replace(",", "")
    else:
        text
    return int(text)


def check_necessary_files_exist():
    try:
        with open("todelete.txt." + username_without_special_characters, "x") as f:
            print(
                "File todelete.txt."
                + username_without_special_characters
                + " has been created."
            )
    except FileExistsError:
        pass

    try:
        with open("tofollow.txt." + username_without_special_characters, "x") as f:
            print(
                "File tofollow.txt."
                + username_without_special_characters
                + " has been created."
            )
    except FileExistsError:
        pass


def check_is_login():
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "svg[aria-label='Notifications']")
            )
        )
    except Exception:
        current_time()
        print("Can't find 'Notifications' button")
        countdown(3600)
        login(driver)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Dismiss']"))
            ).click()
        except Exception as e:
            print(e)
            print("Can't find 'Dismiss' button")


def unfollow_useless_following(times):
    for _ in range(times):
        with open("todelete.txt." + username_without_special_characters, "r") as f:
            first_line = f.readline().strip("\n")
        if first_line != "":
            driver.get("http://instagram.com/" + first_line)
            time.sleep(random.randint(10, 15))

            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "svg[aria-label='Notifications']")
                    )
                )
            except Exception as e:
                print("unfollow_useless_following: Possible that you're not logged in")
                print(e)

            try:
                following_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Following']"))
                )
                time.sleep(random.randint(5, 15))
                following_btn.click()
                time.sleep(random.randint(5, 20))
                try:
                    unfollow_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Unfollow']")
                        )
                    )
                    time.sleep(random.randint(5, 15))
                    unfollow_btn.click()
                    time.sleep(random.randint(5, 20))
                except Exception as e:
                    print("unfollow_useless_following: Cant see Unfollow button")
                    print(e)
            except Exception as e:
                print("Can't see Following button")
                print(e)
                pass

            with open(
                r"todelete.txt." + username_without_special_characters, "r+"
            ) as fp:
                # read an store all lines into list
                lines = fp.readlines()
                # move file pointer to the beginning of a file
                fp.seek(0)
                # truncate the file
                fp.truncate()
                # start writing lines except the first line
                # lines[1:] from line 2 to last line
                fp.writelines(lines[1:])

            print("Unfollowed user: " + first_line)


def saveCookies():
    # Get and store cookies after login
    cookies = driver.get_cookies()

    # Store cookies in a file
    with open("cookies.json." + username_without_special_characters, "w") as file:
        json.dump(cookies, file)
    print("New Cookies saved successfully")


def load_cookies():
    cookies_filename = "cookies.json." + username_without_special_characters

    # Check if cookies file exists
    if cookies_filename in os.listdir():
        # Load cookies to a vaiable from a file
        with open(cookies_filename, "r") as file:
            cookies = json.load(file)

        # Set stored cookies to maintain the session
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        with open(cookies_filename, "w") as file:
            json.dump({}, file)
            pass

    driver.refresh()  # Refresh Browser after login


def accounts_from_suggested_for_you():
    print("accounts_from_suggested_for_you")

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Instagram']"))
        ).click()
    except Exception as e:
        print(e)
        driver.get("http://instagram.com")
        pass

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='See All']"))
        ).click()
    except Exception as e:
        print(e)
        print("Can't see See more button")
        pass

    time.sleep(5)

    elements = driver.find_elements(By.XPATH, "//main//a[@href]")
    new_account_to_follow = [element.get_attribute("href") for element in elements]
    new_account_to_follow_without_duplicates = list(
        dict.fromkeys(new_account_to_follow)
    )

    with open("tofollow.txt." + username_without_special_characters, "w") as f:
        for account in new_account_to_follow_without_duplicates:
            f.write(str(account) + "\n")


def see_stories_from_homepage():
    print("see_stories_from_homepage")

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Instagram']"))
        ).click()
    except Exception as e:
        print(e)
        print("Can't see Instagram logo")
        driver.get("http://instagram.com")
        pass

    time.sleep(5)

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//ul/li/div/div"))
        ).click()
    except Exception as e:
        print(e)
        print("Can't see stories canvas")
        pass

    time.sleep(random.randint(20,90))

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Close']"))
        ).click()
    except Exception as e:
        print(e)
        print("Can't see close button")
        pass

    time.sleep(5)


def login(login_credentials, is_remove_current_cookies=False):
    username = login_credentials["username"]

    if is_remove_current_cookies:
        if os.path.exists("cookies.json." + username_without_special_characters):
            os.remove("cookies.json." + username_without_special_characters)
        else:
            print("The file does not exist")

    driver.get("http://instagram.com")

    time.sleep(10)

    load_cookies()

    time.sleep(10)
    try:
        driver.find_element(By.XPATH, "//a[text()='" + username + "']")
        print("Previous session loaded")
    except Exception:
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Allow all cookies']")
                )
            ).click()
        except Exception:
            pass

        time.sleep(10)

        driver.find_element(
            By.XPATH, "//input[@aria-label='Phone number, username, or email']"
        ).send_keys(login_credentials["username"])

        time.sleep(3)

        driver.find_element(By.XPATH, "//input[@aria-label='Password']").send_keys(
            login_credentials["password"]
        )

        time.sleep(2)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(10)

        driver.find_element(By.XPATH, "//button[text()='Save info']").click()

        time.sleep(10)

        saveCookies()


def endless_growth(login_credentials):
    options = Options()
    options.set_preference("intl.accept_languages", "en-US, en")
    # options.add_argument("-private-window")
    firefox_service = FirefoxService(
        executable_path="./geckodriver",
        log_output="./geckodriver.log." + username_without_special_characters,
    )
    global driver
    driver = webdriver.Firefox(service=firefox_service, options=options)
    time.sleep(random.randint(15, 20))
    login(login_credentials)

    processed_accounts = 0

    while True:
        to_skip = False
        login_error_count = 0

        with open("tofollow.txt." + username_without_special_characters, "r") as f:
            potential_follower_profile = f.readline().strip("\n")
        if potential_follower_profile != "":
            print(potential_follower_profile)
            driver.get(potential_follower_profile)
            time.sleep(random.randint(5, 10))

            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "svg[aria-label='Notifications']")
                    )
                )
            except Exception:
                login_error_count += 1
                current_time()
                print("Can't find 'Notifications' button")
                countdown(3600)
                if login_error_count >= 3:
                    login(login_credentials, True)
                else:
                    login(login_credentials)
                try:
                    dismiss_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Dismiss']")
                        )
                    )
                    dismiss_btn.click()
                except Exception:
                    print("Can't find 'Dismiss' button")
                continue

            try:
                follow_back_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[text()='Follow Back']")
                    )
                )
                follow_back_btn.click()
            except Exception:
                to_skip = False
                pass

            try:
                follow_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow']"))
                )
            except Exception:
                to_skip = True
                pass

            try:
                followers = driver.find_element(
                    By.XPATH, "//a[text()[contains(.,'followers')]]/span/span"
                ).text
                following = driver.find_element(
                    By.XPATH, "//a[text()[contains(.,'following')]]/span/span"
                ).text
                followers = convert_to_number(followers)
                following = convert_to_number(following)
                if followers - following >= 5000 or following <= 50:
                    to_skip = True
            except Exception as e:
                print("Error 1")
                print(e)
                pass

            try:
                profile_username = (
                    WebDriverWait(driver, 10)
                    .until(EC.presence_of_element_located((By.XPATH, "//h2/span")))
                    .text
                )
                medias = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//a[starts-with(@href,'/" + profile_username + "/p/')]",
                        )
                    )
                )
                # add reels in future
            except Exception as e:
                print("Can't fetch media")
                print(e)
                to_skip = True
                pass

            if not to_skip:
                # posts = [media.get_attribute('href') for media in medias]
                current_time()
                # print(posts)
                for post in medias:
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", post
                    )
                    time.sleep(random.randint(4, 8))
                    parent = post.find_element(By.XPATH, "..")
                    ActionChains(driver).click(parent).perform()
                    time.sleep(random.randint(4, 8))
                    try:
                        list_of_like_btn = driver.find_elements(
                            By.CSS_SELECTOR, "svg[aria-label='Like']"
                        )
                        list_of_like_btn[0].click()
                    except Exception as e:
                        print("Error 3")
                        print(e)
                        pass
                    time.sleep(random.randint(4, 8))
                    try:
                        close_btn = driver.find_element(
                            By.CSS_SELECTOR, "svg[aria-label='Close']"
                        )
                        close_btn.click()
                    except Exception as e:
                        print("Error 4")
                        print(e)
                        pass
                    time.sleep(random.randint(4, 8))

                driver.execute_script(
                    "window.scrollBy({top: 0, left: 0, behavior: 'smooth' })"
                )
                time.sleep(random.randint(4, 8))
                try:
                    follow_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow']"))
                    )
                    follow_btn.click()
                except Exception:
                    print("Can't find 'Follow' button")
                    try:
                        follow_back_btn = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//div[text()='Follow Back']")
                            )
                        )
                        follow_back_btn.click()
                    except Exception:
                        print("Can't find 'Follow Back' button")
                        pass
                    pass
                login_error_count = 0
        else:
            accounts_from_suggested_for_you()
            countdown(3600)
            continue

        with open(r"tofollow.txt." + username_without_special_characters, "r+") as fp:
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
            time.sleep(random.randint(20, 60))
        else:
            time.sleep(random.randint(600, 900))

        if probably(0.3):
            unfollow_useless_following(random.randint(1, 5))
        else:
            pass

        if probably(0.3):
            see_stories_from_homepage()
        else:
            pass

        if processed_accounts % 100 == 0:
            print("Time to break...")
            countdown(10800)


def main():
    with open("creds.json", mode="r", encoding="utf-8") as f:
        users = json.load(f)

    main_menu_items = []

    for user in users:
        main_menu_items.append(user["username"])

    main_menu_title = "Select user:\n  Press Q or Esc to quit. \n"
    main_menu_cursor = "# "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    while not main_menu_exit:
        main_sel_user = main_menu.show()

        remove_special_characters(users[main_sel_user]["username"])

        check_necessary_files_exist()

        endless_growth(users[main_sel_user])


if __name__ == "__main__":
    main()
