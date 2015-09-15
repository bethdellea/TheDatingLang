"""
Dellea-Sadwin Senior Project
Contains the barebones functionality to scrape and print desired
data from one OkCupid user profile (already downloaded and stored
in file "beth.txt" to avoid repeatedly downloading a page during
testing)
"""


from bs4 import BeautifulSoup


beth = open("beth.txt", "r")

bethtxt = beth.read()

bethsoup = BeautifulSoup(bethtxt)

print("Beth's gender: ", end="")
gendertag = bethsoup.find("span", "ajax_gender")
gendertag = str(gendertag)
gendersoup = BeautifulSoup(gendertag)
gender = gendersoup.get_text()
print(gender)

print("Beth's orientation: ", end="")
orientag = bethsoup.find(id="ajax_orientation")
orientag = str(orientag)
orientsoup = BeautifulSoup(orientag)
orientation = orientsoup.get_text()
print(orientation)


profile = ""
for i in range(10):
    tid = "essay_text_"+str(i)
    a = bethsoup.find(id=tid)
    if a is not None:
        aboutsoup = BeautifulSoup(str(a))
        profile += aboutsoup.get_text()+"\n"

print(profile)

