import json


with open("./links.json") as fp:
    listObj = json.load(fp)
    print(listObj)