import requests
import fake_useragent
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os

ua = fake_useragent.UserAgent()
headers = {"User-Agent": ua.ie}
USERNAME = str(input("Print username: "))

URL_TEMPLATE_INSTAGRAM = "https://www.instagram.com/{}".format(USERNAME)
URL_TEMPLATE_GITHUB = "https://github.com/{}".format(USERNAME)
URL_TEMPLATE_CAREER_HABR = "https://career.habr.com/{}".format(USERNAME)
URL_TEMPLATE_REDDIT = "https://www.reddit.com/user/{}/".format(USERNAME)
URL_TEMPLATE_PIKABU = "https://pikabu.ru/@{}".format(USERNAME)
URL_TEMPLATE_TIKTOK = "https://tiktok.com/@{}".format(USERNAME)

# selenium web-browser for tiktok
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# set the path for your chrome driver
browser = webdriver.Chrome(executable_path=os.path.abspath("./chromedriver\chromedriver.exe"), chrome_options=chrome_options)

toSeeIfExist = [
    {
        "site": "instagram",
        "url": URL_TEMPLATE_INSTAGRAM,
        "check": "<title>Instagram</title>"
    },
    {
        "site": "github",
        "url": URL_TEMPLATE_GITHUB,
        "check": ""
    },
    {
        "site": "careerHabr",
        "url": URL_TEMPLATE_CAREER_HABR,
        "check": "<title>Хабр Карьера - ошибка 404</title>"
    },
    {
        "site": "reddit",
        "url": URL_TEMPLATE_REDDIT,
        "check": "<title>reddit.com: page not found</title>"
    },
    {
        "site": "pikabu",
        "url": URL_TEMPLATE_PIKABU,
        "check": "<title>404. Страница не найдена</title>"
    },
    {
        "site": "tiktok",
        "url": URL_TEMPLATE_TIKTOK
    },
]

links = {
    USERNAME: []
}


def check_tiktok(each):
    try:
        browser.get(url=each["url"])
        time.sleep(3)
        browser.refresh()
        time.sleep(2)
        title = browser.title

        if USERNAME in title:
            links[USERNAME].append(each["url"])
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


def main():
    for each in toSeeIfExist:
        if each['site'] != "tiktok":
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
        else:
            check_tiktok(each)
    return links[USERNAME]


if __name__ == "__main__":
    answer = main()
    data = json.load(open("./links.json"))
    if type(data) != dict:
        data = {data}

    data[USERNAME] = answer

    with open('links.json', 'w') as outfile:
        json.dump(data, outfile, 
                        indent=4,  
                        separators=(',',': '))
    print(answer)
    