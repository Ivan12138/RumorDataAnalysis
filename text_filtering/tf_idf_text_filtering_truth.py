import json
import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np
import random

import TfIdf_SinglePass


# 把15.8w的数据分成4份，分别聚类
def clustering_truth_to_4_fold(threshold=0.6):
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


# 输出每一折聚类的效果
def gen_clustering(num):
    single_pass_cluster = joblib.load('file/pkl/tf_idf_truth_{}_clustering.pkl'.format(num))
    cluster_list = single_pass_cluster.cluster_list

    print('过滤前共有{}条微博，过滤后为{}条。正在写入文件...'.format(40000, len(cluster_list)))
    # 输出过滤后的文本内容
    with open('file/corpus/corpus_of_truth.txt', 'r', encoding='utf-8') as src:
        with open('file/clustering/truth_{}.txt'.format(num), 'w', encoding='utf-8') as out:
            lines = src.readlines()
            for cluster in cluster_list:
                for i in cluster.node_list:
                    out.write('{}'.format(lines[40000 * (num - 1) + i]))
                out.write('-----------------------------------\n')
                out.flush()


# 生成4折过滤后的语料，供再次过滤
def gen_filtered_truth_from_4_fold():
    with open('file/corpus/corpus_of_truth.txt', 'r', encoding='utf-8') as src:
        lines = src.readlines()

    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r', encoding='utf-8') as src:
        events = src.readlines()

    valid_line_sum = 0

    out = open('file/corpus/corpus_of_truth_4_fold.txt', 'w', encoding='utf-8')
    for num in range(1, 5):
        single_pass_cluster = joblib.load('file/pkl/tf_idf_truth_{}_clustering.pkl'.format(num))
        cluster_list = single_pass_cluster.cluster_list

        valid_cluster_num = 0
        missing_pics_cluster_num = 0

        for cluster in cluster_list:
            valid_indexes = []

            for index in cluster.node_list:
                line = lines[index + 40000 * (num - 1)]
                event_index = int(line.split(',')[0][1:])
                weibo_index = int(line.split(',')[1].split(')')[0][1:])

                event = json.loads(events[event_index], encoding='utf-8')
                truth_weibo = event['weibo'][weibo_index]

                if 'piclist' in truth_weibo.keys() and isinstance(truth_weibo['piclist'], list):
                    if len(truth_weibo['piclist']) != 0:
                        valid_indexes.append(index)

            # 选取规则：在有图片的微博中随机取
            if len(valid_indexes) <= 0:
                missing_pics_cluster_num += 1
                continue
            valid_cluster_num += 1
            chosen_index = random.sample(valid_indexes, 1)[0]

            out.write('{}'.format(lines[chosen_index + 40000 * (num - 1)]))
            out.flush()

        valid_line_sum += valid_cluster_num
        print('第{}组 cluster 已处理完成...'.format(num))
        print('有效的簇为{}个，缺少图片的簇为{}个'.format(valid_cluster_num, missing_pics_cluster_num))

    out.close()

    with open('file/corpus/corpus_of_truth_4_fold.txt', 'r', encoding='utf-8') as src:
        print('处理后的语料库长度为:{}（有效的簇个数为：{}）'.format(len(src.readlines()), valid_line_sum))


# 真实语料库-4 fold-得到tf-idf向量
def get_tf_idf_of_truth(features_num=4000):
    corpus = []
    with open('file/corpus/corpus_of_truth_4_fold.txt', 'r', encoding='utf-8') as src:
        lines = src.readlines()
        for line in lines:
            seg_list = jieba.cut(line)
            result = ' '.join(seg_list)
            corpus.append(result)
    with open('file/corpus/cut_corpus_of_truth_4_fold.txt', 'w', encoding='utf-8') as out:
        for c in corpus:
            out.write('{}'.format(c))

    corpus = []
    with open('file/corpus/cut_corpus_of_truth_4_fold.txt', 'r', encoding='utf-8') as src:
        lines = src.readlines()
        for line in lines:
            corpus.append(line)
        print('The size of corpus is {}'.format(len(corpus)))

    vectorizer = CountVectorizer(max_features=features_num)
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    vocabulary = vectorizer.get_feature_names()

    joblib.dump((vocabulary, tf_idf), 'file/pkl/tf_idf_of_truth_{}.pkl'.format('4_fold'))


# 38180 的数据，重新聚类
def clustering_truth_from_4_fold(threshold=0.6):
    _, tf_idf = joblib.load('file/pkl/tf_idf_of_{}.pkl'.format('truth_4_fold'))
    tf_idf_array = preprocessing.normalize(tf_idf.toarray(), norm='l2')

    single_pass_cluster = TfIdf_SinglePass.SinglePassCluster(tf_idf_array, t=threshold)
    joblib.dump(single_pass_cluster, 'file/pkl/tf_idf_{}_clustering.pkl'.format('truth_4_fold'))


# 展示2次聚类的结果
def show_twice_clustering_truth():
    single_pass_cluster = joblib.load('file/pkl/tf_idf_{}_clustering.pkl'.format('truth_4_fold'))
    cluster_list = single_pass_cluster.cluster_list

    # 输出过滤后的文本内容
    with open('file/corpus/corpus_of_truth_4_fold.txt', 'r', encoding='utf-8') as src:
        with open('file/clustering/truth_4_fold.txt', 'w', encoding='utf-8') as out:
            lines = src.readlines()
            for cluster in cluster_list:
                for i in cluster.node_list:
                    out.write('{}'.format(lines[i]))
                out.write('-----------------------------------\n')
                out.flush()

    # 得到最终的json文件
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r', encoding='utf-8') as src:
        events = src.readlines()

    out = open('file/weibo_truth_4_fold_text_filtered.json', 'w')
    out_pretty = open('file/weibo_truth_4_fold_text_filtered_pretty.json', 'w')

    valid_cluster_num = 0
    missing_pics_cluster_num = 0

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
                    truth_weibo['_position'] = (event_index, weibo_index)
                    truth_weibos.append(truth_weibo)

        # 选取规则：在有图片的微博中随机取
        if len(truth_weibos) <= 0:
            missing_pics_cluster_num += 1
            continue
        valid_cluster_num += 1
        chosen_truth = random.sample(truth_weibos, 1)[0]

        out.write('{}\n'.format(json.dumps(chosen_truth, ensure_ascii=False)))
        out.flush()
        out_pretty.write('{}\n'.format(json.dumps(chosen_truth, ensure_ascii=False, indent=4, separators=(',', ':'))))
        out_pretty.flush()

    print('有效的簇为{}个，缺少图片的簇为{}个'.format(valid_cluster_num, missing_pics_cluster_num))

    # 统计微博数量、图片数量、userCertify分布
    with open('file/weibo_truth_4_fold_text_filtered.json', 'r', encoding='utf-8') as src:
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


# 展示1次聚类的结果
def show_once_clustering_truth():
    # 得到最终的json文件
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r', encoding='utf-8') as src:
        events = src.readlines()

    out = open('file/weibo_truth_once_text_filtered.json', 'w')
    out_pretty = open('file/weibo_truth_once_text_filtered_pretty.json', 'w')
    with open('file/corpus/corpus_of_truth_4_fold.txt', 'r') as src:
        lines = src.readlines()
        for line in lines:
            event_index = int(line.split(',')[0][1:])
            weibo_index = int(line.split(',')[1].split(')')[0][1:])

            event = json.loads(events[event_index], encoding='utf-8')
            truth_weibo = event['weibo'][weibo_index]
            truth_weibo['_position'] = (event_index, weibo_index)

            out.write('{}\n'.format(json.dumps(truth_weibo, ensure_ascii=False)))
            out.flush()
            out_pretty.write(
                '{}\n'.format(json.dumps(truth_weibo, ensure_ascii=False, indent=4, separators=(',', ':'))))
            out_pretty.flush()
    out.close()
    out_pretty.close()

    # 统计微博数量、图片数量、userCertify分布
    with open('file/weibo_truth_once_text_filtered.json', 'r', encoding='utf-8') as src:
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

# show_once_clustering_truth()
