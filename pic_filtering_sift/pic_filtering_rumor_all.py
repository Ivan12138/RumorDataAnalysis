# encoding:utf-8

import os
import time
import cv2
from sklearn.externals import joblib
import numpy as np
from scipy.cluster.vq import *
from sklearn import preprocessing
import random

import BoW
import SinglePass

rumor_pics_dir = '../../raw_img_rumor'
rumor_pics_all_file = 'file/pics_rumor_all.txt'


def gen_pics_rumor_all_file():
    with open(rumor_pics_all_file, 'w') as out:
        for root, dirs, files in os.walk(rumor_pics_dir):
            for file in files:
                out.write('{}\n'.format(file))
    with open(rumor_pics_all_file, 'r') as src:
        print('pics_rumor_all sz = {}'.format(len(src.readlines())))


def get_des_list_of_rumor_all():
    with open(rumor_pics_all_file, 'r') as src:
        lines = src.readlines()
    image_paths = [rumor_pics_dir + '/' + line.strip('\n') for line in lines]
    BoW.get_descriptors_list('rumor_all', image_paths)


def get_im_features_of_rumor_all():
    print('==============================================================')
    print('正在计算im_features......')

    des_list, _ = joblib.load('pkl/des_list_{}.pkl'.format('rumor_all'))
    image_paths = [x[0] for x in des_list]

    # Stack all the descriptors vertically in a numpy array
    print('-----------------------------------------')
    print('Start stacking of the descriptors......')

    des_sum = 0
    for image_path, descriptor in des_list:
        des_sum += descriptor.shape[0]
    descriptors = np.zeros((des_sum, 128))

    position = 0
    for image_path, descriptor in des_list:
        sz = len(descriptor)
        descriptors[position:position + sz] = descriptor
        position += sz

    # TODO: 获取rumor_10773的聚类结果
    _, _, _, num_words, voc = joblib.load('pkl/rumor_im_features.pkl')

    # Calculate the histogram of features
    im_features = np.zeros((len(image_paths), num_words), "float32")
    for i in range(len(image_paths)):
        words, distance = vq(des_list[i][1], voc)
        for w in words:
            im_features[i][w] += 1

    # Perform Tf-Idf vectorization
    nbr_occurrences = np.sum((im_features > 0) * 1, axis=0)
    idf = np.array(np.log((1.0 * len(image_paths) + 1) / (1.0 * nbr_occurrences + 1)), 'float32')

    # Perform L2 normalization
    im_features = im_features * idf
    im_features = preprocessing.normalize(im_features, norm='l2')

    print('-----------------------------------------')
    print('正在保存模型参数...')
    joblib.dump((im_features, image_paths, idf, num_words, voc), 'pkl/rumor_all_im_features.pkl', compress=3)


# get_des_list_of_rumor_all()
# get_im_features_of_rumor_all()
# SinglePass.rumor_all()


# TODO：随机选取聚类后，每一簇的图片
def choose_pics_of_cluster():
    out_dir = '../../pics_filtered_img_rumor'

    single_pass_cluster = joblib.load('pkl/rumor_spc_all.pkl')
    _, image_paths, _, _, _ = joblib.load('pkl/rumor_all_im_features.pkl')

    chosen_imgs = []
    for cluster in single_pass_cluster.cluster_list:
        chosen_index = random.sample(cluster.node_list, 1)[0]
        chosen_imgs.append(image_paths[chosen_index])

    # TODO: cp, 注意检查image_paths的图片名
    valid_pics_num = 0
    for img in chosen_imgs:
        code = os.system('cp {} {}'.format(img, out_dir))
        if code == 0:
            valid_pics_num += 1

    print('共有{}个簇，{}张图片复制成功'.format(len(single_pass_cluster.cluster_list), valid_pics_num))


choose_pics_of_cluster()
