# encoding:utf-8

from sklearn.externals import joblib
import json
import random
import os

src_dir = '../../raw_img_truth'
out_dir = '../../pics_sampling_img_truth'

event_features_list = joblib.load('file/pkl/event_features_all.pkl')
rumor_pics_all_num = 21963
truth_pics_all_num = sum([event_features['pic_sum'] for event_features in event_features_list])

pic_sampling_factor = [e['pic_sum'] / truth_pics_all_num for e in event_features_list]
pics_sampling_num_of_event = [rumor_pics_all_num * factor for factor in pic_sampling_factor]

# 变为整数
pics_sampling_num_of_event = [int(x + 0.7) for x in pics_sampling_num_of_event]
print(sum(pics_sampling_num_of_event))
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
