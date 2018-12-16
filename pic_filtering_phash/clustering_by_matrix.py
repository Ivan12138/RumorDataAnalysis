# encoding:utf-8

import imagehash
from PIL import Image
import time
import random
from sklearn.externals import joblib


class ClusterUnit:
    def __init__(self):
        self.node_list = []  # 该簇存在的节点列表
        self.node_num = 0  # 该簇节点数
        self.centroid = None  # TODO: 该簇质心的索引，随机指定一张图片

    def add_node(self, node):
        """
        为本簇添加指定节点，并更新簇心
        :param node_vec: 该节点的特征向量
        :param node: 节点
        :return: null
        """
        self.node_list.append(node)
        # try:
        #     self.centroid = random.randint(0, len(self.node_list) - 1)
        # except TypeError:
        #     self.centroid = 0
        self.centroid = random.sample(self.node_list, 1)[0]
        self.node_num += 1  # 节点数加1


class SinglePassCluster:
    def __init__(self, pic_index_list, matrix, threshold=0.75):
        self.threshold = threshold  # 一趟聚类的阀值
        self.vectors = pic_index_list
        self.matrix = matrix

        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后簇的个数
        self.spend_time = t2 - t1

        # 聚类完成
        # self.clusters_centroid_pic = [cluster.node_list[cluster.centroid] for cluster in self.cluster_list]

    def clustering(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(self.vectors[0])  # 将读入的第一个节点归于该簇

        for index in range(1, len(self.vectors)):
            # max_distance = similarity_distance(self.vectors[index],
            #                                    self.vectors[self.cluster_list[0].centroid])
            max_distance = similarity_distance(
                index, self.cluster_list[0].centroid, self.matrix)
            max_cluster_index = 0  # 最大相似距离的簇的索引

            start_time = time.time()
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # 寻找相似距离最大的簇，记录下距离和对应的簇的索引
                # distance = similarity_distance(self.vectors[index],
                #                                self.vectors[cluster.centroid])
                distance = similarity_distance(
                    index, cluster.centroid, self.matrix)

                if distance > max_distance:
                    max_distance = distance
                    max_cluster_index = cluster_index + 1

            if max_distance > self.threshold:  # 最大相似距离大于阀值,则归于该簇
                self.cluster_list[max_cluster_index].add_node(self.vectors[index])

            else:  # 否则新建一个簇
                new_cluster = ClusterUnit()
                new_cluster.add_node(self.vectors[index])
                self.cluster_list.append(new_cluster)
                del new_cluster

            # print process
            if (index + 1) % 500 == 0:
                print('[{}] 第 {}/{} 个vector 处理成功，耗时{:.1f}s，目前共有{}个簇...'.format(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), index + 1,
                    len(self.vectors), time.time() - start_time, len(self.cluster_list)))
                start_time = time.time()


def similarity_distance(i, j, matrix):
    if i == j:
        return 1
    elif i > j:
        temp = i
        i = j
        j = temp
    return matrix[i][j]


def main(sz, matrix, threshold):
    # Main
    print('====================================')
    print('开始聚类，阈值为{}......'.format(threshold))
    print()

    spc = SinglePassCluster([i for i in range(sz)], matrix, threshold=threshold)
    joblib.dump(spc, 'pkl/phash_spc_{}_ts{}.pkl'.format(sz, threshold))
