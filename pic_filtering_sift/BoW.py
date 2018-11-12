# encoding:utf-8

import cv2
import numpy as np
from sklearn.externals import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing


# 词袋模型：导入图片，最终生成单词本
def get_words_dict_from_img(image_paths, pkl_path, num_words=1000):
    # image_paths: list.
    # pkl_path: the file of being stored pkl, just like 'words_dict.pkl'
    # num_words: K-means Param. Default 1000.

    # Create feature extraction and key points detector objects
    sift = cv2.xfeatures2d.SIFT_create()

    # List where all the descriptors are stored
    des_list = []

    for i, image_path in enumerate(image_paths):
        im = cv2.imread(image_path)
        print("Extract SIFT %d of %d images" % (i, len(image_paths)))
        kpts, des = sift.detectAndCompute(im, None)
        des_list.append((image_path, des))

    # Stack all the descriptors vertically in a numpy array
    descriptors = des_list[0][1]
    for image_path, descriptor in des_list[1:]:
        descriptors = np.vstack((descriptors, descriptor))

    # Perform k-means clustering
    print("Start k-means: %d words, %d key points" % (num_words, descriptors.shape[0]))
    voc, variance = kmeans(descriptors, num_words, 1)

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

    joblib.dump((im_features, image_paths, idf, num_words, voc), pkl_path, compress=3)
