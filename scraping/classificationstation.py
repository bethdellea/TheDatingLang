"""
It's not even classification, it's clustering.
See brandonrose.org/clustering for possibly relevant example of TfidfVectorizer
See http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting for documentation
TfidfVectorizer takes a corpus parameter as a list of texts.
"""


import sqlite3
import re
from textblob import *
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plot
import numpy

NUM_OF_PROFILES = 1558
NUM_CLUSTERS = 4

class OKCdb(object):
    def __init__(self, dbfile):
        """
        Connect to the database specified by dbfile.  Assumes that this
        dbfile already contains the tables specified by the schema.
        """
        self.dbfile = dbfile
        self.cxn = sqlite3.connect(dbfile)
        self.cur = self.cxn.cursor()

    def execute(self, sql):
        """
        Execute an arbitrary SQL command on the underlying database.
        """

        res = self.cur.execute(sql)
        self.cxn.commit()

        return res
    

    def lookupUser_byID(self, user_id):
        """
        Returns EVERYTHING for the row in some mysterious format
        matching user_id in Users.

        If there is no matching user_id, returns an None.
        """
        sql = "SELECT * FROM Users WHERE id='%s'"\
              % (user_id)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]

    def getGender_byID(self, user_id):
        """
        Returns gender from profiles, or None if no matching user_id
        """
        sql = "SELECT gender FROM Users WHERE id='%s'" % user_id
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]

    def getOrientation_byID(self, user_id):
        """
        Returns orientation from profiles, or None if no matching user_id
        """
        sql = "SELECT orientation FROM Users WHERE id='%s'" % user_id
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]

    def getText_byID(self, user_id):
        """
        Returns tha text from profiles for the row in some mysterious format
        matching user_id in Users.

        If there is no matching user_id, returns an None.
        """
        sql = "SELECT profile0, profile1, profile2, profile3, profile4, profile5, profile6, profile7, profile8, profile9 FROM Users WHERE id='%s'"\
              % (user_id)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]


def tokenize(text):
    blob = TextBlob(text)
    if len(text) < 3 or blob.detect_language() != "en":
        return None
    tokens = blob.words
    # stemmed_tokens = textblob.packages.nltk.stem idk wowejfkdwnoskfnws
    return tokens


def bargraph_orientation(db, clusters):
    width = .4
    straights = [0] * NUM_CLUSTERS
    gays = [0] * NUM_CLUSTERS
    for user_id in range(len(clusters)):
        orientation = db.getOrientation_byID(user_id+1)
        print(orientation)
        if " Straight " in orientation:
            straights[clusters[user_id]] += 1
        else:
            gays[clusters[user_id]] += 1

    ind = numpy.arange(NUM_CLUSTERS)
    fig, ax = plot.subplots()
    straight_rectangles = ax.bar(ind, straights, width, color='b')
    gay_rectangles = ax.bar(ind+width, gays, width, color='m')

    plot.show()


def bargraph_gender(db, clusters):
    width = .2
    men = [0] * NUM_CLUSTERS
    women = [0] * NUM_CLUSTERS
    other = [0] * NUM_CLUSTERS
    for user_id in range(len(clusters)):
        gender = db.getGender_byID(user_id+1)
        if "Man" in gender:
            men[clusters[user_id]] += 1
        elif "Woman" in gender:
            women[clusters[user_id]] += 1
        else:
            other[clusters[user_id]] += 1

    ind = numpy.arange(NUM_CLUSTERS)
    fig, ax = plot.subplots()
    manly_rectangles = ax.bar(ind, men, width, color='b')
    womanly_rectangles = ax.bar(ind+width, women, width, color='m')
    genderless_rectangles = ax.bar(ind+2*width, other, width, color='g')

    plot.show()




def clustering(db):
    corpus = []
    for i in range(1, NUM_OF_PROFILES+1):
        text = '\r'.join(db.getText_byID(i))
        corpus.append(text)
    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(corpus)
    print(matrix)
    km2 = KMeans(n_clusters=NUM_CLUSTERS)
    km2.fit(matrix)
    clusters = km2.labels_.tolist()
    print(clusters)
    bargraph_gender(db, clusters)
    bargraph_orientation(db, clusters)


def main():
    db = OKCdb('profiles.db')
    print("database accessed!")
    clustering(db)


if __name__ == '__main__':
    main()

#punctuation use --- if word ct and sentence length are the same, the person
    #really had something against proper punctuation :/