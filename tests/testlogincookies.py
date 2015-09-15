"""
Dellea-Sadwin Senior Project
CURRENTLY IN DEVELOPMENT
Using a faked Chrome header matching Kelly's personal computer,
logs into OkCupid and stores cookies, hoping to avoid bot
detection.
"""


import requests
import http.cookiejar
import time
import random

definitelyChrome = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36" }
jar = http.cookiejar.CookieJar()
form = {"username":"sadwin", "password":"rememberme"}

r = requests.get("http://okcupid.com/login", data=form, headers=definitelyChrome, cookies=jar)


##for i in range(100):
##    something = urllib.request.urlopen(definitelyChrome)
##    print(something.getcode())
##    waittime = int(10*random.random())
##    time.sleep(waittime)
