from wordcloud import WordCloud
import matplotlib.pyplot as plot
from textblob import TextBlob
# this import style may only work in pycharm
from scraping.classificationstation import OKCdb, NUM_OF_PROFILES


STOPWORDS = {'a', 'an', 'the', 'and', 'but', 'or', 'of', 'to', 'as', 'is', 'in', 'up', 'at', 'on', 'that'}


def generate_cloud(text):
    cloud = WordCloud(max_font_size=40, relative_scaling=.5, font_path="C:/Windows/Fonts/comic.ttf",
                      stopwords=STOPWORDS).generate(text)
    blob = TextBlob(text)
    print(sorted( ((v,k) for k,v in dict(blob.word_counts).items()), reverse=True))

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
    generate_cloud(text)


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


def calc_stats(data):
    """
    For use with t_test_math. Gets std dev and mean.
    :param data: List of data! Yup.
    :return: (Std dev, mean) tuple
    """
    mean = 0
    for d in data:
        mean += d
    mean /= len(data)

    s = 0
    for d in data:
        s += (d - mean)**2/(len(data)-1)
    s **= 0.5  # HAHAHA THIS IS THE SILLIEST LOOKING THING I'VE EVER SEEN

    return s, mean


def t_test_math(list1, list2):
    """
    Where the REAL MATH begins.
    :param list1: List of raw data for group 1.
    :param list2: List of raw data for group 2.
    :return: (Degrees of freedom, t-value) tuple, for lookup.
    """
    s1, mean1 = calc_stats(list1)
    s2, mean2 = calc_stats(list2)

    sd = (s1**2/len(list1) + s2**2/len(list2)) ** 0.5

    t = (mean1-mean2)/sd

    degrees = len(list1) + len(list2) - 2

    return degrees, t


def t_test_gender(db, column_name):
    dudes = []
    ladies = []
    for i in range(1, NUM_OF_PROFILES+1):
        is_female = isFemale(i, db)
        if is_female:
            datum = db.getColumn_byID(i, column_name)
            if datum:
                ladies.append(datum)
        elif is_female == False:
            datum = db.getColumn_byID(i, column_name)
            if datum:
                dudes.append(datum)
    degrees, t = t_test_math(ladies, dudes)
    print(degrees, t)


def t_test_orientation(db, column_name):
    straights = []
    gays = []
    for i in range(1, NUM_OF_PROFILES+1):
        is_gay = isGay(i, db)
        if is_gay:
            datum = db.getColumn_byID(i, column_name)
            if datum:
                gays.append(datum)
        elif is_gay == False:
            datum = db.getColumn_byID(i, column_name)
            if datum:
                straights.append(datum)
    degrees, t = t_test_math(gays, straights)
    print(degrees, t)


def t_test_gentation(db, column_name):
    girllovers = []
    boylovers = []
    for i in range(1, NUM_OF_PROFILES+1):
        looking_for = db.getLookingFor_byID(i)[0]
        if looking_for == " Women ":
            datum = db.getColumn_byID(i, column_name)
            if datum:
                girllovers.append(datum)
        elif looking_for == " Men ":
            datum = db.getColumn_byID(i, column_name)
            if datum:
                boylovers.append(datum)
    degrees, t = t_test_math(girllovers, boylovers)
    print(degrees, t)


def main():
    db = OKCdb("profiles.db")
    columns = ["wordCt", "avgWrdLen", "avgSentLen", "advAdjPct", "uniqueWords", "polarity", "subjectivity"]
    print("GENDER")
    for c in columns:
        print(c, end=": ")
        t_test_gender(db, c)
    print("ORIENTATION")
    for c in columns:
        print(c, end=": ")
        t_test_orientation(db, c)
    print("LOOKING FOR")
    for c in columns:
        print(c, end=": ")
        t_test_gentation(db, c)
    """
    # everyone_everything(db)
    gender_everything(db, True)
    gender_everything(db, False)
    gender_everything(db, None)

    orientation_everything(db, True)
    orientation_everything(db, False)
    """


if __name__ == "__main__":
    main()
