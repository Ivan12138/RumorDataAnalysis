# -*- coding: utf-8 -*-
"""
@author: RMSnow
@file: _test.py
@time: 18-12-19 下午9:57
@contact: xueyao_98@foxmail.com

# weibo_truth.txt 展开成微博级别
"""

import json

with open('file/weibo_truth.txt', 'r') as src:
    lines = src.readlines()
    full_weibos = []
    for line in lines:
        event = json.loads(line, encoding='utf-8')
        full_weibos += event['weibo']

    print(len(full_weibos))

with open('file/weibo_truth_no_event.txt', 'w') as out:
    with open('file/weibo_truth_no_event_pretty.txt', 'w') as out_pretty:
        for weibo in full_weibos:
            out.write('{}\n'.format(json.dumps(weibo, ensure_ascii=False)))
            out_pretty.write('{}\n'.format(json.dumps(weibo, ensure_ascii=False, indent=4, separators=(',', ':'))))

with open('file/weibo_truth_no_event.txt', 'r') as src:
    print(len(src.readlines()))
