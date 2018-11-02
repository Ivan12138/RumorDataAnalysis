# encoding:utf-8

# ========== 把爬取时间 timestamp >﻿ 1539458594654 的微博插入数据库 ========== #

import json

# src_file = 'file/weibo_truth_unicode.txt'
src_file = 'file/_sample_weibo_truth_unicode.txt'
des_file = 'file/truth_weibo.csv'

valid_timestamp = 1539458594654

with open(src_file, 'r') as src:
    with open(des_file, 'w') as out:
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
                        # if header is headers[0]:
                        #     out.write('{}'.format(header))
                        # else:
                        #     out.write(',{}'.format(header))
                        out.write('{},'.format(header))
                    out.write('\n')

                for weibo in weibos:
                    for _, value in weibo.items():
                        out.write('{},'.format(value))
                    # for value in values:
                        # if value is values[0]:
                        #     out.write('{}'.format(value))
                        # else:
                        #     out.write(',{}'.format(value))
                        # out.write('{},'.format(value))
                    out.write('\n')

            break
