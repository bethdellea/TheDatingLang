#this just reads a pickled list

import pickle
import os

lst = pickle.load(open("users.p", "rb"))
print(lst)
