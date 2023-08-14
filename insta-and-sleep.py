#!/usr/bin/env python3

import random
import time
import json
import os
import re
from colorama import Fore, Style
from simple_term_menu import TerminalMenu
from instagrapi import Client

# json.dumps(json.load(resp), indent=2)


def createDevice():
    print(f"You will be logged in!")
    client = Client()
    client.set_locale('pl_PL')
    client.set_country_code(48)  # +48
    # Los Angeles UTC (GMT) -7 hours == -25200 seconds
    client.set_timezone_offset(2 * 60 * 60)
    print(client.get_settings())
    client.dump_settings("dump.json")


def like_by_hashtag(hashtag):
    while True:
        with open("creds.txt", "r") as f:
            username, password = f.read().splitlines()
        client = Client()
        client.load_settings('dump.json')
        client.login(username, password)
        client.get_timeline_feed()
        print(Fore.GREEN + f"get_settings!")
        print(Style.RESET_ALL)
        print(client.get_settings())
        print(f"user_info({client.user_id})!")
        print(client.user_info(client.user_id))

        comments = ["Awesome", "Wonderful 💯", "This is such a moood !!!",
                    "👍📷❤️", "Wow that looks so amazing 😍😍😍"]

        medias = client.hashtag_medias_recent(hashtag, 6)

        for i, media in enumerate(medias):
            try:
                client.media_like(media.id)
                print(f"Linked post number {i+1} of hashtag {hashtag}")
                if i % 2 == 0:
                    client.user_follow(media.user.pk)
                    print(f"Followed user {media.user.username}")
                    comment = random.choice(comments)
                    client.media_comment(media.id, comment)
                    print(f"Commented {comment} under post number {i+1}")
            except:
                client.load_settings('dump.json')
                client.login(username, password)
                client.get_timeline_feed()
                continue
        time.sleep(3600)
        client.logout()


def replace_caption_again(periodOfTime):
    print(f"You have selected {periodOfTime}!")

    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    client = Client()
    client.load_settings('dump.json')
    client.login(username, password)
    client.get_timeline_feed()
    print(Fore.GREEN + f"get_settings!")
    print(Style.RESET_ALL)
    print(client.get_settings())
    print(f"user_info({client.user_id})!")

    insights_media_feed_all = client.insights_media_feed_all(
        "ALL", periodOfTime, "REACH_COUNT", 100, 10)
    print(f"Found: {len(insights_media_feed_all)} media!")

    for i, post in enumerate(insights_media_feed_all):
        postId = post["node"]["instagram_media_id"]
        print(f"Edit post ID: {postId}")
        postInfo = client.media_info(postId).dict()
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
        location_info = client.location_info(postLocation)
        client.media_edit(postId, clean_hashtag, "", [], location_info)
        print(Fore.RED + f"Clear post ID: {postId} finished!")
        time.sleep(15)
        print(Style.RESET_ALL)
        print(f"Location: {location_info}")
        client.media_edit(postId, clean_spaces, "", [], location_info)
        print(Fore.GREEN + f"The post ID: {postId} has been edited again")
        print(Style.RESET_ALL)

    client.logout()


def clearDmComments():
    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    client = Client()
    client.load_settings('dump.json')
    client.login(username, password)
    client.get_timeline_feed()
    print(Fore.GREEN + f"get_settings!")
    print(Style.RESET_ALL)
    print(client.get_settings())
    print(f"user_info({client.user_id})!")

    insights_media_feed_all = client.insights_media_feed_all(
        "IMAGE", "TWO_YEARS", "REACH_COUNT")
    print(f"Found: {len(insights_media_feed_all)} media!")

    for i, post in enumerate(insights_media_feed_all):
        postId = post["node"]["instagram_media_id"]
        print(f"Clear comment for post ID: {postId}")
        comments = client.media_comments(postId)
        commentsToDelete = []
        for i, comment in enumerate(comments):
            comment = comment.dict()
            print(comment["text"])
            if '@' in comment["text"]:
                commentsToDelete.append(comment["pk"])
        print(commentsToDelete)
        if commentsToDelete:
            client.comment_bulk_delete(postId, commentsToDelete)

    client.logout()


def clearFollowing():
    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    client = Client()
    client.load_settings('dump.json')
    client.login(username, password)
    client.get_timeline_feed()
    print(Fore.GREEN + f"get_settings!")
    print(Style.RESET_ALL)
    print(client.get_settings())
    print(f"user_info({client.user_id})!")

    followers = client.user_followers(client.user_id).keys()
    following = client.user_following(client.user_id).keys()

    users_to_delete = []

    for i, user in enumerate(following):
        print(i, user)
        if user not in followers:
            users_to_delete.append(user)

    print(f"Users to delete:")
    print(users_to_delete)

    for user in users_to_delete:
        try:
            print(user)
            user_info = client.user_info(user)
            client.user_unfollow(user)
            print(f"Succes unfollow user: {user_info.username}")
        except:
            client.load_settings('dump.json')
            client.login(username, password)
            client.get_timeline_feed()
            print(user)
            user_info = client.user_info(user)
            client.user_unfollow(user)
            print(f"Succes unfollow user: {user_info.username}")
    client.logout()


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

    like_by_hashtag_menu_title = "  Choose #hashtag.\n  Press Q or Esc to back to main menu. \n"
    like_by_hashtag_menu_items = [
        "spicollective", "streetphotography", "flor", "spi_geometry", "lensculture", "fujifilm", "Back to Main Menu"]
    like_by_hashtag_menu_back = False
    like_by_hashtag_menu = TerminalMenu(
        like_by_hashtag_menu_items,
        title=like_by_hashtag_menu_title,
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
            while not like_by_hashtag_menu_back:
                like_by_hashtag_sel = like_by_hashtag_menu.show()
                if like_by_hashtag_sel == 0:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 1:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 2:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 3:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 4:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 5:
                    print(
                        f"You have selected {like_by_hashtag_menu_items[like_by_hashtag_sel]}!")
                    like_by_hashtag(
                        like_by_hashtag_menu_items[like_by_hashtag_sel])
                elif like_by_hashtag_sel == 6 or like_by_hashtag_sel == None:
                    like_by_hashtag_menu_back = True
                    print("Back Selected")
            like_by_hashtag_menu_back = False
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
