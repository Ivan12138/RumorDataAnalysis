# encoding:utf-8

import numpy as np
import random


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
        try:
            # self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)  # 更新簇心
            self.centroid = random.randint(0, len(self.node_list) - 1)
        except TypeError:
            # self.centroid = np.array(node_vec) * 1.  # 初始化质心
            self.centroid = 0
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
