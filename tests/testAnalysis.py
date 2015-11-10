from textblob import *

#opens files with provided  name, gets all of the words into one list and counts them all
def getFile(name):
    fOpen = open(name+'.txt','r')
    words = fOpen.read()
    return words

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

#input file name here, manage other functions, etc.
def main():
    myWords = '''
Space: the final fronteir. These are the voyages of the Starship Enterprise. Its five year mission: to explore strange new worlds, to seek out new life and new civilizations, to boldly go where no man has gone before.
'''

    #things we said we'd test:
    #   - pronoun use (esp message if) [[IN PROGRESS (AND IN QUESTION)]]
    #   - adj/adv use [[DONE]]
    #   - tense used?
    #   - avg length/section and overall
    #   - word count [[DONE]]
    #   - num unique words --> textblob has a make dict fcn to use!!!!!
    #   - length of sentences [[DONE]]
    #   - introspective/emotion and filler words
    #       - "sounding less direct" (wrt disocurse markers)
    #       - introspective words
    #       - emotion words
    #       - koalafiers (probably goes along with sounding less direct)
    #       - on that note, absolute phrasings
    #       - intensifiers
    #   - action words?
    #   - passive vs active voice
    #   - sentiment analysis (polarity and subjectivity)
    blob = TextBlob(myWords)
    if(blob.detect_language()== "en"):
        
        blobList = blob.words
        wordct = len(blobList)
        print ("there are ",wordct," total words in this sample.")
        print ("thanks for making me do all this work.")
        avgWLen = avgWordLen(blobList)
        print("the average length of a word in this sample is ", avgWLen)

        blobSent = blob.sentences
        aSentLen = avgSentLen(blobSent)
        print("the average length of a sentence in this sample is ", aSentLen, " words")
        w = Word("cats")
        w = w.lemmatize()
        print(w)
    else:
        print("this blob was not in English. NOT COOL.")

main()
        

