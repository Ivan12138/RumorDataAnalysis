# encoding:utf-8

import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


# 谣言语料库
def gen_corpus_of_rumor():
    corpus = []
    with open('../weibo_rumor_analysis/file/rumor_weibo_updated.json', 'r') as src:
        lines = src.readlines()
        for line in lines:
            rumor_dict = json.loads(line)
            reported_weibo = rumor_dict['reportedWeibo']
            if isinstance(reported_weibo, dict):
                corpus.append(reported_weibo['weiboContent'])
            else:
                corpus.append('')
    with open('file/corpus_of_rumor.txt', 'w') as out:
        for c in corpus:
            out.write('{}\n'.format(c))


def gen_corpus_of_truth():
    corpus = []
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
        lines = src.readlines()
        for index_e, line in enumerate(lines):
            event_dict = json.loads(line)
            weibos = event_dict['weibo']
            for index_w, weibo in enumerate(weibos):
                if 'content' in weibo.keys():
                    content = weibo['content'].replace('\t', '').replace('\n', '').replace('\r', '')
                    corpus.append('({}, {}) : {}'.format(index_e, index_w, content))
    with open('file/corpus_of_truth.txt', 'w') as out:
        for c in corpus:
            out.write('{}\n'.format(c))


# with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
#     lines = src.readlines()
#     weibo_num = 0
#     for line in lines:
#         event_dict = json.loads(line)
#         weibos = event_dict['weibo']
#         weibo_num += len(weibos)
#     # 158299
#     print(weibo_num)

with open('file/corpus_of_truth.txt', 'r') as src:
    print(len(src.readlines()))
