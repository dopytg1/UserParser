import requests
import fake_useragent
import json
from bs4 import BeautifulSoup as bs

ua = fake_useragent.UserAgent()
headers = {"User-Agent": ua.ie}
USERNAME = str(input("Print username: "))


toSeeIfExist = [
    {"site": "instagram", "url": "https://www.instagram.com/{}".format(USERNAME), "check": "<title>Instagram</title>"},
    {"site": "github", "url": "https://github.com/{}".format(USERNAME), "check": ""},
    {"site": "careerHabr", "url": "https://career.habr.com/{}".format(USERNAME), "check": "<title>Хабр Карьера - ошибка 404</title>"},
    {"site": "reddit", "url": "https://www.reddit.com/user/{}/".format(USERNAME), "check": "<title>reddit.com: page not found</title>"},
    {"site": "pikabu", "url": "https://pikabu.ru/@{}".format(USERNAME), "check": "<title>404. Страница не найдена</title>"}
]
links = {USERNAME: []}


def main():
    for each in toSeeIfExist:
        result = requests.get(each['url'], headers=headers).text
        soup = bs(result, "html.parser")
        a = soup.find_all('title')
        try:
            if str(a[0]) != each["check"]:
                links[USERNAME].append(each["url"])
        except IndexError:
            pass
        except Exception as ex:
            print(ex)
    return links[USERNAME]
            

if __name__ == "__main__":
    answer = main()
    data = json.load(open("./links.json"))
    data = {data} if type(data) != dict else data
    data[USERNAME] = answer
    with open('links.json', 'w') as outfile:
        json.dump(data, outfile, 
                        indent=4,  
                        separators=(',',': '))
    