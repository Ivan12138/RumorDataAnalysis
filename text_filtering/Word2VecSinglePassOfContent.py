# encoding:utf-8

import numpy as np
import time
import math
import synonyms
import random


class ClusterUnitOfContent:
    def __init__(self):
        self.node_list = []  # 该簇存在的节点列表
        self.node_num = 0  # 该簇节点数
        self.centroid = None  # 该簇质心的索引

    # 计算content相似度时的质心加入方法
    def add_node(self, node):
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
            # TODO: Check
            self.centroid = random.randint(0, len(self.node_list) - 1)  # 更新簇心的索引
        except ValueError:
            self.centroid = 0  # 初始化质心
        self.node_num += 1  # 节点数加1


class SinglePassClusterOfContent:
    def __init__(self, content_list, t=0.8):
        """
        :param t: float, 一趟聚类的阀值
        :param vector_list: array-like, shape = [samples_size, features_size]
        :return:
        """
        self.threshold = t  # 一趟聚类的阀值
        # TODO: Check
        self.vectors = content_list
        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        # To modify the metrics of clustering
        self.clustering_by_content_similarity()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后 簇的个数
        self.spend_time = t2 - t1

    def clustering_by_content_similarity(self):
        self.cluster_list.append(ClusterUnitOfContent())  # 初始新建一个簇
        self.cluster_list[0].add_node(0)  # 将读入的第一个节点归于该簇
        # TODO: Check
        for index in range(1, len(self.vectors)):
            max_similarity = content_similarity(self.vectors[index],
                                                self.vectors[self.cluster_list[0].centroid])  # 与簇的质心的最大相似度
            max_cluster_index = 0  # 最大相似度的簇的索引
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # 寻找相似度最大的簇，记录相似度和对应的簇的索引
                similarity = content_similarity(self.vectors[index],
                                                self.vectors[cluster.centroid])
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_cluster_index = cluster_index + 1
            if max_similarity > self.threshold:  # 最大相似度大于阀值,则归于该簇
                self.cluster_list[max_cluster_index].add_node(index)
            else:  # 否则新建一个簇
                new_cluster = ClusterUnitOfContent()
                new_cluster.add_node(index)
                self.cluster_list.append(new_cluster)
                del new_cluster


def content_similarity(content_a, content_b):
    return synonyms.compare(content_a, content_b)
