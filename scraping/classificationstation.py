import sqlite3
import re
from textblob import *
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


NUM_OF_PROFILES = 1650


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

    def insertWCt(self, wCT, idNum):
        """Inserts the word count into the database"""        
        sql = """UPDATE Users  SET wordCt= '%s' WHERE Id='%s'""" % (wCT, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid

    def insertAvgWrdLen(self, wLen, idNum):
        """Inserts the average word length into the database"""        
        sql = """UPDATE Users  SET avgWrdLen= '%s' WHERE Id='%s'""" % (wLen, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid

    def insertAvgSentLen(self, sentLen, idNum):
        """Inserts the average sentence length into the database"""        
        sql = """UPDATE Users  SET avgSentLen= '%s' WHERE Id='%s'""" % (sentLen, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid


def avgWordLen(wordList):
    sz = len(wordList)
    length = 0
    for word in wordList:
        length += len(word)
    avg = length/sz
    return avg


def avgSentLen(sentList):
    length = 0
    sz = len(sentList)
    for sent in sentList:
        sentWords = sent.words
        length += len(sentWords)
    avg = length/sz
    return avg

from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from .parser import OKCdb

def tenseUsed(textSample):
    #figure this out I guesssssss
    return


def pronouns(blob):
    """
    Each time a PRP or PRP$ is found, add the pronoun to a dict of counts.
    """
    pronounDict = {}
    tagList = blob.tags
    for word, pos in tagList:
        if pos == "PRP" or pos == "PRP$":
            word = word.lower()
            if word not in pronounDict.keys():
                pronounDict[word] = 1
            else:
                pronounDict[word] += 1
    # how shall we store this information? i do not know. here is a dict
    for word in pronounDict.keys():
        print(word+": "+str(pronounDict[word]))
    return pronounDict


def adj_adv(blob, wdcount):
    posTagList = ["JJ","JJR","JJS","RB","RBR","RBS"]
    out = 0.0
    for word, pos in blob.tags:
        if pos in posTagList:
            out += 1
    return out/wdcount


def unique_words(tokens):
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens]
    return len(stemmed)


def sentiment_analysis(sentences):
    polarity = 0
    subjectivity = 0
    for sent in sentences:
        polarity += sent.sentiment.polarity
        subjectivity += sent.sentiment.subjectivity
    polarity /= len(sentences)
    subjectivity /= len(sentences)
    return polarity, subjectivity


# the things we've already done but probably still want the functions for
def doneThings(profileID, db):
    '''from inside the for loop and if statement of doTheThing'''
    tokens = blob.words
    wordct = len(tokens)
    print ("there are ",wordct," total words in this sample.")
    returned = db.insertWCt(wordct, profileID)
    print ("thanks for making me do all this work.")
    avgWLen = avgWordLen(tokens)
    print("the average length of a word in this sample is ", avgWLen)
    returned2 = db.insertAvgWrdLen(avgWLen, profileID)
    blobSent = blob.sentences
    aSentLen = avgSentLen(blobSent)
    eturned3 = db.insertAvgSentLen(aSentLen, profileID)
    print("the average length of a sentence in this sample is ", aSentLen, " words")
        

# eventually have the data output to a .csv so excel can do work for us
def doTheThing(profileID, db):
    print("\nworking on profile ", profileID)
    wordsSet = db.getText_byID(profileID)
    myWords = ""
    for item in wordsSet:
        myWords += item
    blob = TextBlob(myWords)
    # print(blob)
    if(len(myWords) > 3 and blob.detect_language()== "en"):
        
        tokens = blob.words
        wordct = len(tokens)
        adjadv_pct = adj_adv(blob, wordct)
        pol, subj = sentiment_analysis(blob.sentences)
        unique = unique_words(tokens)
        # do something with these
                
    else:
        print("this blob was either not in English or basically empty. NOT COOL.")


def tokenize(text):
    blob = TextBlob(text)
    if len(text) < 3 or blob.detect_language() != "en":
        return None
    tokens = blob.words
    # stemmed_tokens = textblob.packages.nltk.stem idk wowejfkdwnoskfnws
    return tokens


def clustering(db):
    corpus = {}
    for i in range(1, NUM_OF_PROFILES+1):
        text = '\r'.join(db.getText_byID(i))
        if len(text) > 10:
            corpus[text] = i
    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(corpus.keys())
    print(matrix)
    print(tfidf.get_feature_names())
    km2 = KMeans(n_clusters=2)
    km2.fit(matrix)
    clusters = km2.labels_.tolist()
    print(clusters)


def main():
    db = OKCdb('profiles.db')
    #db.cur.execute("alter table Users add column '%s' 'float'" % "advAdjPct")
    #db.cur.execute("alter table Users add column '%s' 'int'" % "uniqueWords")
    #db.cur.execute("alter table Users add column '%s' 'float'" % "polarity")
    #db.cur.execute("alter table Users add column '%s' 'float'" % "subjectivity")
    # ^^^ adding columns for the data we found and need to store. do for all new data fields. 
    print("database accessed!")
    #will it let me pass the database in to the other function to save our efforts?
        #here's hoping

    clustering(db)
    
    """
    for i in range(1296, 1650): #1129-1650 still need to go #not the most responsive solution but idgaf

        doTheThing(i, db)
    #profile 1295 is mean.
    """

if __name__ == '__main__':
    main()

#punctuation use --- if word ct and sentence length are the same, the person
    #really had something against proper punctuation :/



main()

