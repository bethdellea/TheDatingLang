import re

filename = "match.txt"
f = open(filename, "r")
page = f.read()

items = re.findall('"username" : "\w+",', page)
users = []

for item in items:
    #item has form '"username" : "<USER_NAME>"'
    things = item.split('"')
    user = things[3]
    users.append(user)

users.pop(0)
for i in range(len(users)):
    print(str(i+1)+". "+users[i])
