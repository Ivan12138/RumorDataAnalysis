# encoding:utf-8

import json
import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np

import TfIdf_SinglePass


def _cosine_similarity(vec_a, vec_b):
    # vec_a (1, dim)-array
    # vec_b (dim, 1)-array
    return float(vec_a.dot(vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))


# 设置阈值为0.6
def show_threshold_of_rumor():
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_rumor_4000.pkl')
    tf_idf_array = tf_idf.toarray()
    with open('file/corpus/corpus_of_rumor.txt', 'r') as src:
        with open('file/similarity_threshold/tf_idf_4000.txt', 'w') as out:
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


def clustering(category, threshold=0.6):
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_{}.pkl'.format(category))
    tf_idf_array = preprocessing.normalize(tf_idf.toarray(), norm='l2')

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array, t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format(category))


# test on client
def test_on_client():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_rumor_test_clustering.pkl')
    cluster_list = single_pass_cluster.cluster_list
    with open('file/corpus/corpus_of_rumor.txt', 'r') as src:
        with open('test.txt', 'w') as out:
            lines = src.readlines()
            for cluster in cluster_list:
                for i in cluster.node_list:
                    out.write('{}'.format(lines[i]))
                out.write('-----------------------------------\n')


# 查看聚类结果
def show_clustering_rumor():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_{}_clustering.pkl'.format('rumor_4000'))
    cluster_list = single_pass_cluster.cluster_list
    with open('file/corpus/corpus_of_rumor.txt', 'r') as src:
        with open('file/rumor_4000.txt', 'w') as out:
            lines = src.readlines()
            for cluster in cluster_list:
                for i in cluster.node_list:
                    out.write('{}'.format(lines[i]))
                out.write('-----------------------------------\n')


# show_clustering_rumor()


# 生成过滤后的谣言数据集
def gen_filtered_rumor():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_{}_clustering.pkl'.format('rumor_4000'))
    cluster_list = single_pass_cluster.cluster_list

    out = open('file/weibo_rumor_text_filtered.json', 'w')
    out_pretty = open('file/weibo_rumor_text_filtered_pretty.json', 'w')
    with open('../weibo_rumor_analysis/file/rumor_weibo_updated.json', 'r') as src:
        lines = src.readlines()
        for cluster in cluster_list:
            rumor_cluster = []
            for index in cluster.node_list:
                rumor = json.loads(lines[index], encoding='UTF-8-sig')
                # 选取reportedWeibo存在的rumor
                if not isinstance(rumor['reportedWeibo'], dict):
                    continue
                rumor_cluster.append(rumor)

            # 选取规则：（1）pic_num（2）转赞评
            weibos = [r['reportedWeibo'] for r in rumor_cluster]
            rumor_cluster_pics = []
            for weibo in weibos:
                rumor_cluster_pics.append(len(weibo['piclists']))
            rumor_cluster_propagation = []
            for r in rumor_cluster:
                weibo = r['reportedWeibo']
                try:
                    forward = int(weibo['forward'])
                except ValueError:
                    forward = 0
                except KeyError:
                    forward = 0
                try:
                    comment = int(weibo['comment'])
                except ValueError:
                    comment = 0
                except KeyError:
                    comment = 0
                try:
                    praise = int(weibo['praise'])
                except ValueError:
                    praise = 0
                except KeyError:
                    praise = 0
                rumor_cluster_propagation.append(forward + comment + praise)

            chosen_rumor_index = 0
            for i, r in enumerate(rumor_cluster):
                if rumor_cluster_pics[i] > rumor_cluster_pics[chosen_rumor_index]:
                    chosen_rumor_index = i
                elif rumor_cluster_pics[i] == rumor_cluster_pics[chosen_rumor_index]:
                    if rumor_cluster_propagation[i] > rumor_cluster_propagation[chosen_rumor_index]:
                        chosen_rumor_index = i

            # 写文件
            if len(rumor_cluster) != 0:
                chosen_rumor = rumor_cluster[chosen_rumor_index]
                out.write('{}\n'.format(json.dumps(chosen_rumor, ensure_ascii=False)))
                out_pretty.write(
                    '{}\n'.format(json.dumps(chosen_rumor, ensure_ascii=False, indent=4, separators=(':', ','))))
                out.flush()
                out_pretty.flush()

    out.close()
    out_pretty.close()


gen_filtered_rumor()
