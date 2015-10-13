"""
Dellea-Sadwin Senior Project
So you've downloaded all your profiles and it was disturbingly easy.
Now, let's shove these users into your database!
"""
from profiledb import *
from bs4 import BeautifulSoup
import os


def get_text_from_tag(tag):
    if tag is None:
        return ""
    tagstr = str(tag)
    soup = BeautifulSoup(tagstr)
    text = soup.get_text()
    return text


def scrape_profile(filename, db):
    """
    Open file for username, turn it into beautiful soup.
    Find all of the desired tags and extract the text.
    Put all of the information into the database.
    """
    f = open("profiles/"+filename, "r")
    text = f.read()
    f.close()

    soup = BeautifulSoup(text)

    gender = get_text_from_tag(soup.find("span", "ajax_gender"))
    orientation = get_text_from_tag(soup.find(id="ajax_orientation"))
    gentation = get_text_from_tag(soup.find(id="ajax_gentation"))
    age = get_text_from_tag(soup.find(id="ajax_age"))
    location = get_text_from_tag(soup.find(id="ajax_location"))
    
    profile = []
    for i in range(10):
        tid = "essay_text_"+str(i)
        a = soup.find(id=tid)
        profile.append(get_text_from_tag(a))

    
    return db.insertUser(gender, orientation, gentation, age, location, profile[0],
                         profile[1], profile[2], profile[3], profile[4], profile[5],
                         profile[6], profile[7], profile[8], profile[9])

def main():
    db = OKCdb("profiles.db")
    for fname in os.listdir("profiles/"):
        scrape_profile(fname, db)
    
main()
