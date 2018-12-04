# encoding:utf-8

import numpy as np
import imagehash
from PIL import Image
from sklearn.externals import joblib
import time

rumor_pics_dir = '../../pics_filtered_img_rumor_todo'
pics_txt = '../pic_filtering_sift/file/pics_rumor_all_todo.txt'

with open(pics_txt, 'r') as src:
    lines = src.readlines()
image_paths = [rumor_pics_dir + '/' + line.strip('\n') for line in lines]


# 计算两张图片的 pHash 距离
def similarity_distance_by_file(file1, file2):
    p_hash1 = imagehash.phash(Image.open(file1))
    p_hash2 = imagehash.phash(Image.open(file2))

    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    return similarity


def similarity_distance(p_hash1, p_hash2):
    similarity = 1 - (p_hash1 - p_hash2) / len(p_hash1.hash) ** 2
    return similarity


def get_phash_table():
    phash_list = []
    sz = len(image_paths)

    start_time = time.time()
    for i in range(sz):
        phash_list.append(imagehash.phash(Image.open(image_paths[i])))
        if i % 50 == 0:
            print('Img {}/{} Done. It took {:.1f}s...'.format(i + 1, sz, time.time() - start_time))
    joblib.dump(phash_list, 'pkl/phash_list.pkl')


# get_phash_table()


def get_similarity_matrix():
    print('Get Started Generating Matrix...')

    phash_list = joblib.load('pkl/phash_list.pkl')
    sz = len(image_paths)
    matrix = np.zeros((sz, sz))

    for i in range(sz):
        start_time = time.time()
        print('----------------------------------------------')
        print('Handling matrix the {}th lines...'.format(i))
        for j in range(i + 1, sz):
            matrix[i][j] = similarity_distance(phash_list[i], phash_list[j])
        print('It takes {:.1f}s'.format(time.time() - start_time))

    joblib.dump(matrix, 'pkl/matrix.pkl')


get_similarity_matrix()
