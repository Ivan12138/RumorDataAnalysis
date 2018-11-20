# encoding:utf-8

import imagehash
from PIL import Image
import json
import time
import cv2
import os
import random
import traceback

use_server = False

# 本地
img_path = 'sample/'
weibo_file = '../mongo_script/file/_sample_weibo_truth.txt'

if use_server is True:
    # 服务器
    img_path = '../img/'
    weibo_file = '../weibo_truth.txt'


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


class SinglePassCluster:
    def __init__(self, event_id, pic_list, threshold=0.5):
        self.threshold = threshold  # 一趟聚类的阀值
        self.vectors = pic_list
        self.id = event_id

        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后簇的个数
        self.spend_time = t2 - t1

        # TODO: 聚类完成
        self.clusters_centroid_pic = [cluster.node_list[cluster.centroid] for cluster in self.cluster_list]
        # self.print_result()
        # self.save_clustering()
        self.cp_img_on_server()

    def clustering(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(self.vectors[0])  # 将读入的第一个节点归于该簇

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
        # print("************ one-pass cluster result ************")
        # for sorted_index, cluster in enumerate(self.cluster_list):
        #
        #     print("cluster: %s " % sorted_index)  # 簇的序号
        #     print(cluster.node_list)  # 该簇的节点列表
        #     if label_dict is not None:
        #         print(" ".join([label_dict[n] for n in cluster.node_list]))  # 若有提供标签字典，则输出该簇的标签
        #     print("node num: %s" % cluster.node_num)
        #     print("----------------")
        print("the number of nodes %s" % len(self.vectors))
        print("the number of cluster %s" % self.cluster_num)
        print("spend time %.9fs" % (self.spend_time / 1000))

    def save_clustering_img(self):
        src_imgs = [cv2.resize(cv2.imread(img_path + pic), (100, 100)) for pic in self.vectors]
        clustered_imgs = [cv2.resize(cv2.imread(img_path + pic), (100, 100)) for pic in
                          self.clusters_centroid_pic]

        # src_merge = np.hstack(src_imgs)
        # clustered_merge = np.hstack(clustered_imgs)
        # cv2.imwrite(self.id + '-src.jpg',src_merge)
        # cv2.imwrite(self.id + '-clustered.jpg', clustered_merge)

        for i in range(len(src_imgs)):
            if i == 0:
                curr_array = src_imgs[0]
                raw = [np.zeros(curr_array.shape) for i in range(5)]
                src_array = np.hstack(raw)
            elif i % 5 == 0:
                pass
            else:
                src_array = np.hstack((src_array, src_imgs[i]))

    def cp_img_on_server(self):
        if use_server is True:
            for pic in self.clusters_centroid_pic:
                os.system('cp ../img/{} ../img_filter/{}'.format(pic, pic))


# 计算两张图片的 pHash 距离
def similarity_distance(file1, file2, threshold=0.5):
    p_hash1 = imagehash.phash(Image.open(img_path + file1))
    p_hash2 = imagehash.phash(Image.open(img_path + file2))

    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    # print('{}: Similarity between {} and {} is {}.'.format(similarity >= threshold, file1, file2, similarity))

    return similarity


def main():
    with open(weibo_file, 'r') as src:
        lines = src.readlines()
        sz = len(lines)
        for line in lines:
            try:
                start_time = time.time()

                event_json = json.loads(line, encoding='utf-8')

                event_id = event_json['id']  # 事件id
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

                print("========================================================")
                print("[{}] 正在对第 {}/{} 行 的事件图片聚类...\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                              lines.index(line) + 1, sz))
                print("图片共有 {} 个:\n{}...\n".format(len(event_pics), event_pics[:20]))

                single_pass_cluster = SinglePassCluster(event_id, event_pics, threshold=0.5)
                print("\n聚类完成。原有的 {} 张图片过滤后为 {} 张：\n{}\n".format(len(event_pics), single_pass_cluster.cluster_num,
                                                                 single_pass_cluster.clusters_centroid_pic))

                print('>>> 耗时: {:.2f}s <<<'.format(time.time() - start_time))

            except:
                traceback.print_exc()
                print('[Error] Something wrong in line:\n{}'.format(event_id))


def test():
    # Test：CV
    imgs = []
    imgs.append(img_path + 'pic1.jpg')
    imgs.append(img_path + 'pic2.jpg')
    imgs.append(img_path + 'pic3.jpg')
    imgs.append(img_path + 'pic4.jpg')
    imgs.append(img_path + 'ppic1.jpg')
    imgs.append(img_path + 'ppic2.jpg')

    # resize to same scale
    im1 = cv2.resize(cv2.imread(imgs[0]), (200, 200))
    im2 = cv2.resize(cv2.imread(imgs[1]), (200, 200))
    hmerge = np.hstack((im1, np.zeros((im1.shape[0], 10, im1.shape[2])), im2))  # 水平拼接
    # vmerge = np.vstack((im1, im2))  # 垂直拼接

    # cv2.imshow("test1", hmerge)
    # cv2.imshow("test2", vmerge)
    cv2.imwrite('test.png', hmerge)

    # print(im1)
    print(type(im1))
    print(type(hmerge))


# print(similarity_distance('62d90090gw1f2p10z5eg6j20dw0jpabu.jpg', '65d9a912gw1f25vy7hgc5j20c60r0n1k.jpg'))

main()

# 71775
