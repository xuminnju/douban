#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import csv
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
url = 'https://movie.douban.com/top250'
columns = ('排名','电影名', '电影详情', '电影评分', '评价人数', '点评')
path = '豆瓣电影top250.csv'
if os.path.exists(path):
    os.remove(path)
writer = csv.writer(open(path, 'w', encoding='utf-8', newline=''))
writer.writerow(columns)
def crawler(i,page):
    params = {
        'start': page*25,
        'filter': ''
    }
    req = requests.get(url, params=params, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')
    indexs = soup.select('div.item > div.pic > em ')
    titles = soup.select('div.item > div.info > div.hd > a ')
    bds = soup.select('div.item > div.info > div.bd > p.')
    rates = soup.select('div.item > div.info > div.bd > div.star > span.rating_num')
    peoples = soup.select('div.item > div.info > div.bd > div.star')
    comments = soup.select('div.item > div.info > div.bd > p.quote')

    #由于第212,249电影没有评论，手动给其添加评论null
    if i == 226:
        comments.insert(-1, 'Null')
    if i == 201:
        comments.insert(11,'Null')
    for index,title, bd, rate, people, comment in zip(indexs,titles, bds, rates, peoples, comments):
        index = index.get_text()
        title = ''.join(title.get_text().split())
        bd = ''.join(bd.get_text().strip().split())
        rate = rate.get_text()
        people = re.findall('([0-9]*)人评价', people.get_text())[0]
        try:
            comment = comment.get_text().strip()
        except:
            comment = comment
        writer.writerow((index,title,bd,rate,people,comment))


if __name__ == '__main__':
    i = 1
    for page in range(10):
        crawler(i,page)
        i = i + 25