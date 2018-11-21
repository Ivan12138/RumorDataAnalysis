# encoding:utf-8

import json
import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.externals import joblib


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
                corpus.append('[Error] ' + str(reported_weibo))
    with open('file/corpus/corpus_of_rumor.txt', 'w') as out:
        for c in corpus:
            out.write('{}\n'.format(c))


# 真实微博语料库
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
    with open('file/corpus/corpus_of_truth.txt', 'w') as out:
        for c in corpus:
            out.write('{}\n'.format(c))


# 谣言语料库-分词
def cut_words_of_rumor():
    corpus = []
    with open('file/corpus/corpus_of_rumor.txt', 'r') as src:
        lines = src.readlines()
        for line in lines:
            seg_list = jieba.cut(line)
            result = ' '.join(seg_list)
            corpus.append(result)
    with open('file/corpus/cut_corpus_of_rumor.txt', 'w') as out:
        for c in corpus:
            out.write('{}'.format(c))


def cut_words_of_truth():
    pass


# 谣言语料库-得到tf-idf向量
def get_tf_idf_of_rumor(features_num=4000):
    corpus = []
    with open('file/corpus/cut_corpus_of_rumor.txt', 'r') as src:
        lines = src.readlines()
        for line in lines:
            corpus.append(line)
        print('The size of corpus is {}'.format(len(corpus)))

    vectorizer = CountVectorizer(max_features=features_num)
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    vocabulary = vectorizer.get_feature_names()

    joblib.dump((vocabulary, tf_idf), 'file/pkl/tf_idf_of_rumor_{}.pkl'.format(features_num))


def get_tf_idf_of_truth():
    pass
