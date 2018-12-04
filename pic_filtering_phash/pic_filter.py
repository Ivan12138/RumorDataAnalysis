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
        try:
            # self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)  # 更新簇心
            self.centroid = random.randint(0, len(self.node_list) - 1)
        except TypeError:
            # self.centroid = np.array(node_vec) * 1.  # 初始化质心
            self.centroid = 0
        self.node_num += 1  # 节点数加1


class SinglePassCluster:
    def __init__(self, pic_list, threshold=0.75):
        self.threshold = threshold  # 一趟聚类的阀值
        self.vectors = pic_list
        # self.id = event_id

        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后簇的个数
        self.spend_time = t2 - t1

        # TODO: 聚类完成
        self.clusters_centroid_pic = [cluster.node_list[cluster.centroid] for cluster in self.cluster_list]
        # self.cp_img_on_server()

    def clustering(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(self.vectors[0])  # 将读入的第一个节点归于该簇

        for index in range(1, len(self.vectors)):
            max_distance = similarity_distance(self.vectors[index],
                                               self.vectors[self.cluster_list[0].centroid])
            max_cluster_index = 0  # 最大相似距离的簇的索引

            start_time = time.time()
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # 寻找相似距离最大的簇，记录下距离和对应的簇的索引
                distance = similarity_distance(self.vectors[index],
                                               self.vectors[cluster.centroid])

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
            if index % 50 == 0:
                print('[{}] 第 {}/{} 个vector 处理成功，耗时{:.1f}s，目前共有{}个簇...'.format(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), index, len(self.vectors),
                    time.time() - start_time, len(self.cluster_list)))
                start_time = time.time()


# 计算两张图片的 pHash 距离
def similarity_distance(file1, file2):
    p_hash1 = imagehash.phash(Image.open(file1))
    p_hash2 = imagehash.phash(Image.open(file2))

    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    return similarity


rumor_pics_dir = '../../pics_filtered_img_rumor_todo'
pics_txt = '../pic_filtering_sift/file/pics_rumor_all_todo.txt'

with open(pics_txt, 'r') as src:
    lines = src.readlines()
image_paths = [rumor_pics_dir + '/' + line.strip('\n') for line in lines]

# Main
print('====================================')
print('开始聚类......')
print()

spc = SinglePassCluster(image_paths)
joblib.dump(spc, 'pkl/phash_spc.pkl')
