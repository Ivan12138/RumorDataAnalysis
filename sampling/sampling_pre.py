# encoding:utf-8

import json
from sklearn.externals import joblib
import random

# Rumor Features
rumor_weibo_sum = 7880
rumor_certify = 5942
rumor_0 = 4439
rumor_1 = 1284
rumor_2 = 219


# 把过滤后truth微博，重新以event的形式组织
def rearrange_filtered_truth_by_event():
    with open('../weibo_truth_analysis/file/weibo_truth.txt', 'r') as src:
        events = src.readlines()

    filtered_events = dict()  # key = index, value = event(dict)

    with open('../text_filtering/file/weibo_truth_once_text_filtered.json', 'r') as src:
        lines = src.readlines()
        for line in lines:
            truth_weibo = json.loads(line, encoding='utf-8')
            event_index = truth_weibo['_position'][0]

            # 首次出现的事件
            if event_index not in filtered_events.keys():
                filtered_events[event_index] = dict()
                filtered_event = filtered_events[event_index]

                event = json.loads(events[event_index])
                filtered_event['id'] = event['id']
                filtered_event['weibo'] = [truth_weibo]
            else:
                filtered_event = filtered_events[event_index]
                filtered_event['weibo'].append(truth_weibo)

    # 文本过滤后，5979个事件变为了5469个事件
    print('filtered_event_len = {}'.format(len(filtered_events)))

    out = open('file/weibo_truth_filtered.json', 'w')
    out_pretty = open('file/weibo_truth_filtered_pretty.json', 'w')
    for i, e in filtered_events.items():
        out.write('{}\n'.format(json.dumps(e, ensure_ascii=False)))
        out_pretty.write('{}\n'.format(json.dumps(e, ensure_ascii=False, indent=4, separators=(',', ':'))))
        out.flush()
        out_pretty.flush()
    out.close()
    out_pretty.close()


# 得到每个事件的 微博数/总微博数
def get_event_sampling_factor():
    with open('file/weibo_truth_filtered.json', 'r') as src:
        lines = src.readlines()

        events_num = len(lines)
        weibos_num = 0
        event_weibos_num_list = []

        for line in lines:
            event_dict = json.loads(line)
            weibos = event_dict['weibo']
            weibos_num += len(weibos)
            event_weibos_num_list.append(len(weibos))

        event_sampling_factor_list = [x / weibos_num for x in event_weibos_num_list]

    global_sampling_factor = rumor_weibo_sum / weibos_num
    print('events_num = {}, weibos_num = {}'.format(events_num, weibos_num))
    joblib.dump((events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list),
                'file/pkl/event_sampling_factor.pkl')


def get_event_certify_num(threshold=0.75):
    events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list = joblib.load(
        'file/pkl/event_sampling_factor.pkl')
    # 计算在每个事件中抽取的微博数
    raw_sampling_num_of_event = [weibos_num * global_sampling_factor * factor for factor in event_sampling_factor_list]
    raw_sampling_num_of_event = [int(x + 0.5) for x in raw_sampling_num_of_event]
    # sampling_num_of_event = [1 if x == 0 else x for x in sampling_num_of_event]

    # 以一定的机率更新sampling为0的事件（用来调节sampling的样本数）
    sampling_num_of_event = []
    for sampling_num in raw_sampling_num_of_event:
        rand = random.random()
        if rand > threshold:
            sampling_num = 1 if sampling_num == 0 else sampling_num
        sampling_num_of_event.append(sampling_num)

    # 计算不同的userCertify字段应该分别抽取多少微博
    float_certify_num_of_event = [
        [rumor_0 / rumor_certify * x, rumor_1 / rumor_certify * x, rumor_2 / rumor_certify * x]
        for x in sampling_num_of_event]
    certify_num_of_event = []
    for index, float_certify_num in enumerate(float_certify_num_of_event):
        # the last one
        if index == len(float_certify_num_of_event) - 1:
            certify_num_of_event.append([int(x + 1) for x in float_certify_num])
            continue

        next_float_certify_num = float_certify_num_of_event[index + 1]

        certify_num = [int(x) for x in float_certify_num]
        next_float_certify_num[0] += float_certify_num[0] - certify_num[0]
        next_float_certify_num[1] += float_certify_num[1] - certify_num[1]
        next_float_certify_num[2] += float_certify_num[2] - certify_num[2]

        certify_num_of_event.append(certify_num)

    # 更新在每个事件中抽取的微博数
    sampling_num_of_event = [sum(x) for x in certify_num_of_event]

    joblib.dump((sampling_num_of_event, certify_num_of_event), 'file/pkl/certify_num_of_every_event.pkl')

    # 打印sampling的结果
    c0 = sum([x[0] for x in certify_num_of_event])
    c1 = sum([x[1] for x in certify_num_of_event])
    c2 = sum([x[2] for x in certify_num_of_event])
    print('采样数：{}，userCertify的分布为：({}) {}:{}:{} = {:.1f} : {:.1f} : 1'.format(
        sum(sampling_num_of_event), c0 + c1 + c2, c0, c1, c2, c0 / c2, c1 / c2))


def get_event_features(src_file, pkl_file):
    event_features_list = []
    with open(src_file, 'r') as src:
        lines = src.readlines()
        for line in lines:
            event_dict = json.loads(line)
            weibos = event_dict['weibo']

            certify_0 = []
            certify_1 = []
            certify_2 = []
            pic_num = []
            pic_name = []
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
                    names = [name.split('/')[-1] for name in weibo['piclist']]
                    pic_name += names
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
            event_features['pic_sum'] = sum(pic_num)
            event_features['pic_name'] = pic_name

            event_features_list.append(event_features)
    joblib.dump(event_features_list, pkl_file)

get_event_features('../weibo_truth_analysis/file/weibo_truth.txt', 'file/pkl/event_features_all.pkl')
