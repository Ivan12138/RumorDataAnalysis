# encoding:utf-8
import pandas as pd
import os
import json

file_path = 'file'

headers = ['userCertify', 'forward', 'praise', 'pic_num']
rumor_info = []


def gen_rumor_info():
    with open(os.path.join(file_path, 'rumor_weibo.json'), 'r') as src:
        lines = src.readlines()
        for line in lines:
            judge_info = json.loads(line)
            if 'reportedWeibo' in judge_info.keys():
                rumor_weibo = judge_info['reportedWeibo']
                if isinstance(rumor_weibo, dict):
                    if 'userCertify' in rumor_weibo.keys() and 'forward' in rumor_weibo.keys() and 'praise' in rumor_weibo.keys():
                        user_certify = rumor_weibo['userCertify']
                        weibo_forward = rumor_weibo['forward']
                        weibo_praise = rumor_weibo['praise']
                        pic_num = len(rumor_weibo['piclists'])

                        try:
                            weibo_forward = int(weibo_forward)
                            weibo_praise = int(weibo_praise)
                        except ValueError:
                            continue

                        rumor_info.append(dict(zip(headers, [user_certify, weibo_forward, weibo_praise, pic_num])))


def gen_rumor_info_updated(updated_file):
    with open(os.path.join(file_path, updated_file), 'r') as src:
        lines = src.readlines()
        for line in lines:
            judge_info = json.loads(line)
            rumor_weibo = judge_info['reportedWeibo']

            # 判断是否"已被发布者删除"
            if not isinstance(rumor_weibo, dict):
                continue
            # 判断用户认证的字段
            if 'userCertify' not in judge_info.keys():
                continue

            # 把forward、praise的异常值设为-1
            user_certify = judge_info['userCertify']
            weibo_forward = rumor_weibo['forward'] if 'forward' in rumor_weibo.keys() else -1
            weibo_praise = rumor_weibo['praise'] if 'praise' in rumor_weibo.keys() else -1
            pic_num = len(rumor_weibo['piclists'])
            try:
                weibo_forward = int(weibo_forward)
            except ValueError:
                weibo_forward = -1
            try:
                weibo_praise = int(weibo_praise)
            except ValueError:
                weibo_praise = -1

            rumor_info.append(dict(zip(headers, [user_certify, weibo_forward, weibo_praise, pic_num])))


def write_to_csv(csv_file):
    with open(os.path.join(file_path, csv_file), 'w') as out:
        out.write(headers[0])
        for header in headers[1:]:
            out.write(',{}'.format(header))
        out.write('\n')

        for rumor_dict in rumor_info:
            out.write('{}'.format(rumor_dict[headers[0]]))
            for header in headers[1:]:
                out.write(',{}'.format(rumor_dict[header]))
            out.write('\n')


gen_rumor_info_updated('rumor_weibo_updated.json')
# write_to_csv('rumor_info.csv')
write_to_csv('rumor_info_updated.csv')
