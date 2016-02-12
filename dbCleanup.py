''' Feb 8, 2016 ---- we need to get rid of the profiles in our database
which are empty or encoded wrong and totally useless to us. It'll make life a
lot easier for us down the line.
- Beth (hello yes that was a weirdly long opening comment. ANYway.)
'''

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

    def deleteEmpty(self, user_id):
        sql = "DELETE FROM Users WHERE id='%s'"\
              % (user_id)
        res = self.execute(sql)




def swapDBTables:
    #borrowed from a sqlfiddle linked to by a stack overflow post
        #this is the basic process we'll need to do
    #but we'll look cooler doing it
    '''

    CREATE TABLE test (
      _id INTEGER PRIMARY KEY AUTOINCREMENT,
      value VARCHAR(32)
    );

    INSERT INTO test (value) VALUES ('Value#1');
    INSERT INTO test (value) VALUES ('Value#2');
    INSERT INTO test (value) VALUES ('Value#3');

    DELETE FROM test WHERE _id=2;

    CREATE TABLE test2 AS SELECT * FROM test;
    DELETE FROM test;
    DELETE FROM sqlite_sequence WHERE name='test';
    INSERT INTO test (value) SELECT value FROM test2;
    DROP TABLE test2;
    '''


#eventually have the data output to a .csv so excel can do work for us
def doTheCleanup(profileID, db):
    print("\nevaluating profile ", profileID)
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
        if(wordct < 3):
            print("This profile is too short and will be deleted")
            #this pulls out the punctuation for us so it works around the empty!!
            #if there are fewer than 3 words we can dump it
            db.deleteEmpty(profileID)
    else:
        print("This profile is either too short or not in English and will be deleted.")
        #also delete it here if there are basically no english words
   




def main():
    db = OKCdb('profiles.db')
    
    #db.cur.execute("alter table Users add column '%s' 'float'" % "subjectivity")
    # ^^^ adding columns for the data we found and need to store. do for all new data fields. 
    print ("database accessed!")
    #will it let me pass the database in to the other function to save our efforts?
        #here's hoping
    
    
    for i in range(1, 1715):  #1650

        doTheCleanup(i, db)
    

        
if __name__=='__main__':
    main()
