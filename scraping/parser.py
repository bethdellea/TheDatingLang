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


#eventually have the data output to a .csv so excel can do work for us
def doTheThing(profileID, db):
    print("\nworking on profile ", profileID)
    wordsSet = db.getText_byID(profileID)
    myWords = ""
    for item in wordsSet:
        myWords += item
    blob = TextBlob(myWords)
   # print(blob)
    if(len(myWords) > 3 and blob.detect_language()== "en"):
        
        blobList = blob.words
        wordct = len(blobList)
        #print ("there are ",wordct," total words in this sample.")
        returned = db.insertWCt(wordct, profileID)
        #print ("thanks for making me do all this work.")
        avgWLen = avgWordLen(blobList)
        #print("the average length of a word in this sample is ", avgWLen)
        returned2 = db.insertAvgWrdLen(avgWLen, profileID)
        blobSent = blob.sentences
        aSentLen = avgSentLen(blobSent)
        returned3 = db.insertAvgSentLen(aSentLen, profileID)
        #print("the average length of a sentence in this sample is ", aSentLen, " words")
        '''w = Word("cats")
        w = w.lemmatize()
        print(w)
        yeah this isn't worth our time rm
        '''
    else:
        print("this blob was either not in English or basically empty. NOT COOL.")


def main():
    db = OKCdb('profiles.db')
    # db.cur.execute("alter table Users add column '%s' 'float'" % "wordCt")
    # db.cur.execute("alter table Users add column '%s' 'float'" % "avgWrdLen")
    # db.cur.execute("alter table Users add column '%s' 'float'" % "avgSentLen")
    # ^^^ adding columns for the data we found and need to store. do for all new data fields. 
    print ("database accessed!")
    #will it let me pass the database in to the other function to save our efforts?
        #here's hoping
    
    for i in range(1296, 1650): #1129-1650 still need to go #not the most responsive solution but idgaf
        doTheThing(i, db)
#profile 1295 is mean.
if __name__=='__main__':
    main()

#punctuation use --- if word ct and sentence length are the same, the person
    #really had something against proper punctuation :/
  
