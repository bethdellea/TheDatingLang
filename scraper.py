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

NUM_USERS_DESIRED = 100

DEFINITELY_CHROME = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36" }

SADWIN_COOKIES = { "__cfduid" : "d2f8afb7f76247f3edc833502030460451441576259",
                   "authlink" : "6b28378b",
                   "nano" : "k%3Diframe_prefix_lock_1%2Ce%3D1442330317862%2Cv%3D1",
                   "session" : "8558839036192923775%3a17033598225515068147",
                   "signup_exp_2014_09_13" : "2014_simpleblue" }

"""
Recursively refreshes match page to find users until NUM_USERS_DESIRED is found.
Called with an initially empty list (users) from main unless a pickle is found.
"""
def find_matches(users):
    matchURL = "http://okcupid.com/match"
    rget = requests.get(matchURL, headers=DEFINITELY_CHROME, cookies=SADWIN_COOKIES)
    page = rget.text
    
    items = re.findall('"username" : "\w+",', page)
    for item in items:
        #item has form '"username" : "<USER_NAME>"'
        things = item.split('"')
        user = things[3]
        if user not in users:
            users.append(user)

    #remove own username from list
    if len(users) < NUM_USERS_DESIRED:
        #this doesn't have to be returned probably? python is weird
        find_matches(users)
    else:
        return users


"""
Given a single username (user), downloads the profile of the user.
Saves to a text document of form user.txt.
"""
def download_users(user):
    profileURL = "http://okcupid.com/profile/"+user
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME, cookies=SADWIN_COOKIES)
    f = open(user+".txt", "w")
    f.write(rget.text)
    f.close()


def main():
    
