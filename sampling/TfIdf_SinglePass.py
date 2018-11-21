# encoding:utf-8
import numpy as np
import time
import math
from sklearn.externals import joblib


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


class SinglePassCluster:
    def __init__(self, vector_list, t=0.6):
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

    def clustering_by_cosine_similarity(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(0, self.vectors[0])  # 将读入的第一个节点归于该簇
        # TODO: Check
        for index in range(1, len(self.vectors)):
            start_time = time.time()

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
            print('[{}] 第 {}/{} 个vector 处理成功，耗时{:.1f}s，目前共有{}个簇...'.format(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), index, len(self.vectors),
                time.time() - start_time, len(self.cluster_list)))
            # 每处理500个vector，就存储一次中间结果
            # if index % 500 == 0:
            #     joblib.dump(self, 'file/pkl/clustering_rumor/vector_{}.pkl'.format(index))


def cosine_similarity(vec_a, vec_b):
    # vec_a (1, dim)-array
    # vec_b (dim, 1)-array
    return float(vec_a.dot(vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))
