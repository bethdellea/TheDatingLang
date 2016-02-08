"""
Clustering documents instead of classifying them?
See brandonrose.org/clustering for possibly relevant example of TfidfVectorizer
See http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting for documentation
TfidfVectorizer takes a corpus parameter as a list of texts.
"""


from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from .parser import OKCdb


NUM_OF_PROFILES = 2


def tokenize(text):
    blob = TextBlob(text)
    if(len(myWords) < 3 or blob.detect_language() != "en"):
        return None
    tokens = blob.words
    # stemmed_tokens = textblob.packages.nltk.stem idk wowejfkdwnoskfnws
    return tokens
    
# NEED get_text_from_profile()    
def create_token_dict():
    token_dict = {}
    for i in range(NUM_OF_PROFILES):
        text = get_text_from_profile(i)
        tokens = tokenize(text)
        if tokens is None:
            continue
        for t in tokens:
            if t in token_dict.keys():
                token_dict[t] += 1
            else:
                token_dict[t] = 1
    return token_dict

# NEED get_text_from_profile() 
def create_corpus():
    corpus = [tokenize(get_text_from_profile(i)) for i in range(NUM_OF_PROFILES)]
    return corpus


def main():
    db = OKCdb('profiles.db')
    print(db)
    # tfidfer = TfidfVectorizer()

# stopwords = nltk.corpus.stopwords.words('english')


main()
