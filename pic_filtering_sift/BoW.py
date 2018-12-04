# encoding:utf-8

import cv2
import numpy as np
from sklearn.externals import joblib
from scipy.cluster.vq import *
import time

from sklearn import preprocessing


# 词袋模型：导入图片，最终生成单词本
def get_descriptors_list(category, image_paths):
    start_time = time.time()
    print('==============================================================')
    print('Extracting SIFT of {} imgs......'.format(len(image_paths)))

    # Create feature extraction and key points detector objects
    sift = cv2.xfeatures2d.SIFT_create()

    # List where all the descriptors are stored
    des_list = []

    removed_num = 0
    for i, image_path in enumerate(image_paths):
        im = cv2.imread(image_path)
        if im is None:
            removed_num += 1
            print('Remove the {}th pics'.format(i))
            continue
        _, des = sift.detectAndCompute(im, None)
        if des is not None:
            des_list.append((image_path, des))

        if i % 50 == 0:
            print("Extract SIFT {} of {} images, it took {:.1f}s".format(i, len(image_paths), time.time() - start_time))
            start_time = time.time()

    # TODO: 存储des_list，有可能很大
    joblib.dump((des_list, image_paths), 'pkl/des_list_{}.pkl'.format(category))

    print('--------------------------------')
    print('[{:.1f}s] Has Extracted All imgs! The len of image_paths is {}, removed {} imgs.'.format(
        time.time() - start_time, len(image_paths), removed_num))
    print('--------------------------------')


def get_im_features(category, pkl_path, num_words=1000):
    des_list, _ = joblib.load('pkl/des_list_{}.pkl'.format(category))

    # 在修改完上面的代码以后，就不用去除 descriptor空值
    # for image_path, descriptor in des_list:
    #     if descriptor is None:
    #         des_list.remove((image_path, descriptor))

    image_paths = [x[0] for x in des_list]

    # Stack all the descriptors vertically in a numpy array
    print('-----------------------------------------')
    print('Start stacking of the descriptors......')

    # 方法1，np.vstack
    # i = 0
    # start_time = time.time()
    # descriptors = des_list[0][1]
    # for image_path, descriptor in des_list[1:]:
    #     descriptors = np.vstack((descriptors, descriptor))
    #     i += 1
    #     if i % 100 == 0:
    #         print('[{:.1f}s] The {}/{} descriptors has been stacked.'.format(
    # time.time() - start_time, i, len(des_list)))
    #         start_time = time.time()

    # 方法2，显著提升性能
    des_sum = 0
    for image_path, descriptor in des_list:
        des_sum += descriptor.shape[0]
    descriptors = np.zeros((des_sum, 128))

    position = 0
    for image_path, descriptor in des_list:
        sz = len(descriptor)
        descriptors[position:position + sz] = descriptor
        position += sz

    # Perform k-means clustering
    start_time = time.time()
    print('-----------------------------------------')
    print("Start k-means: %d words, %d key points..." % (num_words, descriptors.shape[0]))
    voc, variance = kmeans(descriptors, num_words, 1)
    print('[{:.1f}s] K-means has done.'.format(time.time() - start_time))

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
    joblib.dump((im_features, image_paths, idf, num_words, voc), pkl_path, compress=3)

# get_im_features('rumor', 'pkl/rumor_im_features.pkl')
