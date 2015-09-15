"""
Dellea-Sadwin Senior Project
CURRENTLY IN DEVELOPMENT
Using a faked Chrome header and some hand-copied cookies,
trying to access OkCupid match page.
"""

import requests
import http.cookiejar

definitelyChrome = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36" }

cookies = { "__cfduid" : "d2f8afb7f76247f3edc833502030460451441576259",
            "authlink" : "6b28378b",
            "nano" : "k%3Diframe_prefix_lock_1%2Ce%3D1442330317862%2Cv%3D1",
            "session" : "8558839036192923775%3a17033598225515068147",
            "signup_exp_2014_09_13" : "2014_simpleblue" }


rget = requests.get("http://okcupid.com/match", headers=definitelyChrome, cookies=cookies)

text = rget.text
print(text)

f = open("matchesmaybe.txt", 'w')

f.write(text)

f.close()
