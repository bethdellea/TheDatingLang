#Beth pulling code we already wrote out into its own file so numpy doesn't have to be
        #wrestled onto another computer before Thursday
#May 10, 2016


import sqlite3
import re
from textblob import *


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

    def getLookingFor_byID(self, user_id):
        """
        Returns orientation from profiles, or None if no matching user_id
        """
        sql = "SELECT lookingFor FROM Users WHERE id='%s'" % user_id
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

    def getProfile_byContains(self, phrase):
        '''returns EVERYTHING for the row which contains searched phrases
          if there is no matching contents, returns a None'''
        sql = "SELECT * from Users WHERE profile0 LIKE '" + phrase + "' OR profile1 LIKE '" + phrase + "' OR profile2 LIKE '" + phrase + "' OR profile3 LIKE \
        '" + phrase + "' OR profile4 LIKE '" + phrase + "' OR profile5 LIKE '" + phrase + "' OR profile6 LIKE '" + phrase + "' OR profile7 LIKE \
        '" + phrase + "' OR profile8 LIKE '" + phrase + "' OR profile9 LIKE '" + phrase + "'"
        res = self.execute(sql)
        reslist = res.fetchall()
        if(reslist) == []:
            return None
        else:
            return reslist

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

    def getColumn_byID(self, user_id, column_name):
        """
        Because I'm kind of done writing a million functions when I could have just written one
        :param user_id: primary key of user in db
        :param column_name: str name of column
        :return: data in column column_name for user with id user_id
        """
        sql = "SELECT %s FROM Users WHERE id='%s'" % (column_name, user_id)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0][0]
