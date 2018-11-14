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


def write_to_csv():
    with open(os.path.join(file_path, 'rumor_info.csv'), 'w') as out:
        out.write(headers[0])
        for header in headers[1:]:
            out.write(',{}'.format(header))
        out.write('\n')

        for rumor_dict in rumor_info:
            out.write('{}'.format(rumor_dict[headers[0]]))
            for header in headers[1:]:
                out.write(',{}'.format(rumor_dict[header]))
            out.write('\n')


gen_rumor_info()
write_to_csv()
