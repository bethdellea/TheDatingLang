#Beth fooling aroud while trying to get contexts for phrasings
#April 23/24, 2016 (technically it's the 24th but I haven't gone to sleep yet)

from justDB import OKCdb, NUM_OF_PROFILES
from textblob import TextBlob

# added getProfile_byContains(self, phrase) to OKCdb in parser.py and classificationstation.py
# it should be a big help here

def parseAndQuery(db, toSearch):
    toSearch = "%" + toSearch + "%"
    results = db.getProfile_byContains(toSearch)
    return results

def displayResults(toShow, toSearch):
    '''prints out demographics and the section of their profile the phrase appears in'''
    print("Total profiles containing ", toSearch, ": ", len(toShow))
    wordCount = 0
    for item in toShow:   #group of all profiles returned by db
        for i in range(6, 16):
            sectBlob = TextBlob(item[i])
            wds = sectBlob.words
            for word in wds:
                currWord = str(word)
                if not currWord.isdigit():
                    currWord = currWord.lower()
                if not toSearch.isdigit():
                    toSearch = toSearch.lower()
                if currWord == toSearch:
                    wordCount = wordCount + 1
    print(toSearch, " was used a total of ", wordCount, "times in those profiles.\n")
    sentOrAll = input("Enter 'sentence' to view your input in the sentences where it\
    was used. Enter 'whole' to view the whole section of the profile it was from. ")
    
    toSearch = toSearch.lower()
    if sentOrAll.lower() == 'sentence':
        justSents(toShow, toSearch)
    if sentOrAll.lower() == 'whole':
        wholeSection(toShow, toSearch)
    else:
        print("Sorry, that input was invalid. Please start over. :)")

def justSents(toShow, toSearch):
    '''prints out the searched word as it appears in sentences in the profile, with context
       of section numbers'''
    sectionHeads = ["Self Summary: ", "What I'm Doing With My Life: ", "I'm Really Good At: ",
                    "First Thing People Notice About Me: ", "Fave book/show/movie/food: ",
                    "6 Things I Can't Live Without: ", "I Spend A Lot of Time Thinking About: ",
                    "On a Typical Friday Night I Am: ", "A Secret/Confession: ", "Message Me If: "]
    for item in toShow:
        print("\n\n")
        print("ID #: ", item[0], "\tGender: ", item[1], "\tAge: ", item[4], "\tLocation: ", item[5])
        print("Orientation: ", item[2], "\tLookinng For: ",item[3])
        for i in range(6, 16):
            headPrinted = False
            #each of the profile sections with content
            #header location will be i-6
            sectBlob = TextBlob(item[i])
            sents = sectBlob.sentences
            for sent in sents:
                sentPrinted = False
                words = sent.words
                for word in words:
                    currWord = str(word)
                    if not currWord.isdigit():
                        currWord = currWord.lower()
                    if not toSearch.isdigit():
                        toSearch = toSearch.lower()
                    if currWord == toSearch:
                        if not headPrinted:
                            print(sectionHeads[i-6])
                            headPrinted = True
                        print (sent)
                        break
                

def wholeSection(toShow, toSearch):
    '''prints out the entire profile section where a word occurs, including context'''
    sectionHeads = ["Self Summary: ", "What I'm Doing With My Life: ", "I'm Really Good At: ",
                    "First Thing People Notice About Me: ", "Fave book/show/movie/food: ",
                    "6 Things I Can't Live Without: ", "I Spend A Lot of Time Thinking About: ",
                    "On a Typical Friday Night I Am: ", "A Secret/Confession: ", "Message Me If: "]
    for item in toShow:
        
        print("\n\n")
        print("ID #: ", item[0], "\tGender: ", item[1], "\tAge: ", item[4], "\tLocation: ", item[5])
        print("Orientation: ", item[2], "\tLookinng For: ",item[3])
        for i in range(6, 16):
            #each of the profile sections with content
            #header location will be i-6
            headPrinted = False
            sectBlob = TextBlob(item[i])
            sents = sectBlob.sentences
            wordFound = False
            if wordFound == False: 
                for sent in sents:
                    if wordFound == False: 
                        words = sent.words
                        for word in words:
                            currWord = str(word)
                            if not currWord.isdigit():
                                currWord = currWord.lower()
                            if not toSearch.isdigit():
                                toSearch = toSearch.lower()
                            if currWord == toSearch:
                                wordFound = True
                                if not headPrinted:
                                    print(sectionHeads[i-6])
                                    headPrinted = True
                                    print (item[i])
                                break
                    
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
