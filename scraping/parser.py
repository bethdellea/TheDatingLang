import sqlite3
import re
from textblob import *


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

def tenseUsed(textSample):
    #figure this out I guesssssss
    return


#eventually have the data output to a .csv so excel can do work for us

if __name__=='__main__':
    db = OKCdb('profiles.db')
   # db.cur.execute("alter table Users add column '%s' 'float'" % "wordCt")
   # db.cur.execute("alter table Users add column '%s' 'float'" % "avgWrdLen")
   # db.cur.execute("alter table Users add column '%s' 'float'" % "avgSentLen")
   # ^^^ adding columns for the data we found and need to store. do for all new data fields. 
    print ("database accessed!")
    wordsSet = db.getText_byID(30)
    myWords = ""
    for item in wordsSet:
        myWords += item
    blob = TextBlob(myWords)
    print(blob)
    if(blob.detect_language()== "en"):
        
        blobList = blob.words
        wordct = len(blobList)
        print ("there are ",wordct," total words in this sample.")
        print ("thanks for making me do all this work.")
        avgWLen = avgWordLen(blobList)
        print("the average length of a word in this sample is ", avgWLen)

        blobSent = blob.sentences
        aSentLen = avgSentLen(blobSent)
        print("the average length of a sentence in this sample is ", aSentLen, " words")
        w = Word("cats")
        w = w.lemmatize()
        print(w)
    else:
        print("this blob was not in English. NOT COOL.")
