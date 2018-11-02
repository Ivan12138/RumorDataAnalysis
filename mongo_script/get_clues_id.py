# encoding:utf-8

# =========== 根据 MongoDB 生成真实谣言的 clue_id =========== #

# ﻿db.getCollection('newsclues_ready').find({label:"truth", category:{$nin:["军事", "娱乐"]}}).sort({timestamp:-1})
# ﻿db.getCollection('event_ready').find({clue_id:"87b620c2f8aedb60f999f93950c8ac80", update:true})

from pymongo import MongoClient

client_news = MongoClient('localhost', 27017)
db_news = client_news.NewsCertify

clues_article = db_news.newsclues_ready

count = 1
with open("clues_id.txt", 'w') as f:
    for doc in clues_article.find({'label': "truth", 'category': {'$nin': ["军事", "娱乐"]}}):
        clues_id = doc['id']
        f.write(clues_id + '\n')
