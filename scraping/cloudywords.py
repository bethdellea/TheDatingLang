from wordcloud import WordCloud
import matplotlib.pyplot as plot
import scipy
from PIL import Image
from os import path
import numpy as np
# this import style WILL NOT work in pycharm
from classificationstation import OKCdb, NUM_OF_PROFILES


STOPWORDS = { "I'm", "i'm", "I've", "i've", 'i', 'I', 'me', 'my', 'you', 'your', 'they', 'their', 'mine','a', 'an', 'the', 'and', 'but', 'or', 'of', 'to', 'as', 'is', 'in', 'up', 'at', 'on', 'that'}
#taking out pronouns now because I'm curious

d = path.dirname(__file__)


gal_mask = np.array(Image.open(path.join(d, "cloudimg/lady2.png")))
guy_mask = np.array(Image.open(path.join(d, "cloudimg/dude2.png")))
none_mask = np.array(Image.open(path.join(d, "cloudimg/noneGender.png")))
gay_mask = np.array(Image.open(path.join(d, "cloudimg/gay.png")))
str_mask = np.array(Image.open(path.join(d, "cloudimg/str8.png")))
f_gay_mask = np.array(Image.open(path.join(d, "cloudimg/galgay.png")))
m_gay_mask = np.array(Image.open(path.join(d, "cloudimg/dudegay.png")))


def generate_cloud(text, maskIn):
    cloud = WordCloud(background_color="white", relative_scaling=.5,
                      font_path="C:/Windows/Fonts/wensleydale_gothic_nbp.ttf",
                      mask=maskIn, stopwords=STOPWORDS).generate(text)
    plot.figure()
    plot.imshow(cloud)
    plot.axis("off")
    plot.show()


def isFemale(id, db):
    gender = db.getGender_byID(id)
    if gender is None:
        return None
    gender = ','.join(gender)
    if "Woman" in gender:
        return True
    elif "Man" in gender:
        return False
    else:
        return None


def isGay(id, db):
    orientation = db.getOrientation_byID(id)
    if orientation is None:
        return None
    orientation = ','.join(orientation)
    if "Straight" in orientation:
        return False
    else:
        return True


def lookingfor_everything(db, looking_for):
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if db.getLookingFor_byID(i)[0] == looking_for:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text, None)


def gender_everything(db, is_female_desired):
    mask = none_mask
    if is_female_desired == True:
        mask = gal_mask
    if is_female_desired == False:
        mask = guy_mask
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if isFemale(i, db) == is_female_desired:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text, mask)


def orientation_everything(db, is_gay_desired):
    mask = str_mask
    if is_gay_desired:
        mask = gay_mask

    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if isGay(i, db) == is_gay_desired:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text, mask)

def gender_orientation(db, is_gay_desired, is_female_desired):
    mask = none_mask
    if is_female_desired == True and is_gay_desired == True:
        mask = f_gay_mask 
    if is_female_desired == False and is_gay_desired == True:
        mask = m_gay_mask
    if is_female_desired == False and is_gay_desired == False:
        mask = guy_mask
    if is_female_desired == True and is_gay_desired == False:
        mask = gal_mask
    #currently the Straights get the basic lady/lord shapes, but that's not a
    # good way to be, because it's confusing and also it perpetuates the idea
    #   that straight is the standard and everything else is marked as abnormal
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if isFemale(i, db) == is_female_desired and isGay(i, db) == is_gay_desired:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text, mask)

def everyone_everything(db):
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        tiptup = db.getText_byID(i)
        if tiptup is not None:
            count += 1
            text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text, None)


def main():
    db = OKCdb("profiles.db")
    
    everyone_everything(db)
    #gender_everything(db, True)
    #gender_everything(db, False)
    #gender_everything(db, None)

    #orientation_everything(db, True)
    #orientation_everything(db, False)
    gender_orientation(db, True, True) #gay gals
    gender_orientation(db, True, False) #gay guys
    gender_orientation(db, False, True) #straight gals
    gender_orientation(db, False, False) #straight guys


if __name__ == "__main__":
    main()
