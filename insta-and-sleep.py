#!/usr/bin/env python3

import random
import time
import json
import os
import re
from colorama import Fore, Style
from simple_term_menu import TerminalMenu
from instagrapi import Client

# with open("creds.txt", "r") as f:
#     username, password = f.read().splitlines()

# client = Client()
# client.login(username, password)


# hashtag = "spicollective"
# comments = ["Awesome", "Wonderful 💯", "This is such a moood !!!",
#             "👍📷❤️", "Wow that looks so amazing 😍😍😍"]

# medias = client.hashtag_medias_recent(hashtag, 20)

# for i, media in enumerate(medias):
#     client.media_like(media.id)
#     print(f"Linked post number {i+1} of hashtag {hashtag}")
#     if i % 5 == 0:
#         client.user_follow(media.user.pk)
#         print(f"Followed user {media.user.username}")
#         comment = random.choice(comments)
#         client.media_comment(media.id, comment)
#         print(f"Commented {comment} under post number {i+1}")


# insights_media_feed_all = client.insights_media_feed_all(
#     "ALL", "THREE_MONTHS", "PROFILE_VIEW")

# postId = insights_media_feed_all[1]["node"]["instagram_media_id"]

# postInfo = client.media_info(postId).dict()
# postCaption = postInfo["caption_text"]
# postLocation = postInfo["location"]["pk"]

# client.media_edit(postId, "", "", [], None)
# print(f"clear post")
# time.sleep(41)

# print(json.dumps(postInfo, indent=2, sort_keys=True, default=str))
# print(postCaption)
# print(postLocation)
# locationInfo = client.location_info(postLocation)
# mediaInfo = client.media_edit(postId, postCaption, "", [], locationInfo)
# print(f"post editet again")

# print(json.dumps(mediaInfo, indent=2))

def like_by_hashtag(hashtag):

    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    client = Client()
    client.login(username, password)

    comments = ["Awesome", "Wonderful 💯", "This is such a moood !!!",
                "👍📷❤️", "Wow that looks so amazing 😍😍😍"]

    medias = client.hashtag_medias_recent(hashtag, 20)

    for i, media in enumerate(medias):
        client.media_like(media.id)
        print(f"Linked post number {i+1} of hashtag {hashtag}")
        if i % 5 == 0:
            client.user_follow(media.user.pk)
            print(f"Followed user {media.user.username}")
            comment = random.choice(comments)
            client.media_comment(media.id, comment)
            print(f"Commented {comment} under post number {i+1}")


def replace_caption_again(periodOfTime):
    print(f"You have selected {periodOfTime}!")

    with open("creds.txt", "r") as f:
        username, password = f.read().splitlines()
    client = Client()
    client.login(username, password)

    insights_media_feed_all = client.insights_media_feed_all(
        "ALL", periodOfTime, "LIKE_COUNT", 100, 20)
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
        time.sleep(25)
        print(Style.RESET_ALL)
        print(f"Location: {location_info}")
        client.media_edit(postId, clean_spaces, "", [], location_info)
        print(Fore.GREEN + f"The post ID: {postId} has been edited again")
        print(Style.RESET_ALL)


def main():
    main_menu_title = "  Insta & Sleep.\n  Press Q or Esc to quit. \n"
    main_menu_items = ["Replace caption",
                       "Like 20 most recent posts by #hashtag", "Quit"]
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
        "spicollective", "streetphotography", "flor", "spi_geometry", "lensculture", "Back to Main Menu"]
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
                elif like_by_hashtag_sel == 5 or like_by_hashtag_sel == None:
                    like_by_hashtag_menu_back = True
                    print("Back Selected")
            like_by_hashtag_menu_back = False
        elif main_sel == 2 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
