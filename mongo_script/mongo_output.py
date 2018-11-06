# encoding:utf-8

# ========== 根据 clue_id 生成对应 weibo 的json 文件 ========== #

import json


def get_unicode_txt_from_mongo():
    from pymongo import MongoClient

    client_news = MongoClient('localhost', 27017)
    db_news = client_news.NewsCertify
    event_article = db_news.event_ready

    count = 0
    with open('clues_id.txt', 'r') as src:
        with open('weibo_truth_unicode.txt', 'w') as out:
            id_list = src.readlines()
            for clue_id in id_list:
                clue_id = clue_id.split()[0]
                doc = event_article.find_one({'clue_id': clue_id, 'update': True})

                doc.pop('_id')
                doc_json = json.dumps(doc, encoding="UTF-8")
                # doc_json = json.dumps(doc, encoding="UTF-8", indent=4)

                out.write(doc_json + '\n')


def handle_unicode_txt_to_pretty():
    file = 'weibo_truth_unicode.txt'
    with open(file, 'r') as src:
        with open('weibo_truth_pretty.txt', 'w') as out:
            lines = src.readlines()
            for line in lines:
                weibo_json = json.loads(line)
                out.write(json.dumps(weibo_json, ensure_ascii=False, indent=4, separators=(',', ':')))


# get_unicode_txt_from_mongo()
# handle_unicode_txt_to_pretty()

def handle_unicode_txt():
    file = 'weibo_truth_unicode.txt'
    with open(file, 'r') as src:
        with open('weibo_truth.txt', 'w') as out:
            lines = src.readlines()
            for line in lines:
                weibo_json = json.loads(line)
                out.write(json.dumps(weibo_json, ensure_ascii=False))
                out.write('\n')


handle_unicode_txt()
