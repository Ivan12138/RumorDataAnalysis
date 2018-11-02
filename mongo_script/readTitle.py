##coding:utf-8

import pymongo
from pymongo import MongoClient
import time, datetime

import sys

# reload(sys)
sys.setdefaultencoding("utf-8")

client_news = MongoClient('localhost', 27017)
db_news = client_news.NewsCertify

news_article = db_news.tencent_article

# uselessList = []
with open("./alltitle.csv", 'w') as f:
    # for doc in clues_article.find({'clue_score':{'$lt':0.1}},{"articleId":1 , "title":1}):
    #	articleId = doc['articleId']
    # title = doc['title']
    # f.write(articleId + "," + title + "," + "1" + '\n')
    for doc in news_article.find({'isread': {'$ne': False}}):
        articleId = doc['articleId']
        title = doc['title']
    print(articleId)
    # f.write(articleId + "," + title + '\n')
    news_article.update({'articleId': doc['articleId']}, {'$set': {'isread': False}})
