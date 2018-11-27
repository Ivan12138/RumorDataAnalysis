# encoding:utf-8

import json
from sklearn.externals import joblib
import random
import numpy as np


def _get_pic_result_for_certify(event_features, certify_num, i):
    # 获取图片数最大的
    # top_pic_index = np.argsort(event_features['pic_num_' + str(i)])
    # result = np.array(event_features['certify_' + str(i)])[top_pic_index[::-1][:certify_num[i]]]
    # return result

    # 随机获取
    return np.array(random.sample(event_features['certify_' + str(i)], certify_num[i]))


# 计算出采样的索引
def get_result():
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

        # TODO: 如果过滤后的该事件不存在
        # if event_features == '':
        #     result_index_of_event[sorted_index] = ''
        #     continue

        # The last one
        if i == len(sorted_index_of_event) - 1:
            if certify_num[0] < len(event_features['certify_0']):
                result = _get_pic_result_for_certify(event_features, certify_num, 0)
                result_index.append(result.tolist())
            else:
                certify_num[0] = len(event_features['certify_0'])
                result_index.append(event_features['certify_0'])

            if certify_num[1] < len(event_features['certify_1']):
                result = _get_pic_result_for_certify(event_features, certify_num, 1)
                result_index.append(result.tolist())
            else:
                certify_num[1] = len(event_features['certify_1'])
                result_index.append(event_features['certify_1'])

            if certify_num[2] < len(event_features['certify_2']):
                result = _get_pic_result_for_certify(event_features, certify_num, 2)
                result_index.append(result.tolist())
            else:
                certify_num[2] = len(event_features['certify_2'])
                result_index.append(event_features['certify_2'])

            result_index_of_event[sorted_index] = result_index
            break

        next_certify_num = certify_num_of_event[sorted_index_of_event[i + 1]]

        # userCertify = 0
        if certify_num[0] < len(event_features['certify_0']):
            result = _get_pic_result_for_certify(event_features, certify_num, 0)
            result_index.append(result.tolist())
        else:  # modify next userCertify_0
            next_certify_num[0] += certify_num[0] - len(event_features['certify_0'])
            certify_num[0] = len(event_features['certify_0'])
            result_index.append(event_features['certify_0'])

        # userCertify = 1
        if certify_num[1] < len(event_features['certify_1']):
            result = _get_pic_result_for_certify(event_features, certify_num, 1)
            result_index.append(result.tolist())
        else:  # modify next userCertify_1
            next_certify_num[1] += certify_num[1] - len(event_features['certify_1'])
            certify_num[1] = len(event_features['certify_1'])
            result_index.append(event_features['certify_1'])

        # userCertify = 2
        if certify_num[2] < len(event_features['certify_2']):
            result = _get_pic_result_for_certify(event_features, certify_num, 2)
            result_index.append(result.tolist())
        else:  # modify next userCertify_2
            next_certify_num[2] += certify_num[2] - len(event_features['certify_2'])
            certify_num[2] = len(event_features['certify_2'])
            result_index.append(event_features['certify_2'])

        result_index_of_event[sorted_index] = result_index

    joblib.dump((certify_num_of_event, result_index_of_event), 'file/pkl/result.pkl')


# 采样后的图片数
def _cal_result_pic_num():
    certify_num_of_event, result_index_of_event = joblib.load('file/pkl/result.pkl')
    event_features_list = joblib.load('file/pkl/event_features.pkl')

    result_pic_num_list = []
    for index, result in result_index_of_event.items():
        pic_num = 0

        event_features = event_features_list[index]
        for certify_list in result:
            for i in certify_list:
                pic_num += event_features['pic_num'][i]

        result_pic_num_list.append(pic_num)

    return sum(result_pic_num_list)


# 按照result得到的索引去采样
def get_weibo_truth_sampling_file():
    certify_num_of_event, result_index_of_event = joblib.load('file/pkl/result.pkl')

    sampling_event_dict_list = []
    with open('file/weibo_truth_filtered.json', 'r') as src:
        lines = src.readlines()
        for index, line in enumerate(lines):
            event_dict = json.loads(line)

            # TODO: 如果过滤后的该事件不存在
            # if len(event_dict) == 0:
            #     continue

            result_index = [i for result in result_index_of_event[index] for i in result]
            raw_weibos = event_dict['weibo']
            event_dict['weibo'] = [raw_weibos[i] for i in result_index]
            sampling_event_dict_list.append(event_dict)

    out = open('file/weibo_truth_sampling.json', 'w')
    out_pretty = open('file/weibo_truth_sampling_pretty.json', 'w')

    for sampling_event in sampling_event_dict_list:
        out.write('{}\n'.format(json.dumps(sampling_event, ensure_ascii=False)))
        out_pretty.write('{}\n'.format(json.dumps(sampling_event, ensure_ascii=False, indent=4, separators=(',', ':'))))

    out.close()
    out_pretty.close()

    # 统计微博数量、图片数量、userCertify分布
    with open('file/weibo_truth_sampling.json', 'r', encoding='utf-8') as src:
        lines = src.readlines()
        sampling_weibo_num = 0
        sampling_pic_num = 0
        certify_0 = 0
        certify_1 = 0
        certify_2 = 0

        for line in lines:
            event = json.loads(line, encoding='utf-8-sig')
            for truth in event['weibo']:
                sampling_weibo_num += 1
                sampling_pic_num += len(truth['piclist'])
                if 'userCertify' in truth.keys():
                    certify = truth['userCertify']
                    if certify == 0:
                        certify_0 += 1
                    elif certify == 1:
                        certify_1 += 1
                    else:
                        certify_2 += 1

        print('聚类后的真实微博：数量为{}，图片数量为{}'.format(sampling_weibo_num, sampling_pic_num))
        print('（{}）{}:{}:{} = {:.1f} : {:.1f} : 1'.format(
            certify_0 + certify_1 + certify_2, certify_0, certify_1,
            certify_2, certify_0 / certify_2, certify_1 / certify_2))


# get_result()
get_weibo_truth_sampling_file()
