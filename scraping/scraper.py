"""
Dellea-Sadwin Senior Project: THE SCRAPER v.1
1. Download matches page while "logged in" as user of choice (BETA: ONLY SADWIN)
2. Parse matches for usernames, appending to list while checking for repeats
3. Repeat steps 1 & 2 as desired.
4. For each username, download profile (still "logged in"!)
5. Parse profiles for data. (BUT NOT YET BECAUSE WE DON'T HAVE A DB)
Here we go!
"""

import requests
import http.cookiejar
import re
import pickle
import os
import time
import random

NUM_USERS_DESIRED = 50

DEFINITELY_CHROME = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/45.0.2454.85 Safari/537.36"}

"""
SADWIN_COOKIES = { "__cfduid" : "d2f8afb7f76247f3edc833502030460451441576259",
                   "authlink" : "6b28378b",
                   "nano" : "k%3Diframe_prefix_lock_1%2Ce%3D1442330317862%2Cv%3D1",
                   "session" : "8558839036192923775%3a17033598225515068147" }
"""


class HTTPResponseError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


"""
Recursively refreshes match page to find users until NUM_USERS_DESIRED is found.
Called with an initially empty list (users) from main unless a pickle is found.
"""
def find_matches(users, cj):
    try:
        matchURL = "http://okcupid.com/match"
        rget = requests.get(matchURL, headers=DEFINITELY_CHROME, cookies=cj)
        if rget.status_code != 200:
            raise HTTPResponseError(rget.status_code)

        newcookies = requests.utils.dict_from_cookiejar(rget.cookies)
        cj = requests.utils.add_dict_to_cookiejar(cj, newcookies)
        
        page = rget.text
        
        items = re.findall('"username" : "\w+",', page)
        print(items)
        for item in items:
            # item has form '"username" : "<USER_NAME>"'
            things = item.split('"')
            user = things[3]
            if user not in users and user != "sadwin" and user != "delleae":
                users.append(user)

        if len(users) < NUM_USERS_DESIRED:
            # this doesn't have to be returned probably? python is weird
            return find_matches(users, cj)
        else:
            return users
    except HTTPResponseError as e:
        print(e)
        return users


"""
Given a single username (user), downloads the profile of the user.
Saves to a text document of form user.txt.
"""
def download_user(user, cj):
    profileURL = "http://okcupid.com/profile/"+user
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME, cookies=cj)
    f = open("profiles/"+user+".txt", "w", errors="replace")
    f.write(rget.text)
    f.close()


def main():
    # option to open pickled cookies, or create new cookies for pickling.
    # also the least appetizing concept I have encountered in computer science
    filename = input("Enter cookie pickle name: ")
    try:
        cj = pickle.load(open(filename, "rb"))
    except OSError:
        print("Pickle not found. Create new cookie jar.")
        cookies = dict()
        cookies["__cfduid"] = input("__cfduid: ")
        cookies["authlink"] = input("authlink: ")
        cookies["nano"] = input("nano: ")
        cookies["session"] = input("session: ")
        cj = requests.utils.cookiejar_from_dict(cookies)
        pickle.dump(cj, open(filename, "wb"))

    username = input("Enter username: ")
    try:
        userlist = pickle.load(open(username+"_userlist.p", "rb"))
        if len(userlist) < NUM_USERS_DESIRED:
            userlist = find_matches(userlist, cj)
    # catches TypeError if pickled data is NoneType because ????
    except (OSError, TypeError):
        print("Pickle not found for this user. Making new userlist...")
        userlist = find_matches([], cj)
        pickle.dump(userlist, open(username+"_userlist.p", "wb"))

    if len(userlist) < NUM_USERS_DESIRED:
        print("Not enough users. Something may have gone wrong. Try again later.")
    else:
        print(userlist)
        lazy_breakpoint = input("Ok?")
        for u in userlist:
            if os.path.isfile("profiles/"+u+".txt"):
                print("Skipping "+u+", file already exists.")
                continue
            download_user(u, cj)
            print(u+" downloaded.")
            # i'm definitely not a robot okcupid. totally defintely. its fine
            waittime = int(5*random.random()) + 5
            time.sleep(waittime)
        print("Done!")
        # maybe lol

main()

