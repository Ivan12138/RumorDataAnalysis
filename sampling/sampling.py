# encoding:utf-8

# ============================ 真实微博：按比例采样 ============================
# 谣言微博：34611      userCertify字段（0：1：2） = 22：4：1
# 真实微博：154114     userCertify字段（0：1：2） = 5：2：5
#
# 真实微博来源：5979个事件

import json
from sklearn.externals import joblib
import random
import numpy as np

events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list = joblib.load(
    'file/pkl/event_sampling_factor.pkl')
sampling_num_of_event, certify_num_of_event = joblib.load('file/pkl/certify_num_of_every_event.pkl')
event_features_list = joblib.load('file/pkl/event_features.pkl')

# 按照事件微博数从小到大排列
event_weibos_num_array = np.array(event_weibos_num_list)
sorted_index_of_event = np.argsort(event_weibos_num_array)

result_index_of_event = dict()  # 在每个事件中需要抽取的微博索引, key为事件索引，value为微博索引的列表(0, 1, 2)

for i, sorted_index in enumerate(sorted_index_of_event):
    result_index = []

    sampling_num = sampling_num_of_event[sorted_index]  # 在本事件中需要抽取的微博数
    certify_num = certify_num_of_event[sorted_index]  # 在本事件中需要抽取的userCertify字段分别为多少
    event_features = event_features_list[sorted_index]  # 事件的属性字典

    next_certify_num = certify_num_of_event[sorted_index_of_event[i + 1]]

    # userCertify = 0
    if certify_num[0] < len(event_features['certify_0']):
        top_pic_index = np.argsort(event_features['pic_num_0'])[:certify_num[0]]
        result_index.append(np.array(event_features['certify_0'])[top_pic_index[::-1]].tolist())
    else:  # modify next userCertify_0
        certify_num[1] += certify_num[0] - len(event_features['certify_0'])
        certify_num[0] = len(event_features['certify_0'])
        result_index.append(event_features['certify_0'])

    # userCertify = 1
    if certify_num[1] < len(event_features['certify_1']):
        top_pic_index = np.argsort(event_features['pic_num_1'])[:certify_num[1]]
        result_index.append(np.array(event_features['certify_1'])[top_pic_index[::-1]].tolist())
    else:  # modify next userCertify_1
        certify_num[2] += certify_num[1] - len(event_features['certify_1'])
        certify_num[1] = len(event_features['certify_1'])
        result_index.append(event_features['certify_1'])

    # userCertify = 2
    if certify_num[2] < len(event_features['certify_2']):
        top_pic_index = np.argsort(event_features['pic_num_2'])[:certify_num[2]]
        result_index.append(np.array(event_features['certify_2'])[top_pic_index[::-1]].tolist())
    elif i != len(sorted_index_of_event) - 1:  # modify next userCertify_2
        certify_num_of_event[sorted_index_of_event[i + 1]][0] += certify_num[2] - len(event_features['certify_2'])
        certify_num[2] = len(event_features['certify_2'])
        result_index.append(event_features['certify_2'])
    else:  # 最后一个事件
        result_index.append(event_features['certify_2'])

    result_index_of_event[sorted_index] = result_index
