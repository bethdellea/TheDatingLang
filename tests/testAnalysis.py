from textblob import TextBlob

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

#input file name here, manage other functions, etc.
def main():
    myWords = '''
Implementation Assignment: Canvas Artwork

In this assignment you will use JavaScript and the <canvas> element to create a piece of art. You will also write and include a brief (~150 word) rationale for your artistic decisions. 

Static Artwork

Think about the things that inspire and interest you, and create a piece of art using canvas and JavaScript code.

The easy part: Use variables, loops, arrays, canvas methods, and other JavaScript tools to make visual objects.

The hard part: Create a multimedia experience that produces an emotional, cognitive, or aesthetic response in those who view it. Create something beautiful and meaningful. Create art.

Rationale

Write a ~150 word rationale where you dissect and explore the inspiration and ideas that motivated you to create this art. What is your theory of inspiration, and why were you inspired by this? How are your inspiration and ideas reflected in the implementation? How do you hope others will interpret or understand your artwork?

Requirements

'''

    #things we said we'd test:
    #   - pronoun use (esp message if)
    #   - adj/adv use
    #   - tense used?
    #   - avg length/section and overall
    #   - word count
    #   - num unique words
    #   - length of sentences
    #   - introspective/emotion and filler words
    #   - action words?
    #   - passive vs active voice
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
        print("the average length of a sentence in this sample is ", aSentLen)
        
    else:
        print("this blob was not in English. NOT COOL.")

main()
        

