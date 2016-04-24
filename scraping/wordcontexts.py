#Beth fooling aroud while trying to get contexts for phrasings
#April 23/24, 2016 (technically it's the 24th but I haven't gone to sleep yet)

from classificationstation import OKCdb, NUM_OF_PROFILES
from textblob import TextBlob

# added getProfile_byContains(self, phrase) to OKCdb in parser.py and classificationstation.py
# it should be a big help here

def parseAndQuery(db, toSearch):
    toSearch = "%" + toSearch + "%"
    results = db.getProfile_byContains(toSearch)
    return results

def displayResults(toShow, toSearch):
    '''prints out demographics and the section of their profile the phrase appears in'''
    #leveled up function TODO --- print out which section it was from and just the sentence it appeared in
    #make own functio and choice in loop I think, will do after sleeping maybe
    print("Total profiles containing ", toSearch, ": ", len(toShow))
    toSearch = toSearch.lower()
    for item in toShow:
        print("\n\n")
        print("ID #: ", item[0], "\tGender: ", item[1], "\tAge: ", item[4], "\tLocation: ", item[5])
        print("Orientation: ", item[2], "\tLookinng For: ",item[3])
        if toSearch in item[6] or toSearch.capitalize() in item[6] or toSearch.upper() in item[6]:
            print("Self Summary: ", item[6])
        if toSearch in item[7] or toSearch.capitalize() in item[7] or toSearch.upper() in item[7]:
            print("What I'm Doing With My Life: ", item[7])
        if toSearch in item[8] or toSearch.capitalize() in item[8] or toSearch.upper() in item[8]:
            print("I'm Really Good At: ",  item[8])
        if toSearch in item[9] or toSearch.capitalize() in item[9] or toSearch.upper() in item[9]:
            print("First Thing People Notice About Me: ", item[9])
        if toSearch in item[10] or toSearch.capitalize() in item[10] or toSearch.upper() in item[10]:
            print("Fave books/movies/shows/foods: ", item[10])
        if toSearch in item[11] or toSearch.capitalize() in item[11] or toSearch.upper() in item[11]:
            print("6 Things I Can't Do Without: ", item[11])
        if toSearch in item[12] or toSearch.capitalize() in item[12] or toSearch.upper() in item[12]:
            print("I Spend A Lot of Time Thiking About: ", item[12])
        if toSearch in item[13] or toSearch.capitalize() in item[13] or toSearch.upper() in item[13]:
            print("On a Typical Friday Night I Am: ", item[13])
        if toSearch in item[14] or toSearch.capitalize() in item[14] or toSearch.upper() in item[14]:
            print("A Secret/Confession: ", item[14])
        if toSearch in item[15] or toSearch.capitalize() in item[15] or toSearch.upper() in item[15]:
            print("Message Me If: ", item[15])
    #this is gonna require some more precise formatting I guess :/
    '''
    profile sections:
       (a la our db) [pos in the result thing that prolly isn't a tuple]
       id  [0]
       gender  [1]
       orientation  [2]
       looking for  [3]
       age          [4]
       location     [5]
       self-summary (0) [6]
       what I'm doing with my life (1) [7]
       I'm really good at (2)          [8]
       First thing people notice about you (my deduction) (3) [9]
       Favorite books/movies/shows/food (4)     [10]
       6 things I can't do without (5)          [11]
       I spend a lot of time thinking about (6) [12]
       On a typical Friday night I am (7)       [13]
       A secret/confession (also deduction) (8) [14]
       Message Me If (9)                        [15]
       //stats things we're gonna ignore for rn but could be interesting later
       '''


def main():
    toSearch = ""
    db = OKCdb('profiles.db')
    print("Welcome to the database searcher! Enter '-1' to quit at any time.")
    toSearch = input("Enter a phrase to search the profiles for: ")
    while toSearch != "-1":
        toShow = parseAndQuery(db, toSearch)
        displayResults(toShow, toSearch)
        toSearch = input("Enter a phrase to search the profiles for: ")
    print("Wasn't that fun???? Come back soon!")


if __name__ == "__main__":
    main()
