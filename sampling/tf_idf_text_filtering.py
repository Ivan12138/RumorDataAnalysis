# encoding:utf-8

import json
import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np

import TfIdf_SinglePass


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
def get_tf_idf_of_rumor():
    corpus = []
    with open('file/corpus/cut_corpus_of_rumor.txt', 'r') as src:
        lines = src.readlines()
        for line in lines:
            corpus.append(line)
        print('The size of corpus is {}'.format(len(corpus)))

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    vocabulary = vectorizer.get_feature_names()

    joblib.dump((vocabulary, tf_idf), 'file/pkl/tf_idf_of_rumor.pkl')


def get_tf_idf_of_truth():
    pass


# 设置阈值为0.6
def show_threshold_of_rumor():
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_rumor.pkl')
    tf_idf_array = tf_idf.toarray()
    with open('file/corpus/corpus_of_rumor.txt', 'r') as src:
        with open('file/similarity_threshold/tf_idf.txt', 'w') as out:
            lines = src.readlines()
            for i in range(50):
                for j in range(50):
                    if j > i:
                        # vec_a = tf_idf[i].toarray()
                        # vec_b = tf_idf[j].toarray().reshape((vec_a.shape[1], vec_a.shape[0]))
                        # cos = _cosine_similarity(vec_a, vec_b)

                        cos = _cosine_similarity(tf_idf_array[i], tf_idf_array[j])

                        if cos > 0:
                            out.write('{}{}{}\n\n'.format(lines[i], lines[j], cos))


def _cosine_similarity(vec_a, vec_b):
    # vec_a (1, dim)-array
    # vec_b (dim, 1)-array
    return float(vec_a.dot(vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))


def _clustering(category, threshold=0.6):
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_{}.pkl'.format(category))
    tf_idf_array = preprocessing.normalize(tf_idf.toarray(), norm='l2')

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array, t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format(category))


def main_rumor():
    # 153547
    _clustering('rumor')
    # single_pass_cluster = joblib.load('file/pkl/tf_idf_rumor_clustering.pkl')


main_rumor()
