# encoding:utf-8

import imagehash
from PIL import Image
import json
import time

# from pic_handle.SinglePass import SinglePassCluster
from pic_handle.ClusterUnit import *

img_path = 'sample/'
# weibo_file = '../mongo_script/file/weibo_truth.txt'
weibo_file = '../mongo_script/file/_sample_weibo_truth.txt'


class SinglePassCluster:
    def __init__(self, pic_list, threshold=0.5):
        self.threshold = threshold  # 一趟聚类的阀值
        self.vectors = pic_list

        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后簇的个数
        self.spend_time = t2 - t1

        # TODO: 聚类完成
        self.clusters_centroid_pic = [self.vectors[cluster.centroid] for cluster in self.cluster_list]
        # self.print_result()

    def clustering(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(self.vectors[0])  # 将读入的第一个节点归于该簇

        # TODO: ShowProcess
        # sp = ShowProcess(len(self.vectors))

        # TODO: 第一个节点
        for index in range(1, len(self.vectors)):
            # sp.show_process()

            max_distance = similarity_distance(self.vectors[index],
                                               self.vectors[self.cluster_list[0].centroid])
            max_cluster_index = 0  # 最大相似距离的簇的索引

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

    def print_result(self, label_dict=None):
        """
        print出聚类结果
        :param label_dict: 节点对应的标签字典
        :return:
        """
        print("************ one-pass cluster result ************")
        for index, cluster in enumerate(self.cluster_list):

            print("cluster: %s " % index)  # 簇的序号
            print(cluster.node_list)  # 该簇的节点列表
            if label_dict is not None:
                print(" ".join([label_dict[n] for n in cluster.node_list]))  # 若有提供标签字典，则输出该簇的标签
            print("node num: %s" % cluster.node_num)
            print("----------------")
        print("the number of nodes %s" % len(self.vectors))
        print("the number of cluster %s" % self.cluster_num)
        print("spend time %.9fs" % (self.spend_time / 1000))


# 计算两张图片的 pHash 距离
def similarity_distance(file1, file2, threshold=0.5):
    p_hash1 = imagehash.phash(Image.open(img_path + file1))
    p_hash2 = imagehash.phash(Image.open(img_path + file2))

    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    # print('{}: Similarity between {} and {} is {}.'.format(similarity >= threshold, file1, file2, similarity))

    return similarity


def main():
    start_time = time.time()
    with open(weibo_file, 'r') as src:
        lines = src.readlines()
        sz = len(lines)
        for line in lines:
            event_json = json.loads(line, encoding='utf-8')

            event_id = event_json['id']  # 时间id
            event_weibo_list = event_json['weibo']
            event_pics = []

            # 提取事件中的图片
            for weibo_dict in event_weibo_list:
                if 'piclist' in weibo_dict.keys():
                    curr_pics = weibo_dict['piclist']
                    if curr_pics is not None:
                        for curr_pic in curr_pics:
                            event_pics.append(curr_pic.split('/')[-1])

            event_pics = list(set(event_pics))

            print("\n========================================================")
            print("[{}] 正在对第 {}/{} 行 的事件图片聚类...\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                          lines.index(line) + 1, sz))
            print("图片共有 {} 个，分别为:\n{}\n".format(len(event_pics), event_pics))

            single_pass_cluster = SinglePassCluster(event_pics, threshold=0.5)
            print("\n聚类完成。原有的 {} 张图片过滤后为 {} 张：\n{}\n".format(len(event_pics), single_pass_cluster.cluster_num,
                                                             single_pass_cluster.clusters_centroid_pic))


main()
