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


# --------------- Step1: 计算【每个事件】的【每个userCertify字段】分别应该抽取多少微博 ---------------

# 得到每个事件的 微博数/总微博数
def get_event_sampling_factor():
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
        lines = src.readlines()

        events_num = len(lines)
        weibos_num = 0
        event_weibos_num_list = []

        for line in lines:
            event_dict = json.loads(line)
            weibos = event_dict['weibo']
            weibos_num += len(weibos)
            event_weibos_num_list.append(len(weibos))

            # test
            # index = lines.index(line)
            # if index < 5:
            #     print(len(weibos))

        event_sampling_factor_list = [x / weibos_num for x in event_weibos_num_list]

    global_sampling_factor = 34611 / weibos_num
    joblib.dump((events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list),
                'file/pkl/event_sampling_factor.pkl')


# get_event_sampling_factor()
events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list = joblib.load(
    'file/pkl/event_sampling_factor.pkl')

# 计算在每个事件中抽取的微博数
sampling_num_of_event = [weibos_num * global_sampling_factor * factor for factor in event_sampling_factor_list]
sampling_num_of_event = [int(x + 0.5) for x in sampling_num_of_event]
sampling_num_of_event = [1 if x == 0 else x for x in sampling_num_of_event]

# 计算不同的userCertify字段应该分别抽取多少微博
certify_num_of_event = []
for x in sampling_num_of_event:
    certify_num = [22 / 27 * x, 4 / 27 * x, 1 / 27 * x]
    certify_num = [int(x + 0.5) for x in certify_num]
    # certify_num = [1 if x == 0 else x for x in certify_num]

    # 按照一定的概率，将0更新为1
    updated_certify_num = []
    for num in certify_num:
        rand = random.random()
        if rand >= 0.9:
            num = 1 if num == 0 else num
        updated_certify_num.append(num)

    certify_num_of_event.append(updated_certify_num)

# 更新在每个事件中抽取的微博数
sampling_num_of_event = [sum(x) for x in certify_num_of_event]


# ------------------------------------ Step2: 计算【事件-微博】的特性 ---------------------------------
def get_event_features():
    event_features_list = []
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
        lines = src.readlines()
        for line in lines:
            event_dict = json.loads(line)
            weibos = event_dict['weibo']

            certify_0 = []
            certify_1 = []
            certify_2 = []
            pic_num = []
            for index, weibo in enumerate(weibos):
                certify = weibo['userCertify']
                if certify == 0:
                    certify_0.append(index)
                elif certify == 1:
                    certify_1.append(index)
                else:
                    certify_2.append(index)

                if 'piclist' in weibo.keys() and isinstance(weibo['piclist'], list):
                    pic_num.append(len(weibo['piclist']))
                else:
                    pic_num.append(0)

            event_features = dict()
            event_features['id'] = event_dict['id']
            event_features['weibo_num'] = len(weibos)
            event_features['certify_0'] = certify_0
            event_features['certify_1'] = certify_1
            event_features['certify_2'] = certify_2
            event_features['pic_num_0'] = [pic_num[x] for x in certify_0]
            event_features['pic_num_1'] = [pic_num[x] for x in certify_1]
            event_features['pic_num_2'] = [pic_num[x] for x in certify_2]
            event_features['pic_num'] = pic_num

            event_features_list.append(event_features)
    joblib.dump(event_features_list, 'file/pkl/event_features.pkl')


# get_event_features()
event_features_list = joblib.load('file/pkl/event_features.pkl')

# ------------------------------------ Step3: Sampling ---------------------------------

# 按照事件微博数从小到大排列
event_weibos_num_array = np.array(event_weibos_num_list)
sorted_index_of_event = np.argsort(event_weibos_num_array)

result_index_of_event = {}  # 在每个事件中需要抽取的微博索引, key为事件索引，value为微博索引的列表

# with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
#     lines = src.readlines()
#     for index in sorted_index_of_event:
#         sampling_num = sampling_num_of_event[index]  # 在本事件中需要抽取的微博数
#         certify_num = certify_num_of_event[index]  # 在本事件中需要抽取的userCertify字段分别为多少
#
#         event_dict = json.loads(lines[index])
#         event_weibos = event_dict['weibo']
