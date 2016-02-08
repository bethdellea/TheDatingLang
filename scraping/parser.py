# -*- coding: utf-8 -*-
import sqlite3
import re
from textblob import *
from nltk.stem.porter import *
from collections import defaultdict



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

    def insertAdjAdv(self, adjadv, idNum):
        """Inserts the percent of the profile that is adjective or adverb into the database"""        
        sql = """UPDATE Users  SET advAdjPct= '%s' WHERE Id='%s'""" % (adjadv, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid

    def insertUniqueWds(self, numWords, idNum):
        """Inserts the number of unique words in the profile into the db"""
        sql = """UPDATE Users  SET uniqueWords= '%s' WHERE Id='%s'""" % (numWords, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid

    def insertPolarity(self, pol, idNum):
        """Inserts the polarity rating of the profile into the db"""
        sql = """UPDATE Users  SET polarity= '%s' WHERE Id='%s'""" % (pol, idNum)
        res = self.execute(sql)
        return self.cur.lastrowid

    def insertSubjectivity(self, subj, idNum):
        """Inserts the number of unique words in the profile into the db"""
        sql = """UPDATE Users  SET subjectivity= '%s' WHERE Id='%s'""" % (subj, idNum)
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
    return (out/wdcount)


def unique_words(tokens):
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens]
    stem_dict = defaultdict(int)
    for word in stemmed:
        if word in stem_dict:
            stem_dict[word] += 1
        else:
            stem_dict[word] = 1
    #return len(stemmed)
    return len(stem_dict)


def sentiment_analysis(sentences):
    polarity = 0
    subjectivity = 0
    for sent in sentences:
        polarity += sent.sentiment.polarity
        subjectivity += sent.sentiment.subjectivity
    polarity /= len(sentences)
    subjectivity /= len(sentences)
    return polarity, subjectivity

#the things we've already done but probably still want the functions for
#leaving like this bc I had to call it earlier and we may need to do so again
def doneThings(profileID, db):
    wordsSet = db.getText_byID(profileID)
    myWords = ""
    if(wordsSet):
        for item in wordsSet:
            myWords += item
    else:
        myWords = "none"

    blob = TextBlob(myWords)
   # print(blob)
    if(len(myWords.split()) > 5 and blob.detect_language()== "en" ):
        #and actualWords(myWords)
        tokens = blob.words
        wordct = len(tokens)
        if(wordct > 3): #this pulls out the punctuation for us so it works around the empty!!
            '''from inside the for loop and if statement of doTheThing'''
            #tokens = blob.words
            #wordct = len(tokens)
            #print ("there are ",wordct," total words in this sample.")
            returned = db.insertWCt(wordct, profileID)
            #print ("thanks for making me do all this work.")
            avgWLen = avgWordLen(tokens)
            #print("the average length of a word in this sample is ", avgWLen)
            returned2 = db.insertAvgWrdLen(avgWLen, profileID)
            blobSent = blob.sentences
            aSentLen = avgSentLen(blobSent)
            eturned3 = db.insertAvgSentLen(aSentLen, profileID)
            #print("the average length of a sentence in this sample is ", aSentLen, " words")

#some profiles were different charsets and got stored as ???
    #unfortunately they're long enough to get past the filter, so we need to try harder
    #I (Beth) found a more eloquent way of doing this,leaving it here for posterity mostly
def actualWords(wordsToCheck):
    wordsToCheck = wordsToCheck.split()
    totalAnum = 0
    totalChars = 0
    for word in wordsToCheck:
        for char in word:
            totalChars +=1
            if(char.isalnum()):
                totalAnum +=1
    if (totalChars - totalAnum >= totalChars/2):
        #if more than half of your profile is not a-z, 1-9, we don't want your data!
        return False
    return True

#eventually have the data output to a .csv so excel can do work for us
def doTheThing(profileID, db):
    print("\nworking on profile ", profileID)
    wordsSet = db.getText_byID(profileID)
    myWords = ""
    if(wordsSet):
        for item in wordsSet:
            myWords += item
    else:
        myWords = "none"

    blob = TextBlob(myWords)
   # print(blob)
    if(len(myWords.split()) > 5 and blob.detect_language()== "en" ):
        #and actualWords(myWords)
        tokens = blob.words
        wordct = len(tokens)
        if(wordct > 3): #this pulls out the punctuation for us so it works around the empty!!
            '''
            adjadv_pct = adj_adv(blob, wordct)
            sents = sentiment_analysis(blob.sentences)
            pol = sents[0]
            subj = sents[1]
            '''
            unique = unique_words(tokens)
            '''
            # do something with these
            db.insertAdjAdv(adjadv_pct, profileID)
            db.insertPolarity(pol, profileID)
            db.insertSubjectivity(subj, profileID)
            '''
            db.insertUniqueWds(unique, profileID)
                
    else:
        print("this blob was either not in English or basically empty. NOT COOL.")


def main():
    db = OKCdb('profiles.db')
    #db.cur.execute("alter table Users add column '%s' 'float'" % "advAdjPct")
    #db.cur.execute("alter table Users add column '%s' 'int'" % "uniqueWords")
    #db.cur.execute("alter table Users add column '%s' 'float'" % "polarity")
    #db.cur.execute("alter table Users add column '%s' 'float'" % "subjectivity")
    # ^^^ adding columns for the data we found and need to store. do for all new data fields. 
    print ("database accessed!")
    #will it let me pass the database in to the other function to save our efforts?
        #here's hoping
    
    
    for i in range(1, 1715):  #1650

        doTheThing(i, db)
    

        
if __name__=='__main__':
    main()

#punctuation use --- if word ct and sentence length are the same, the person
    #really had something against proper punctuation :/
  
