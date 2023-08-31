from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time

# Проверяю ссылки, которые даны в документе:

list_pages = ["https://www.kia.ru/press/magazine/j33/", "https://www.kia.ru/press/magazine/j35/", "https://www.kia.ru/press/magazine/j21/", "https://www.kia.ru/press/magazine/j18/", "https://www.kia.ru/press/magazine/j10/", "https://www.kia.ru/press/magazine/j38/", "https://www.kia.ru/press/magazine/j43/", "https://www.kia.ru/press/magazine/j42/", "https://www.kia.ru/press/magazine/j44/", "https://www.kia.ru/press/magazine/j33/", "https://www.kia.ru/press/tips/27/", "https://www.kia.ru/press/tips/26/", "https://www.kia.ru/press/tips/24/", "https://www.kia.ru/press/tips/20/", "https://www.kia.ru/press/tips/16/", "https://www.kia.ru/press/tips/15/"]
invalid_links = []

for i in list_pages:
    ua = UserAgent().random
    HEADERS = {"user-agent": ua, "accept": "*/*"}
    response = requests.get(url=i, headers=HEADERS)
    if response.status_code == 200:
        pass
    else:
        invalid_links.append(i)

print(f"Количество недействительных ссылок: {len(invalid_links)} из {len(list_pages)}")
if len(invalid_links) > 0:
    [print(i) for i in invalid_links]


# ВАРИАНТ 1: беру список страниц новостей/статей только из гугловского файла
# https://docs.google.com/spreadsheets/d/1btiLDeliT87fFw4yI4aFMEthwL0GtUFMKAgGDW6ryOk/edit#gid=545765203

list_pages = ["https://www.kia.ru/press/magazine/j33/", "https://www.kia.ru/press/magazine/j35/", "https://www.kia.ru/press/magazine/j21/", "https://www.kia.ru/press/magazine/j18/", "https://www.kia.ru/press/magazine/j10/", "https://www.kia.ru/press/magazine/j38/", "https://www.kia.ru/press/magazine/j43/", "https://www.kia.ru/press/magazine/j42/", "https://www.kia.ru/press/magazine/j44/", "https://www.kia.ru/press/magazine/j33/", "https://www.kia.ru/press/tips/27/", "https://www.kia.ru/press/tips/26/", "https://www.kia.ru/press/tips/24/", "https://www.kia.ru/press/tips/20/", "https://www.kia.ru/press/tips/16/", "https://www.kia.ru/press/tips/15/"]
invalid_links = []

with open("press.txt", "w", encoding="utf-8") as file:
    pass

for i in list_pages:
    try:
        ua = UserAgent().random
        HEADERS = {"user-agent": ua, "accept": "*/*"}
        response = requests.get(url=i, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            head_press = soup.h1.text.strip() #заголовок статьи
            all_img_list, all_img = [], ""
            [all_img_list.append(img.find("img").attrs.get("src")) for img in soup.find_all("div", class_="articles-detail__content__offset")] #все фото из статьи
            for img in all_img_list:
                all_img += img + ","

            try:
              date_press = soup.select_one("div.articles-detail__date").text.strip()  # дата статьи
              for val in soup.find_all("div", class_="g-container"):
                for child in val.children:
                  if date_press in child.text:
                    with open("press.txt", "a", encoding="utf-8") as file:
                      file.write(f"<{head_press}>\n")
                      file.write(child.text.strip().replace("\xa0", " "))
                      file.write(f"\n\nФотографии из статьи: {all_img[:-1]}")

            except:
              for val in soup.find_all("div", class_="g-container"):
                for child in val.children:
                  if child.find("h1") is not None and child.find("h1") != -1:
                    with open("press.txt", "a", encoding="utf-8") as file:
                      file.write(f"<{head_press}>\n")
                      file.write(child.text.replace("\xa0", " "))
                      file.write(f"\n\nФотографии из статьи: {all_img[:-1]}\n\n")
        time.sleep(5)

    except ConnectionError:
        print("Проверьте подключение к сети")

# ВАРИАНТ 2: парсинг со страницы https://www.kia.ru/press/magazine/ статей и новостей (новости можно свежие только наверное?)

with open("press.txt", "w", encoding="utf-8") as file_press:
    pass

url = "https://www.kia.ru/press/magazine/"

ua = UserAgent().random
HEADERS = {"user-agent": ua, "accept": "*/*"}

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    all_article_list = []
    [all_article_list.append("https://www.kia.ru" + val.find("a").attrs.get("href")) for val in soup.find_all("article", class_="article-preview")]

    for i in all_article_list:
        try:
            response = requests.get(url=i, headers=HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                head_press = soup.h1.text.strip() #заголовок статьи
                all_img_list, all_img = [], ""
                [all_img_list.append(img.find("img").attrs.get("src")) for img in soup.find_all("div", class_="articles-detail__content__offset")]  # все фото из статьи
                for img in all_img_list:
                    all_img += img + ","

                try:
                    date_press = soup.select_one("div.articles-detail__date").text.strip()  # дата статьи
                    for val in soup.find_all("div", class_="g-container"):
                        for child in val.children:
                            if date_press in child.text:
                                with open("press.txt", "a", encoding="utf-8") as file:
                                    file.write(f"<{head_press}>\n")
                                    file.write(child.text.strip().replace("\xa0", " "))
                                    file.write(f"\n\nФотографии из статьи: {all_img[:-1]}\n\n")
                except:
                    for val in soup.find_all("div", class_="g-container"):
                        for child in val.children:
                            if child.find("h1") is not None and child.find("h1") != -1:
                                with open("press.txt", "a", encoding="utf-8") as file:
                                    file.write(f"<{head_press}>\n")
                                    file.write(child.text.replace("\xa0", " "))
                                    file.write(f"\nФотографии из статьи: {all_img[:-1]}\n\n")
            time.sleep(5)
        except ConnectionError:
            print("Проверьте подключение к сети")

with open("news.txt", "w", encoding="utf-8") as file_news:
    pass

url = "https://www.kia.ru/press/news/"

ua = UserAgent().random
HEADERS = {"user-agent": ua, "accept": "*/*"}

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    all_article_list = []
    [all_article_list.append("https://www.kia.ru" + val.find("a").attrs.get("href")) for val in soup.find_all("article", class_="article-preview")]

    for i in all_article_list:
        try:
            response = requests.get(url=i, headers=HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                head_press = soup.h1.text.strip() #заголовок статьи
                all_img_list, all_img = [], ""
                [all_img_list.append(img.find("img").attrs.get("src")) for img in soup.find_all("div", class_="articles-detail__content__offset")]  # все фото из статьи
                for img in all_img_list:
                    all_img += img + ","

                try:
                    date_press = soup.select_one("div.articles-detail__date").text.strip()  # дата статьи
                    for val in soup.find_all("div", class_="g-container"):
                        for child in val.children:
                            if date_press in child.text:
                                with open("news.txt", "a", encoding="utf-8") as file:
                                    file.write(f"<{head_press}>\n")
                                    file.write(child.text.strip().replace("\xa0", " "))
                                    file.write(f"\n\nФотографии из статьи: {all_img[:-1]}\n\n")
                except:
                    for val in soup.find_all("div", class_="g-container"):
                        for child in val.children:
                            if child.find("h1") is not None and child.find("h1") != -1:
                                with open("news.txt", "a", encoding="utf-8") as file:
                                    file.write(f"<{head_press}>\n")
                                    file.write(child.text.replace("\xa0", " "))
                                    file.write(f"\nФотографии из статьи: {all_img[:-1]}\n\n")
            time.sleep(5)
        except ConnectionError:
            print("Проверьте подключение к сети")
