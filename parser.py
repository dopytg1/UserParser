import requests
import fake_useragent
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

ua = fake_useragent.UserAgent()
headers = {"User-Agent": ua.ie}
USERNAME = str(input("Print username: "))

URL_TEMPLATE_INSTAGRAM = "https://www.instagram.com/{}".format(USERNAME)
URL_TEMPLATE_GITHUB = "https://github.com/{}".format(USERNAME)
URL_TEMPLATE_CAREER_HABR = "https://career.habr.com/{}".format(USERNAME)
URL_TEMPLATE_REDDIT = "https://www.reddit.com/user/{}/".format(USERNAME)
URL_TEMPLATE_PIKABU = "https://pikabu.ru/@{}".format(USERNAME)
URL_TEMPLATE_TIKTOK = "https://tiktok.com/@{}".format(USERNAME)


toSeeIfExist = [
    # use the value of check, to compare it with the title of a page that does not exist
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
    # tik tok is not opening(not giving me the content), so i use for this selenium
    
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    browser = webdriver.Chrome(executable_path="C:\\Users\\tenir\\Desktop\\zeon\\parserPython\\chromedriver\\chromedriver.exe", chrome_options=chrome_options)

    try:
        browser.get(url=each["url"])
        time.sleep(3)
        browser.refresh()
        # taking some time to verify from browser
        time.sleep(2)
        title = browser.title

        # common tiktok title looks like this (username (@user) TikTok | Смотреть свежие видео username в TikTok) 
        # so i can check if page exist like this
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
                # if page doesnt exist in github it gives nothing, this cause indexerror
                # to make it work, using try except
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
    