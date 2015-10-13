#!/usr/bin/python3
'''
sqllite3 wrapper for OKC Scraping (Richard Wicentowski, Doug Turnbull, Beth Dellea, 2010-2015)
Kelly and Beth's Kickass Senior Project 2k5ever
'''

import sqlite3
import re

class OKCdb(object):

    def __init__(self, dbfile):
        """
        Connect to the database specified by dbfile.  Assumes that this
        dbfile already contains the tables specified by the schema.
        """
        self.dbfile = dbfile
        self.cxn = sqlite3.connect(dbfile)
        self.cur = self.cxn.cursor()
        
        
        self.execute("""CREATE TABLE IF NOT EXISTS Users (
                                 id  INTEGER PRIMARY KEY,
                                 gender VARCHAR,
                                 orientation VARCHAR,
                                 lookingFor VARCHAR,
                                 age INTEGER,
                                 location VARCHAR,
                                 profile0 VARCHAR,
                                 profile1 VARCHAR,
                                 profile2 VARCHAR,
                                 profile3 VARCHAR,
                                 profile4 VARCHAR,
                                 profile5 VARCHAR,
                                 profile6 VARCHAR,
                                 profile7 VARCHAR,
                                 profile8 VARCHAR,
                                 profile9 VARCHAR
                            );""")
                  
                             
                                

    def _quote(self, text):
        """
        Properly adjusts quotation marks for insertion into the database.
        """

        text = re.sub("'", "''", text)
        return text

    def _unquote(self, text):
        """
        Properly adjusts quotations marks for extraction from the database.
        """

        text = re.sub("''", "'", text)
        return text

    def execute(self, sql):
        """
        Execute an arbitrary SQL command on the underlying database.
        """

        res = self.cur.execute(sql)
        self.cxn.commit()

        return res


    ####----------####
    #### Users ####

    '''gives id, then call the id gettng function and then use whatever general
    function we come up with to parse through whatever that returns'''

    def lookupUser_byOrientation(self, orientation):
        """
        Returns the id of the row matching orientation in Users.

        If there is no matching url, returns an None.
        """
        sql = "SELECT id FROM Users WHERE orientation='%s'" % (self._quote(orientation))
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist


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

    def lookupByAge(self, age):
        """
        Returns a Item ID for the row
        matching the requested age.

        If there is no match, returns an None.
        """
        sql = "SELECT id FROM Users WHERE age='%s'"\
              % (age)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist

    def lookupGentation(self, gentation):
        """
        Returns id applicable for a set lookingFor value
        """
        sql = "SELECT id FROM Users WHERE lookingFor='%s'"\
              % self._quote(gentation)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist
    
            
    def lookupbyLocation(self, location):
        """
        Returns id for the row
        matching location.

        If there is no match, returns an None.
        """
        sql = "SELECT id FROM Users WHERE location='%s'"\
              % self._quote(location)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist

  

    def insertUser(self, orientation, lookingFor, age, location, profile0, profile1,
                   profile2, profile3, profile4, profile5, profile6,
                   profile7, profile8, profile9):
        """Inserts a new user into the Users table, returning the id of the
        row."""        

        sql = """INSERT INTO Users (gender, orientation, lookingFor, age, location, profile0,
profile1, profile2, profile3, profile4, profile5, profile6, profile7, profile8, profile9)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',
                 '%s','%s','%s','%s','%s','%s')""" % (gender, orientation, lookingFor, age, location,
                                                      profile0, profile1, profile2, profile3,
                                                      profile4, profile5, profile6, profile7,
                                                      profile8, profile9)

        res = self.execute(sql)
        return self.cur.lastrowid
        


if __name__=='__main__':
    db = OKCdb('profiles.db')
    print ("database creaeted!")
    #userID  = db.insertUser("bird",":/", "enemies", "21", "ithaca", "part1", "part2","part3","this part doesnt seem to really exist","part5", "part6", "part7", "part8", "this part also doesnt exist", "part10")
    

   # print("User ID in the table: ", userID)
   # print(db.lookupUser_byID(userID))
   # print("Number of URLS: ", db.countURLs())

    print(db.lookupGentation("enemies"))
    


    
