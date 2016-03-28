__author__ = 'Kelly'

import math
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plot
# this import style WILL ONLY work in pycharm
from scraping.classificationstation import OKCdb, NUM_OF_PROFILES
from scraping.cloudywords import isFemale, isGay, generate_cloud


# edit this to not use comic sans, I GUESS.
FONT_PATH = "comic.ttf"


def generate_tfidf_cloud(tuple_list, maskIn):
    cloud = WordCloud(background_color="white", max_font_size=40, relative_scaling=.5, font_path=FONT_PATH,
                      mask=maskIn, stopwords=None).fit_words(tuple_list)
    plot.figure()
    plot.imshow(cloud)
    plot.axis("off")
    plot.show()


def tf_idf(documents):
    """
    Performs normalized tf-idf scoring of terms in documents. Formatted for processing by wordcloud.
    :param documents: a list of strings
    :return: a list of lists of tuples where the outer list represents a document and the inner list is comprised of
             tuples of the form (term, weighting)
    """

    # create index
    index = {}

    # index will be a dict of lists because sparseness should not be a concern with so few documents
    # key: term; value: list of occurrences corresponding to document
    # e.g. index["the"][0] is the weight for the occurrence of "the" in the first document

    # go through each document and tokenize
    for i in range(len(documents)):
        terms = TextBlob(documents[i]).words

        # check if all of the tokens are already in the dictionary
        for t in terms:
            # This is a great place to do stemming if that's a desired thing.
            t = t.lower()
            # check if the current term is in the dictionary of terms
            if t not in index.keys():
                # add term to dictionary with enough places in the list
                index[t] = [0] * len(documents)
            # and increment
            index[t][i] += 1

    # print(index)

    # figure out weights, w = tf * idf / magnitude
    # DAMPENED tf = 1 + log(<number of occurrences of term>)
    # BORING TF: just the raw term frequency with no dampening. toggle the comments below
    # idf = log(<number of total documents>/<number of documents in which term appears>)
    # magnitude = sqrt( sum of squared raw_w )

    # find magnitude of each document for normalization
    sqrd_mag = [0] * len(documents)
    for term in index.keys():
        # find number of documents in which term appears (i.e. nonzero values in index[term])
        df = 0
        for d in index[term]:
            if d > 0:
                df += 1
        # calculate inverse document frequency
        idf = math.log(len(documents)/df)

        for i in range(len(index[term])):
            # DAMPENED
            tf = math.log1p(index[term][i])
            # BORING tf = index[term][i]
            # unnormalized weight = tf * idf
            raw_w = tf * idf
            # overwrite the actual term frequency with the raw weight
            index[term][i] = raw_w
            # add raw weight squared to running sum of squared weights for the doc. we need normalization later!!
            sqrd_mag[i] += math.pow(raw_w, 2)

    # divide sqrt of summed squared magnitude into every weight for normalization
    for term in index.keys():
        for i in range(len(index[term])):
            index[term][i] /= math.sqrt(sqrd_mag[i])

    # you're almost done but wordcloud.py wants tuples, which are immutable, so it's time to change formats.
    # this will be a list of lists of tuples:
    # first dimension: each list represents a document
    # second dimension: each tuple is a term, weight pair for that document

    tuplist = []
    for i in range(len(documents)):
        doctuplist = []
        for term in index.keys():
            term_tuple = term, index[term][i]
            doctuplist.append(term_tuple)
        tuplist.append(doctuplist)

    return tuplist


def tfidf_gender(db):
    female_text = ""
    male_text = ""
    nb_text = ""
    for i in range(1, NUM_OF_PROFILES+1):
        # there is an errant frenchman
        if i == 1467:
            continue
        tiptup = db.getText_byID(i)
        if tiptup is not None:
            if isFemale(i, db):
                female_text += '\r'.join(tiptup)
            elif isFemale(i, db) is None:
                nb_text += '\r'.join(tiptup)
            else:
                male_text += '\r'.join(tiptup)
    corpus = [female_text, male_text, nb_text]
    tuple_lists = tf_idf(corpus)
    for i in range(len(tuple_lists)):
        # print(tuple_list)
        generate_tfidf_cloud(tuple_lists[i], None)


def tfidf_lookingfor(db):
    women_text = ""
    men_text = ""
    everyone_text = ""
    for i in range(1, NUM_OF_PROFILES+1):
        # there is an errant frenchman
        if i == 1467:
            continue
        tiptup = db.getText_byID(i)
        if tiptup is not None:
            if db.getLookingFor_byID(i)[0] == " Women ":
                women_text += '\r'.join(tiptup)
            elif db.getLookingFor_byID(i)[0] == " Men ":
                men_text += '\r'.join(tiptup)
            elif db.getLookingFor_byID(i)[0] == " Everyone ":
                everyone_text += '\r'.join(tiptup)
    corpus = [women_text, men_text, everyone_text]
    tuple_lists = tf_idf(corpus)
    for i in range(len(tuple_lists)):
        # print(tuple_list)
        generate_tfidf_cloud(tuple_lists[i], None)


def tfidf_orientation(db):
    gay_text = ""
    straight_text = ""
    for i in range(1, NUM_OF_PROFILES+1):
        # there is an errant frenchman
        if i == 1467:
            continue
        tiptup = db.getText_byID(i)
        if tiptup is not None:
            if isGay(i, db):
                gay_text += '\r'.join(tiptup)
            else:
                straight_text += '\r'.join(tiptup)
    corpus = [gay_text, straight_text]
    tuple_lists = tf_idf(corpus)
    for i in range(len(tuple_lists)):
        # print(tuple_list)
        generate_tfidf_cloud(tuple_lists[i], None)


def main():
    db = OKCdb("profiles.db")
    tfidf_lookingfor(db)
    tfidf_gender(db)
    tfidf_orientation(db)


if __name__ == "__main__":
    main()
