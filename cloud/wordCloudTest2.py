'''
Author: Beth Dellea
Date: Aug 20, 2015 (wayyyy later than I should have started this)
Purpose: building and testing an algorithm for a word cloud program for
        my Capstone Project (to be worked on with the Brilliant Kelly)
'''
import string


#series of functions for handling words of various frequencies, right now just print out stats
def manyWords(hList,num):
    count = len(hList)
    print ("There are ",count,"words used more than ",num," times in the provided text")

def medWords(mList, hnum, lnum):
    count = len(mList)
    print ("There are ",count,"words used more than ", lnum," and less than ",hnum," times.")

def lowWords(lList,num, lNum):
    count = len(lList)
    print ("There are ",count,"words used more than ",lNum," and fewer than ",num," times.")

#function that makes a dictionary of all words provided, keys are words, values are the number of times used in text
def makeDict(wordses):
    wordDict = {}
    for word in wordses:
        if word in wordDict.keys():
            wordDict[word] +=1
        else:
            wordDict[word] = 1
    return wordDict

#takes the dictionary and filters by values for different frequencies
def parseDict(wordDict):

    ks = list(wordDict.keys())
    vl = list(wordDict.values())
    freqList = [] #list of words that occurred beyond the frequent threshold
    medList = [] #list of words for the middle threshold
    shortList = [] #list of words for the too small to matter threshold
    #mostly to make my test prints neater, not for any real focused functional purpose
    hNum = int(input("What is the threshold for frequent words? "))
    mNum = int(input("What is the middle number for frequency? "))
    lNum = int(input("What is the lowest number you care about? ")) 
    for key in wordDict:
        if wordDict[key] > hNum:
            freqList.append(key)
        elif wordDict[key] >= mNum:
            medList.append(key)
        elif wordDict[key] >= lNum and wordDict[key]<=mNum:
            shortList.append(key)
    #print (freqList," are words that occurred more than ten times.")
    #print (medList," are words that occurred between three and ten times")
    #print (shortList, " are words that occurred less than three times.")
    
    manyWords(freqList,hNum)
    medWords(medList,hNum,mNum)
    lowWords(shortList,mNum, lNum)

    skippedWords = len(ks) - len(freqList) - len(medList) - len(shortList)
    print (skippedWords,"total words were skipped for occurring too infrequently.")
#opens files with provided  name, gets all of the words into one list and counts them all
def getFile(name):
    fOpen = open(name+'.txt','r')
    line = fOpen.read()
    words = line.lower()
    for c in string.punctuation:
        words = words.replace(c,"")
    wordList = words.split()
    wordCount = len(wordList)
    fOpen.close()
    print ("There are ",wordCount," total words in the provided text. \nThis will be a bit of work, please be patient.")
    return wordList

#input file name here, manage other functions, etc.
def main():
    fName = input("Please enter the name of the .txt file you would like to analyze: ")
  
    myWords = getFile(fName)
    totWords = len(myWords)
    wordCounts = makeDict(myWords)
    
    parseDict(wordCounts)
    allWords = len(wordCounts)
    print ("In total, there were ",allWords," individual words in the text provided.")

main()
        
