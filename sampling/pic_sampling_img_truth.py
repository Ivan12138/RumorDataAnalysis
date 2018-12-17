# encoding:utf-8

from sklearn.externals import joblib
import json
import random
import os

src_dir = '/media/Data/qipeng/modified_complete_images/crawler/raw/raw_img_truth'
out_dir = '/media/Data/qipeng/modified_complete_images/crawler/truth_pics_sampling'

event_features_list = joblib.load('file/pkl/event_features_all.pkl')

# to_sampling_num 为 需要采样的truth数量
rumor_pics_all_num = 21963
to_sampling_num = 30000

truth_pics_all_num = sum([event_features['pic_sum'] for event_features in event_features_list])
print('To_sampling_num = {}, Truth_pics_sz = {}'.format(to_sampling_num, truth_pics_all_num))

pic_sampling_factor = [e['pic_sum'] / truth_pics_all_num for e in event_features_list]
pics_sampling_num_of_event = [to_sampling_num * factor for factor in pic_sampling_factor]

# 变为整数
pics_sampling_num_of_event = [int(x + 0.5) for x in pics_sampling_num_of_event]
print('采样后的数量约为：{}'.format(sum(pics_sampling_num_of_event)))
print()

# sampling
pics_sampling_name = []
for i, event_features in enumerate(event_features_list):
    pics_sampling_name += random.sample(event_features['pic_name'], pics_sampling_num_of_event[i])

# cp
valid_num = 0
for name in pics_sampling_name:
    code = os.system('cp {} {}'.format(os.path.join(src_dir, name), out_dir))
    if code == 0:
        valid_num += 1

print('采集{}张图片完成，其中有{}张有效图片'.format(len(pics_sampling_name), valid_num))
