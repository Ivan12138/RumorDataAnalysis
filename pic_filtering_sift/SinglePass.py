# encoding:utf-8

import numpy as np
import time
import math
from sklearn.externals import joblib
import sklearn.metrics.pairwise as pw


class ClusterUnit:
    def __init__(self):
        self.node_list = []  # 该簇存在的节点列表
        self.node_num = 0  # 该簇节点数
        self.centroid = None  # 该簇质心

    def add_node(self, node, node_vec):
        """
        为本簇添加指定节点，并更新簇心
        :param node_vec: 该节点的特征向量
        :param node: 节点（在整个vector_list中的索引）
        :return: null
        """
        # np.append(self.node_list, node)
        # self.node_list += [node]
        self.node_list.append(node)
        try:
            self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)  # 更新簇心
        except TypeError:
            # TODO: Check
            self.centroid = np.array(node_vec) * 1.  # 初始化质心
        self.node_num += 1  # 节点数加1

    def remove_node(self, node):
        """
        移除本簇指定节点
        :param node: 节点
        :return: null
        """
        try:
            self.node_list.remove(node)
            self.node_num -= 1
        except ValueError:
            raise ValueError("%s not in this cluster" % node)  # 该簇本身就不存在该节点，移除失败
        '''更新质心 待完成'''

    def move_node(self, node, another_cluster):
        """
        将本簇中的其中一个节点移至另一个簇
        :param node: 节点
        :param another_cluster: 另一个簇
        :return: null
        """
        self.remove_node(node=node)
        another_cluster.add_node(node=node)
        '''更新质心 待完成'''


class SinglePassCluster:
    def __init__(self, vector_list, t=0.5):
        """
        :param t: float, 一趟聚类的阀值
        :param vector_list: array-like, shape = [samples_size, features_size]
        :return:
        """
        self.threshold = t  # 一趟聚类的阀值
        self.vectors = np.array(vector_list)
        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering_by_cosine_similarity()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后 簇的个数
        self.spend_time = t2 - t1

    def clustering_by_e_distance(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(0, self.vectors[0])  # 将读入的第一个节点归于该簇
        for index in range(len(self.vectors))[1:]:
            min_distance = e_distance(vec_a=self.vectors[0],
                                      vec_b=self.cluster_list[0].centroid)  # 与簇的质心的最小距离
            min_cluster_index = 0  # 最小距离的簇的索引
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # 寻找距离最小的簇，记录下距离和对应的簇的索引
                distance = e_distance(vec_a=self.vectors[index],
                                      vec_b=cluster.centroid)
                if distance < min_distance:
                    min_distance = distance
                    min_cluster_index = cluster_index + 1
            if min_distance < self.threshold:  # 最小距离小于阀值,则归于该簇
                self.cluster_list[min_cluster_index].add_node(index, self.vectors[index])
            else:  # 否则新建一个簇
                new_cluster = ClusterUnit()
                new_cluster.add_node(index, self.vectors[index])
                self.cluster_list.append(new_cluster)
                del new_cluster

    def clustering_by_cosine_similarity(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(0, self.vectors[0])  # 将读入的第一个节点归于该簇
        # TODO: Check
        start_time = time.time()
        for index in range(1, len(self.vectors)):
            max_similarity = cosine_similarity(vec_a=self.vectors[index],
                                               vec_b=self.cluster_list[0].centroid)  # 与簇的质心的最大相似度
            max_cluster_index = 0  # 最大相似度的簇的索引
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # 寻找相似度最大的簇，记录相似度和对应的簇的索引
                similarity = cosine_similarity(vec_a=self.vectors[index],
                                               vec_b=cluster.centroid)
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_cluster_index = cluster_index + 1
            if max_similarity > self.threshold:  # 最大相似度大于阀值,则归于该簇
                self.cluster_list[max_cluster_index].add_node(index, self.vectors[index])
            else:  # 否则新建一个簇
                new_cluster = ClusterUnit()
                new_cluster.add_node(index, self.vectors[index])
                self.cluster_list.append(new_cluster)
                del new_cluster

            # print process
            if index % 50 == 0:
                print('[{}] 第 {}/{} 个vector 处理成功，耗时{:.1f}s，目前共有{}个簇...'.format(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), index, len(self.vectors),
                    time.time() - start_time, len(self.cluster_list)))
                start_time = time.time()


def e_distance(vec_a, vec_b):
    """
    计算向量a与向量b的欧氏距离
    :param vec_a:
    :param vec_b:
    :return: 欧氏距离
    """
    diff = vec_a - vec_b
    return math.sqrt(np.dot(diff, diff))
    # return np.sqrt(np.num(np.square(vec_a - vec_b)))


# 余弦相似度
def cosine_similarity_raw(vec_a, vec_b):
    len_a = 0
    for x in vec_a:
        len_a += x ** 2
    len_a = np.sqrt(len_a)

    len_b = 0
    for x in vec_b:
        len_b += x ** 2
    len_b = np.sqrt(len_b)

    multi = 0
    for i in range(len(vec_a)):
        multi += vec_a[i] * vec_b[i]

    return float(multi / (len_a * len_b))


def cosine_similarity_np(vec_a, vec_b):
    return vec_a.dot(vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def magnitude(vector):
    return math.sqrt(dot_product(vector, vector))


def cosine_similarity_math(vec_a, vec_b):
    return dot_product(vec_a, vec_b) / (magnitude(vec_a) * magnitude(vec_b) + .00000000001)


def cosine_similarity(vec_a, vec_b):
    array = np.array((vec_a, vec_b))
    return pw.cosine_similarity(array)[0][1]


# Rumor_10773 Single-Pass
def rumor_10773():
    im_features, image_paths, idf, num_words, voc = joblib.load('pkl/rumor_im_features.pkl')
    single_pass_cluster = SinglePassCluster(im_features, 0.9)
    joblib.dump(single_pass_cluster, 'pkl/rumor_spc_10773.pkl')


def rumor_all_todo():
    print('==============================================================')
    print('开始进行 SinglePass 聚类......')
    im_features, image_paths, idf, num_words, voc = joblib.load('pkl/rumor_all_todo_im_features.pkl')
    single_pass_cluster = SinglePassCluster(im_features, 0.9)
    joblib.dump(single_pass_cluster, 'pkl/rumor_spc_all_todo.pkl')
