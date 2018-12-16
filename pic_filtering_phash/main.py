# encoding:utf-8

import get_matrix
import clustering_by_matrix

# ============================= 初始化 =============================

# 需要去重的图片文件夹
rumor_pics_dir = '/media/Data/qipeng/modified_complete_images/crawler/pics_modal/pics_filtered_img_rumor'
# 文件夹中的所有图片名
rumor_pics_name_file = 'file/rumor_pics_name.txt'

with open(rumor_pics_name_file, 'r') as src:
    lines = src.readlines()
image_paths = [line.strip('\n') for line in lines]
sz = len(image_paths)
print('正在对{}中的图片去重，其中共有{}张图片'.format(rumor_pics_dir.split('/')[-1], sz))

# ============================= 计算矩阵 =============================

# 计算所有图片的phash值
get_matrix.get_phash_table(image_paths, sz)

# 根据phash值，计算图片的相似度矩阵
get_matrix.get_similarity_matrix(sz)

# ============================= Single Pass 聚类 =============================
