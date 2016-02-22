# -*- coding: utf-8 -*-
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

    def getLen_byID(self, user_id):
            """
            Returns the number we're looking for. hopefully.
            matching user_id in Users.

            If there is no matching user_id, returns an None.
            """
            sql = "SELECT wordCt FROM Users WHERE id='%s'"\
                  % (user_id)
            res = self.execute(sql)
            reslist = res.fetchall()
            if reslist == []:
                return None
            else:
                return reslist[0]

    def getUWords_byID(self, user_id):
            """
            Returns the number we're looking for. hopefully.
            matching user_id in Users.

            If there is no matching user_id, returns an None.
            """
            sql = "SELECT uniqueWords FROM Users WHERE id='%s'"\
                  % (user_id)
            res = self.execute(sql)
            reslist = res.fetchall()
            if reslist == []:
                return None
            else:
                return reslist[0]

   
def main():
    db = OKCdb('profiles.db')
    print ("database accessed!")
    numProfiles = 1558
    totLen = 0.0
    uProf = 0
    lProf = 0
    uniqueW = 0
    for i in range(1, numProfiles + 1):  #1650
        lenTup = (db.getLen_byID(i)[0])
        uTup = (db.getUWords_byID(i)[0])
        if(lenTup):
            totLen += lenTup
            lProf +=1
        if(uTup):
            uniqueW += uTup
            uProf += 1

    totLen /= lProf
    uniqueW /= uProf

    toPrint = "Average profile length ouf of " + str(lProf) + " profiles: " + str(totLen) + "\nAverage Unique Words Used across " + str(uProf) + " profiles: " + str(uniqueW)
    f = open("coredata.txt", "w")
    f.write(toPrint)
    f.close()
        
if __name__=='__main__':
    main()
