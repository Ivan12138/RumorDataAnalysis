# encoding:utf-8

# ========== 把爬取时间 timestamp >﻿ 1539458594654 的微博插入数据库 ========== #

import json

src_file = 'file/weibo_truth.txt'
# src_file = 'file/_sample_weibo_truth.txt'
des_file = 'file/truth_weibo.csv'

valid_timestamp = 1539458594654

filter_keys = ['content', 'url', 'piclist']
selected_keys = ['name', 'userCertify', 'userWeiboCount', 'userFollowCount', 'userFanCount', 'forward', 'praise']
extreme_keys = selected_keys + ['pic_num']


def gen_csv_with_filter_keys():
    count = 0
    with open(src_file, 'r') as src:
        with open('file/truth_weibo_filter.csv', 'w') as out:
            lines = src.readlines()
            for line in lines:
                weibo_dict = json.loads(line, encoding='UTF-8')

                # 判断爬取时间
                if weibo_dict['timestamp'] < valid_timestamp:
                    weibos = weibo_dict['weibo']

                    # Header
                    if line is lines[0]:
                        headers = weibos[0].keys()
                        for header in headers:
                            if header not in filter_keys:
                                out.write('{},'.format(header))
                        out.write('\n')

                    for weibo in weibos:
                        # 查找缺失的问题
                        # if len(weibo) != len(headers):
                        #     print('Something wrong in line{}, weibo{} and length of the weibo is {}.'.format(
                        #         lines.index(line), weibos.index(weibo), len(weibo)))
                        #     count += 1

                        keys = weibo.keys()
                        for header in headers:
                            if header not in keys:
                                out.write('Missing,')
                            else:
                                out.write('{},'.format(weibo[header]))
                        out.write('\n')

                if count == 1:
                    break


def gen_csv_with_selected_keys():
    write_headers = False
    with open(src_file, 'r') as src:
        with open(des_file, 'w') as out:
            lines = src.readlines()

            # print(json.loads(lines[0])['weibo'][0].keys())

            for line in lines:
                weibo_dict = json.loads(line, encoding='UTF-8')

                # 判断爬取时间
                if weibo_dict['timestamp'] < valid_timestamp:
                    weibos = weibo_dict['weibo']

                    # Header
                    headers = selected_keys
                    if write_headers is False:
                        for header in headers:
                            out.write('{},'.format(header))
                        out.write('\n')
                        write_headers = True

                    for weibo in weibos:
                        keys = weibo.keys()
                        for header in headers:
                            if header not in keys:
                                out.write(',')
                            else:
                                out.write('{},'.format(weibo[header]))
                        out.write('\n')


def get_truth_dict_list():
    truth_dict_list = []
    with open(src_file, 'r') as src:
        lines = src.readlines()
        for line in lines:
            weibo_dict = json.loads(line, encoding='UTF-8')
            # 判断爬取时间
            if weibo_dict['timestamp'] < valid_timestamp:
                weibos = weibo_dict['weibo']

                for weibo in weibos:
                    truth_info = []

                    for key in selected_keys:
                        if key in weibo.keys():
                            truth_info.append(weibo[key])
                        else:
                            truth_info.append('')
                    # pic_num
                    if 'piclist' in weibo.keys() and isinstance(weibo['piclist'], list):
                        truth_info.append(len(weibo['piclist']))
                    else:
                        truth_info.append(0)

                    truth_dict = dict(zip(extreme_keys, truth_info))
                    truth_dict_list.append(truth_dict)

    return truth_dict_list


def write_to_csv(truth_dict_list):
    with open(des_file, 'w') as out:
        # Header
        out.write(extreme_keys[0])
        for header in extreme_keys[1:]:
            out.write(',{}'.format(header))
        out.write('\n')

        # truth_weibo
        for truth_dict in truth_dict_list:
            out.write(truth_dict[extreme_keys[0]])
            for key in extreme_keys[1:]:
                out.write(',{}'.format(truth_dict[key]))
            out.write('\n')


write_to_csv(get_truth_dict_list())
