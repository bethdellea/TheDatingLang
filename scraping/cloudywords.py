from wordcloud import WordCloud
import matplotlib.pyplot as plot
# this import style may only work in pycharm
from scraping.classificationstation import OKCdb, NUM_OF_PROFILES


def generate_cloud(text):
    cloud = WordCloud(max_font_size=40, relative_scaling=.5, font_path="C:/Windows/Fonts/comic.ttf").generate(text)
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


def gender_everything(db, is_female_desired):
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if isFemale(i, db) == is_female_desired:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text)


def orientation_everything(db, is_gay_desired):
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        if isGay(i, db) == is_gay_desired:
            tiptup = db.getText_byID(i)
            if tiptup is not None:
                count += 1
                text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text)


def everyone_everything(db):
    text = ""
    count = 0
    for i in range(1, NUM_OF_PROFILES+1):
        tiptup = db.getText_byID(i)
        if tiptup is not None:
            count += 1
            text += '\r'.join(tiptup)
    print(count, "profiles")
    generate_cloud(text)


def main():
    db = OKCdb("profiles.db")
    everyone_everything(db)
    gender_everything(db, True)
    gender_everything(db, False)


if __name__ == "__main__":
    main()
