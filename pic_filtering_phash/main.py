# encoding:utf-8

import get_matrix
import clustering_by_matrix
from sklearn.externals import joblib
import os
import time
import random


# =================================================================

# 说明：
# 对truth_pics_sampling(28779)与pics_filtered_img_rumor(17494)进行去重

# ============================= 初始化 =============================

# # 需要去重的图片文件夹
# pics_dir = '../../truth_pics_sampling'
# # 文件夹中的所有图片名
# pics_name_file = 'file/truth_pics_name.txt'
#
# with open(pics_name_file, 'w') as out:
#     for _, _, files in os.walk(pics_dir):
#         for file in files:
#             out.write('{}\n'.format(os.path.join(pics_dir, file)))
#
# with open(pics_name_file, 'r') as src:
#     lines = src.readlines()
# image_paths = [os.path.join(pics_dir, line.strip('\n').split('/')[-1]) for line in lines]
# sz = len(image_paths)
# print('正在对{}中的图片去重，其中共有{}张图片'.format(pics_dir.split('/')[-1], sz))

# ============================= 计算矩阵 =============================

# 计算所有图片的phash值
# get_matrix.get_phash_table(image_paths, sz)

# 根据phash值，计算图片的相似度矩阵
# sz = 28776
# image_paths, phash_list = joblib.load('pkl/phash_list_{}.pkl'.format(sz))
# print('img_sz = {}, phash_list_sz = {}'.format(len(image_paths), len(phash_list)))
# sz = len(phash_list)
# get_matrix.get_similarity_matrix(sz)


# ============================= Single Pass 聚类 =============================

# matrix = joblib.load('pkl/matrix_{}.pkl'.format(sz))
# clustering_by_matrix.main(sz, matrix, threshold=0.85)

# ============================= 展示聚类效果 =============================

def show_clustering_pics_dir(threshold):
    clustering_pics_dir = '../../clustering_truth_ts{}'.format(threshold)

    spc = joblib.load('pkl/phash_spc_28776_ts{}.pkl'.format(threshold))
    clusters = spc.cluster_list
    n_list = [c.node_list for c in clusters]

    print('clusters_size = {}, img_sz = {}, del_sz = {}'.format(
        len(clusters), sz, sz - len(clusters)))

    # 执行cp命令
    toCmd = input('是否执行cp命令(y/n)')
    if not toCmd == 'y':
        return

    valid_num = 0
    start_time = time.time()
    for index, node_list in enumerate(n_list):
        for node in node_list:
            img = image_paths[node]
            code = os.system('cp {} {}'.format(img, clustering_pics_dir + '/' + str(index) + '-' + img.split('/')[-1]))
            if code == 0:
                valid_num += 1

        if index % 100 == 0:
            print('Done {}/{} clusters, it took {:.1f}s'.format(
                index + 1, len(n_list), time.time() - start_time
            ))
            start_time = time.time()

    print('cp successfully! Valid_num = {}'.format(valid_num))


# show_clustering_pics_dir(threshold=0.75)
# show_clustering_pics_dir(threshold=0.8)
# show_clustering_pics_dir(threshold=0.85)

# ============================= mv =============================

# src_dir = '../../clustering_truth_ts0.85'
# out_dir = '../../handled_truth'

# img_names = dict()
# for _, _, files in os.walk(src_dir):
#     for file in files:
#         key = file.split('-')[0]
#         img_name = file.replace(key + '-', '')
#
#         if key not in img_names.keys():
#             img_names[key] = [img_name]
#         else:
#             img_names[key].append(img_name)
#
# for key, value in img_names.items():
#     cp_img = random.sample(value, 1)[0]
#     code = os.system('cp {} {}'.format(os.path.join(src_dir, key + '-' + cp_img), os.path.join))

# ============================= Truth Sampling =============================

get_matrix.random_sampling_truth()
