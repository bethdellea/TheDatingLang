"""
Dellea-Sadwin Senior Project
Contains the barebones functionality to scrape and print desired
data from one OkCupid user profile (already downloaded and stored
in file "beth.txt" to avoid repeatedly downloading a page during
testing)
Now with database testing!
"""

from testingDb import *
from bs4 import BeautifulSoup


beth = open("beth.txt", "r")

bethtxt = beth.read()

bethsoup = BeautifulSoup(bethtxt)

gendertag = bethsoup.find("span", "ajax_gender")
gendertag = str(gendertag)
gendersoup = BeautifulSoup(gendertag)
gender = gendersoup.get_text()

orientag = bethsoup.find(id="ajax_orientation")
orientag = str(orientag)
orientsoup = BeautifulSoup(orientag)
orientation = orientsoup.get_text()

gentag = bethsoup.find(id="ajax_gentation")
gentag = str(gentag)
gentsoup = BeautifulSoup(gentag)
gentation = gentsoup.get_text()

agetag = bethsoup.find(id="ajax_age")
agetag = str(agetag)
agesoup = BeautifulSoup(agetag)
age = agesoup.get_text()

loctag = bethsoup.find(id="ajax_location")
loctag = str(loctag)
locsoup = BeautifulSoup(loctag)
location = locsoup.get_text()

profile = []
for i in range(10):
    tid = "essay_text_"+str(i)
    a = bethsoup.find(id=tid)
    if a is not None:
        aboutsoup = BeautifulSoup(str(a))
        profile.append(aboutsoup.get_text())
    else:
        profile.append("")

db = OKCdb("poop.db")

profile_id = db.insertUser(gender, orientation, gentation, age, location,
                           profile[0], profile[1], profile[2], profile[3],
                           profile[4], profile[5], profile[6], profile[7],
                           profile[8], profile[9])


print(db.lookupUser_byID(profile_id))


