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
        
        
        self.execute("""CREATE TABLE IF NOT EXISTS TestMove (
                                 id  INTEGER PRIMARY KEY,
                                 gender VARCHAR,
                                 orientation VARCHAR,
                                 lookingFor VARCHAR
                            );""")
                  
    def addDestination(self):
        self.execute("""INSERT INTO testMove (gender, orientation, lookingFor) SELECT gender, orientation, lookingFor FROM testMove2;""")
        self.execute("""DROP TABLE testMove2;""")
                                

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

    def deleteEmpty(self, user_id):
        sql = "DELETE FROM testMove WHERE id='%s'"\
              % (user_id)
        res = self.execute(sql)


    def insertTests(self, gender, orientation, lookingFor):
        """Inserts a new user into the Users table, returning the id of the
        row."""        

        sql = """INSERT INTO testMove (gender, orientation, lookingFor)
                 VALUES ('%s','%s','%s')""" % (gender, orientation, lookingFor)

        res = self.execute(sql)
        return self.cur.lastrowid



if __name__=='__main__':
    db = OKCdb('profiles.db')
    print ("database accessed!")

    db.addDestination()


    
