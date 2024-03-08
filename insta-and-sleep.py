#!/usr/bin/env python3

import random
import time
import json
import os
import re
from colorama import Fore, Style
from simple_term_menu import TerminalMenu
from datetime import datetime
import logging
import numpy as np
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

# json.sessions(json.load(resp), indent=2)
logger = logging.getLogger()


def createDevice():
    print(f"You will be logged in!")
    cl = Client()
    cl.set_locale('pl_PL')
    cl.set_country_code(48)  # +48
    # Los Angeles UTC (GMT) -7 hours == -25200 seconds
    cl.set_timezone_offset(2 * 60 * 60)
    print(cl.get_settings())
    cl.session_settings("session.json")


def login_user(cl):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    with open("creds.txt", "r") as f:
        USERNAME, PASSWORD = f.read().splitlines()
    cl.delay_range = [5, 10]
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

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

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info(
                "Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info(
                "Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


def like_by_hashtag():
    cl = Client()

    login_user(cl)

    hashtags = ["spicollective", "photography", "photographyday", "timeless_streets", "today_street",  "streetphotography",
                "spi_geometry", "lensculture", "fujifilm", "architecture_minimal", "minimal_streetphoto", "architecturelover"]

    while True:

        print(f"user_info({cl.user_id})!")
        print(cl.user_info(cl.user_id))

        comments = ["Awesome", "Wonderful 💯", "This is such a moood !!!",
                    "👍📷❤️", "Wow that looks so amazing 😍😍😍", "Stunning shot🔥",
                    "I really like this one!", "I like the mood 🖖", "Nice!"]

        try:
            hashtag = random.choice(hashtags)
            medias = cl.hashtag_medias_recent(hashtag, 10)
        except:
            print(datetime.now().strftime("%H:%M:%S"))
            print("Except 1")
            time.sleep(3600)
            continue

        for i, media in enumerate(medias):
            try:
                print(datetime.now().strftime("%H:%M:%S"))
                # cl.media_like(media.id)
                # print(f"Linked post number {i+1} of hashtag {hashtag}")
                if i % 2 == 0:
                    cl.user_follow(media.user.pk)
                    print(f"Followed user {media.user.username}")
                    comment = random.choice(comments)
                    cl.media_comment(media.id, comment)
                    print(f"Commented {comment} under post number {i+1}")
            except:
                print(datetime.now().strftime("%H:%M:%S"))
                print("Except 2")
                login_user(cl)
                continue
        time.sleep(3600)


def replace_caption_again(periodOfTime):
    print(f"You have selected {periodOfTime}!")

    cl = Client()

    login_user(cl)

    insights_media_feed_all = cl.insights_media_feed_all(
        "ALL", periodOfTime, "IMPRESSION_COUNT", 100, 10)
    print(f"Found: {len(insights_media_feed_all)} media!")

    for i, post in enumerate(insights_media_feed_all):
        print(datetime.now().strftime("%H:%M:%S"))
        postId = post["node"]["instagram_media_id"]
        print(f"Edit post ID: {postId}")
        postInfo = cl.media_info(postId).dict()
        postCaption = postInfo["caption_text"]
        postLocation = postInfo["location"]["pk"]
        print(postCaption)
        print(postInfo["location"]["name"])
        hashtag_list = []
        for word in postCaption.split():
            if word[0] == '#':
                hashtag_list.append(word[0:])
        clean_hashtag = re.sub(
            "#[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9_]+", "", postCaption)
        clean_spaces = re.sub(' +', ' ', clean_hashtag)
        random.shuffle(hashtag_list)
        for elem in hashtag_list:
            clean_spaces += elem + ' '
        print(clean_spaces)
        location_info = cl.location_info(postLocation)
        cl.media_edit(postId, clean_hashtag, "", [], location_info)
        print(Fore.RED + f"Clear post ID: {postId} finished!")
        print(Style.RESET_ALL)
        print(f"Location: {location_info}")
        cl.media_edit(postId, clean_spaces, "", [], location_info)
        print(Fore.GREEN + f"The post ID: {postId} has been edited again")
        print(Style.RESET_ALL)


def clearDmComments():
    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    cl = Client()
    cl.load_settings('session.json')
    cl.login(username, password)
    cl.get_timeline_feed()
    print(Fore.GREEN + f"get_settings!")
    print(Style.RESET_ALL)
    print(cl.get_settings())
    print(f"user_info({cl.user_id})!")

    insights_media_feed_all = cl.insights_media_feed_all(
        "IMAGE", "TWO_YEARS", "REACH_COUNT")
    print(f"Found: {len(insights_media_feed_all)} media!")

    for i, post in enumerate(insights_media_feed_all):
        postId = post["node"]["instagram_media_id"]
        print(f"Clear comment for post ID: {postId}")
        comments = cl.media_comments(postId)
        commentsToDelete = []
        for i, comment in enumerate(comments):
            comment = comment.dict()
            print(comment["text"])
            if '@' in comment["text"]:
                commentsToDelete.append(comment["pk"])
        print(commentsToDelete)
        if commentsToDelete:
            cl.comment_bulk_delete(postId, commentsToDelete)

    cl.logout()


def clearFollowing():
    cl = Client()

    login_user(cl)

    try:
        print(f"befor user_followers")
        followers = cl.user_followers(cl.user_id, 600)
        followers_arr = []
        for i, user in enumerate(followers):
            followers_arr.append(user.pk)
        print(f"after user_followers")
    except:
        login_user(cl)
        print(f"befor user_followers 2")
        followers = cl.user_followers(cl.user_id, 600)
        followers_arr = []
        for i, user in enumerate(followers):
            followers_arr.append(user)
        print(f"after user_followers 2")

    print(f"user_followers")
    print(followers_arr)
    print(len(followers_arr))

    try:
        print(f"befor user_following")
        following = cl.user_following(cl.user_id, 600)
        following_arr = []
        for i, user in enumerate(following):
            following_arr.append(user)
        print(f"after user_following")
    except:
        login_user(cl)
        print(f"befor user_following 2")
        following = cl.user_following(cl.user_id, 600)
        following_arr = []
        for i, user in enumerate(following):
            following_arr.append(user)
        print(f"after user_following 2")

    print(f"user_following")
    print(following_arr)
    print(len(following_arr))

    time.sleep(60)

    users_to_delete = []

    for i, user in enumerate(following_arr):
        if user not in followers_arr:
            users_to_delete.append(user)

    print(datetime.now().strftime("%H:%M:%S"))
    print(f"Users to delete:")
    print(users_to_delete)
    print(len(users_to_delete))

    for user in users_to_delete:
        time.sleep(120)
        print(datetime.now().strftime("%H:%M:%S"))
        try:
            print(user)
            user_info = cl.user_info(user)
            cl.user_unfollow(user)
            print(f"Succes unfollow user: {user_info.username}")
        except:
            print("Except")
            login_user(cl)
            print(user)
            user_info = cl.user_info(user)
            cl.user_unfollow(user)
            print(f"Succes unfollow user: {user_info.username}")


def main():
    main_menu_title = "  Insta & Sleep.\n  Press Q or Esc to quit. \n"
    main_menu_items = ["Replace caption",
                       "Like 20 most recent posts by #hashtag", "Create device", "Clear DM comments", "Clear useless Following", "Quit"]
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

    replace_caption_menu_title = "  Choose time.\n  Press Q or Esc to back to main menu. \n"
    replace_caption_menu_items = [
        "ONE_WEEK", "ONE_MONTH", "THREE_MONTHS", "SIX_MONTHS", "ONE_YEAR", "Back to Main Menu"]
    replace_caption_menu_back = False
    replace_caption_menu = TerminalMenu(
        replace_caption_menu_items,
        title=replace_caption_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not replace_caption_menu_back:
                replace_caption_sel = replace_caption_menu.show()
                if replace_caption_sel == 0:
                    replace_caption_again(
                        replace_caption_menu_items[replace_caption_sel])
                elif replace_caption_sel == 1:
                    replace_caption_again(
                        replace_caption_menu_items[replace_caption_sel])
                elif replace_caption_sel == 2:
                    replace_caption_again(
                        replace_caption_menu_items[replace_caption_sel])
                elif replace_caption_sel == 3:
                    replace_caption_again(
                        replace_caption_menu_items[replace_caption_sel])
                elif replace_caption_sel == 4:
                    replace_caption_again(
                        replace_caption_menu_items[replace_caption_sel])
                elif replace_caption_sel == 5 or replace_caption_sel == None:
                    replace_caption_menu_back = True
                    print("Back Selected")
            replace_caption_menu_back = False
        elif main_sel == 1:
            like_by_hashtag()
        elif main_sel == 2:
            createDevice()
        elif main_sel == 3:
            clearDmComments()
        elif main_sel == 4:
            clearFollowing()
        elif main_sel == 5 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
