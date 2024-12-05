#!/usr/bin/env python3

import random
import time
import json
import os
import re
from pprint import pprint
from colorama import Fore, Style
from simple_term_menu import TerminalMenu
from datetime import datetime
import logging
import numpy as np
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from datetime import datetime, timedelta

# json.sessions(json.load(resp), indent=2)
logger = logging.getLogger()


def probably(chance=.5):
    # By default returns True 50% of the time.
    return random.random() < chance


def remove_special_characters(string):
    return re.sub('\W+', '', string)


def countdown(t):
    # define the countdown func.
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


def current_time():
    now = datetime.now()
    return print(now)


def createDevice(login_credentials):
    username = remove_special_characters(login_credentials["username"])
    print(f"You will be logged in!")
    cl = Client()
    cl.set_locale('pl_PL')
    cl.set_country_code(48)  # +48
    # Los Angeles UTC (GMT) -7 hours == -25200 seconds
    cl.set_timezone_offset(2 * 60 * 60)
    cl.login(login_credentials["username"], login_credentials["password"])
    cl.dump_settings("session.json."+username)


def login_user(cl, login_credentials):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    username = remove_special_characters(login_credentials["username"])
    cl.delay_range = [5, 15]
    session = cl.load_settings("session.json."+username)

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(login_credentials["username"],
                     login_credentials["password"])

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info(
                    "Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(login_credentials["username"],
                         login_credentials["password"])
            login_via_session = True
        except Exception as e:
            logger.info(
                "Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % login_credentials["username"])
            if cl.login(login_credentials["username"],
                        login_credentials["password"]):
                login_via_pw = True
        except Exception as e:
            logger.info(
                "Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


def get_more_potential_followers(login_credentials, type):
    login_username = remove_special_characters(login_credentials["username"])
    if type == "BY USERNAME":
        print("Type username:")
        user_to_check_input = input()
    cl = Client()
    login_user(cl, login_credentials)

    users_to_follow = []
    processed_accounts = 0
    omitted_accounts = 0
    followed_accounts = 0
    accounts_to_follow = 0

    if type == "BY USERNAME":
        user_to_check = cl.user_info_by_username(user_to_check_input)
        try:
            followings = cl.user_following(user_to_check.pk, 600)
            users = []
            for i, user in enumerate(followings):
                users.append(user)
            np.random.shuffle(users)
            print("Number of users")
            print(len(users))
        except:
            print("Exception when user following.")
            time.sleep(10800)
    else:
        medias = cl.user_medias(cl.user_id, 3)
        users = cl.media_likers(medias[random.randint(0, 2)].id)
        np.random.shuffle(users)

    if type == "BY USERNAME":
        print("users")
        print(users)
        for user in users:
            current_time()
            print(
                f"Processed accounts: {processed_accounts}; Omitted accounts: {omitted_accounts}; Followed accounts: {followed_accounts}; Accounts to follow: {accounts_to_follow}")
            try:
                user_fol = cl.user_info(user)
                print(user_fol)
            except:
                print("Error when fetch user info.")
            try:
                medias = cl.user_medias(user_fol.pk, 6)
            except:
                current_time()
                print("Error when fetch posts. Private account?")
                omitted_accounts += 1
                time.sleep(600)
                login_user(cl, login_credentials)
                continue
            try:
                medias = cl.user_medias(user_fol.pk, 6)
                print(medias)
            except:
                current_time()
                print("Error when fetch posts. Private account?")
                omitted_accounts += 1
                time.sleep(600)
                login_user(cl, login_credentials)
                continue
            rate_counter = 0
            permission_to_save = False
            for media in medias:
                post_created_at = media.taken_at
                n_days_ago = datetime.now() - timedelta(days=14)
                if (n_days_ago.timestamp() < post_created_at.timestamp()) and (rate_counter <= 5):
                    rate_counter += 1
            if rate_counter >= 4:
                permission_to_save = True
            if permission_to_save:
                # Do something X% of the time
                if probably(0.99):
                    users_to_follow.append(
                        'https://www.instagram.com/' + user_fol.username)
                    time.sleep(random.randint(180, 420))
                else:
                    # Do something else 100-X% of the time
                    users_to_follow.append(
                        'https://www.instagram.com/' + user_fol.username)
                accounts_to_follow += 1
                with open('tofollow.txt.'+login_username, 'r') as tofollow:
                    link_to_save = 'https://www.instagram.com/' + user_fol.username + '/\n'
                    if link_to_save in tofollow.read():
                        current_time()
                        print(f"{link_to_save} is already saved")
                    else:
                        with open('tofollow.txt.'+login_username, 'a') as tofollow:
                            tofollow.write(link_to_save)
                time.sleep(random.randint(30, 60))
            else:
                omitted_accounts += 1
            processed_accounts += 1
            if processed_accounts % 800 == 0:
                print("Time to break...")
                time.sleep(18000)
            else:
                time.sleep(random.randint(20, 60))
    else:
        for user in users:
            print(f"Media liker username: {user.username}")
            if user.username != cl.username:
                try:
                    following = cl.user_following(user.pk, 10)
                except:
                    print("Exception when user following.")
                    time.sleep(10800)
                    login_user(cl, login_credentials)
                    continue
                following_list_from_dict = [i for i in following.values()]
                following_list_from_dict[:1]
                np.random.shuffle(following_list_from_dict)
                following_list_from_dict[:350]
                for user_fol in following_list_from_dict:
                    current_time()
                    print(
                        f"Processed accounts: {processed_accounts}; Omitted accounts: {omitted_accounts}; Followed accounts: {followed_accounts}; Accounts to follow: {accounts_to_follow}")
                    try:
                        medias = cl.user_medias(user_fol.pk, 6)
                    except:
                        current_time()
                        print("Error when fetch posts. Private account?")
                        omitted_accounts += 1
                        time.sleep(600)
                        login_user(cl, login_credentials)
                        continue
                    rate_counter = 0
                    permission_to_save = False
                    for media in medias:
                        post_created_at = media.taken_at
                        n_days_ago = datetime.now() - timedelta(days=14)
                        if (n_days_ago.timestamp() < post_created_at.timestamp()) and (rate_counter <= 5):
                            rate_counter += 1
                    if rate_counter >= 4:
                        permission_to_save = True
                    if permission_to_save:
                        # Do something X% of the time
                        if probably(0.99):
                            users_to_follow.append(
                                'https://www.instagram.com/' + user_fol.username)
                            time.sleep(random.randint(180, 420))
                        else:
                            # Do something else 100-X% of the time
                            users_to_follow.append(
                                'https://www.instagram.com/' + user_fol.username)
                        accounts_to_follow += 1
                        with open('tofollow.txt.'+login_username, 'r') as tofollow:
                            link_to_save = 'https://www.instagram.com/' + user_fol.username + '/\n'
                            if link_to_save in tofollow.read():
                                current_time()
                                print(f"{link_to_save} is already saved")
                            else:
                                with open('tofollow.txt.'+login_username, 'a') as tofollow:
                                    tofollow.write(link_to_save)
                        time.sleep(random.randint(30, 60))
                    else:
                        omitted_accounts += 1
                    processed_accounts += 1
                    if processed_accounts % 700 == 0:
                        print("Time to break...")
                        time.sleep(3600)
                    else:
                        time.sleep(random.randint(20, 60))
            time.sleep(random.randint(20, 60))


def main():
    with open("creds.json", mode="r", encoding="utf-8") as f:
        users = json.load(f)

    main_menu_users = []
    for user in users:
        main_menu_users.append(user["username"])

    main_menu_title = "  Insta & Sleep.\n  Press Q or Esc to quit. \n"
    main_menu_items = ["Create device",
                       "Get more potential followers", "Quit"]
    main_menu_cursor = "# "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu_choose_user = TerminalMenu(
        menu_entries=main_menu_users,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    get_more_potential_follower_menu_title = "Choose type of strategy.\n  Press Q or Esc to back to main menu. \n"
    get_more_potential_follower_menu_items = [
        "BY USERNAME", "BY LATEST POSTS", "Back to Main Menu"]
    get_more_potential_follower_menu_back = False
    get_more_potential_follower_menu = TerminalMenu(
        get_more_potential_follower_menu_items,
        title=get_more_potential_follower_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    while not main_menu_exit:
        main_sel_user = main_menu_choose_user.show()

        main_sel = main_menu.show()

        if main_sel == 0:
            createDevice(users[main_sel_user])
        elif main_sel == 1:
            while not get_more_potential_follower_menu_back:
                get_more_potential_follower_sel = get_more_potential_follower_menu.show()
                if get_more_potential_follower_sel == 0:
                    get_more_potential_followers(users[main_sel_user],
                                                 get_more_potential_follower_menu_items[get_more_potential_follower_sel])
                elif get_more_potential_follower_sel == 1:
                    get_more_potential_followers(users[main_sel_user],
                                                 get_more_potential_follower_menu_items[get_more_potential_follower_sel])
                elif get_more_potential_follower_sel == 2 or get_more_potential_follower_sel == None:
                    get_more_potential_follower_menu_back = True
                    print("Back selected")
            get_more_potential_follower_menu_back = False
        elif main_sel == 2 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
