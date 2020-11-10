import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# https://riac34.ru/

client = MongoClient()
db = client.news_parser
news_coll = db.news

def getHtml(url):
    r = requests.get(url)
    return r.text

def getNews(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.findAll('div', class_='new-block')
    newTexts = ""
    for i in range(len(news)):
        Name = news[i].find('a', class_='caption').text
        Link = 'https://riac34.ru' + news[i].find('div', class_='col-xl-8 col-lg-8 col-md-8 col-sm-12').find('a').get('href')
        Date = news[i].find('span', class_='date').text.replace("Общество", "")
        verify = news_coll.find_one({'Name news': Name})

        if not(str(verify) == 'None'):
            for new in news_coll.find():
                if new['Name news'] == Name:
                    continue
        else:
            soup2 = BeautifulSoup(getHtml(Link), 'lxml')
            blocks = soup2.findAll('div', class_='full-text')
            for k in range(len(blocks)):
                texts = blocks[k].findAll('b')
                for r in range(len(texts)):
                    newTexts += texts[r].text #+ '\n'
            Text = newTexts
            newTexts = ""


            news_doc = {
                "Name news": Name,
                "Date news": Date,
                "Link news": Link,
                "Text news": Text,

            }
            news_coll.insert_one(news_doc)


for i in range(10):
    url = ("https://riac34.ru/news/123568?PAGEN_1=" + str(i))
    getNews(getHtml(url))
    i += 1


#url = "https://riac34.ru/news/"

#getNews(getHtml(url))





