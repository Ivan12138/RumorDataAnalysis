
from pymongo import MongoClient
import json
from collections import Iterable


def get_unicode_txt():
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

                # count += 1
                # if count == 3:
                #     break


def handle_unicode_txt():
    to_handle_file = 'weibo_truth_unicode.txt'
    output_file = 'weibo_truth.txt'

    with open(to_handle_file, 'r') as src:
        with open(output_file, 'w') as out:
            json_lines = src.readlines()
            for weibo_json in json_lines:
                weibo_dict = json.loads(weibo_json)

                handled_weibo_dict = {}
                for key, value in weibo_dict.items():
                    # 对 keywords 进行处理
                    # if key == 'keywords':
                    #     err_out.write(value + '\n')
                    #     handled_weibo_dict[key] = value

                    # 对于微博集合来说，每一个value都是一个dict
                    if key == 'weibo':
                        for single_weibo in value:
                            for k, v in single_weibo.items():
                                print(k)
                                print(type(v))
                                print()
                            break

                out.write(json.dumps(handled_weibo_dict))
                break


get_unicode_txt()
# handle_unicode_txt()
