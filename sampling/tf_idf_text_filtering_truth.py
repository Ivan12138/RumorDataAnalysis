import json
import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np
import random

import TfIdf_SinglePass


def gen_filtered_truth():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_{}_clustering.pkl'.format('truth_4000'))
    cluster_list = single_pass_cluster.cluster_list

    out = open('file/weibo_truth_text_filtered.json', 'w', encoding='utf-8')
    out_pretty = open('file/weibo_truth_text_filtered_pretty.json', 'w', encoding='utf-8')
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r', encoding='utf-8') as src:
        events = src.readlines()

    valid_cluster_num = 0
    missing_pics_cluster_num = 0
    with open('file/corpus/corpus_of_truth.txt', 'r', encoding='utf-8') as corpus:
        lines = corpus.readlines()

        for cluster in cluster_list:
            truth_weibos = []

            for index in cluster.node_list:
                line = lines[index]
                event_index = int(line.split(',')[0][1:])
                weibo_index = int(line.split(',')[1].split(')')[0][1:])

                event = json.loads(events[event_index], encoding='utf-8')
                truth_weibo = event['weibo'][weibo_index]

                if 'piclist' in truth_weibo.keys() and isinstance(truth_weibo['piclist'], list):
                    if len(truth_weibo['piclist']) != 0:
                        # 添加_position字段
                        truth_weibo['_position'] = (event_index, weibo_index)
                        truth_weibos.append(truth_weibo)

            # 选取规则：在有图片的微博中随机取
            if len(truth_weibos) <= 0:
                missing_pics_cluster_num += 1
                continue
            valid_cluster_num += 1
            chosen_truth = random.sample(truth_weibos, 1)[0]

            out.write('{}\n'.format(json.dumps(chosen_truth, ensure_ascii=False)))
            out_pretty.write(
                '{}\n'.format(json.dumps(chosen_truth, ensure_ascii=False, indent=4, separators=(',', ':'))))
            out.flush()
            out_pretty.flush()
    out.close()
    out_pretty.close()

    print('有效的簇为{}个，缺少图片的簇为{}个'.format(valid_cluster_num, missing_pics_cluster_num))


def show_clustering_truth():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_{}_clustering.pkl'.format('rumor_4000'))
    cluster_list = single_pass_cluster.cluster_list

    # 输出过滤后的文本内容
    with open('file/corpus/corpus_of_truth.txt', 'r', encoding='utf-8') as src:
        with open('file/truth_4000.txt', 'w', encoding='utf-8') as out:
            lines = src.readlines()
            for cluster in cluster_list:
                for i in cluster.node_list:
                    out.write('{}'.format(lines[i]))
                out.write('-----------------------------------\n')
                out.flush()

    # 统计微博数量、图片数量、userCertify分布
    with open('file/weibo_truth_text_filtered.json', 'r', encoding='utf-8') as src:
        lines = src.readlines()
        filtered_weibo_num = len(lines)
        filtered_pic_num = 0
        certify_0 = 0
        certify_1 = 0
        certify_2 = 0

        for line in lines:
            truth = json.loads(line, encoding='utf-8-sig')
            filtered_pic_num += len(truth['piclist'])
            if 'userCertify' in truth.keys():
                certify = truth['userCertify']
                if certify == 0:
                    certify_0 += 1
                elif certify == 1:
                    certify_1 += 1
                else:
                    certify_2 += 1

        print('聚类后的真实微博：数量为{}，图片数量为{}'.format(filtered_weibo_num, filtered_pic_num))
        print('（{}）{}:{}:{} = {:.1f} : 1 : {:.1f}'.format(
            certify_0 + certify_1 + certify_2, certify_0, certify_1,
            certify_2, certify_0 / certify_1, certify_2 / certify_1))


# 把15.8w的数据分成4份，分别聚类
def clustering_truth(threshold=0.6):
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_{}.pkl'.format('truth_4000'))
    tf_idf_array = preprocessing.normalize(tf_idf.toarray(), norm='l2')

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array[:40000], t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format('truth_1'))

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array[40000:80000], t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format('truth_2'))

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array[80000:120000], t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format('truth_3'))

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array[120000:], t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format('truth_4'))


clustering_truth()
