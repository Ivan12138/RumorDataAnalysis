# -*- coding: utf-8 -*-
"""
@author: RMSnow
@file: pics_crawler_recover.py
@time: 18-12-20 上午11:14
@contact: xueyao_98@foxmail.com

# 重新抓取thumb的图片
"""

import pandas as pd
import json
import os

from rumor_pic_crawler import crawler

multimodal_rumor_pics_file = 'file/crawler/multimodal_rumor_pics.txt'
multimodal_truth_pics_file = 'file/crawler/multimodal_truth_pics.txt'
rumor_file = 'file/rumor_weibo_updated.json'
truth_file = '../weibo_truth_analysis/file/weibo_truth_no_event.txt'


# 抓取多模态数据集中的pic
def get_all_thumb_pics_url(pics_file, json_file):
    with open(pics_file, 'r') as src:
        pics_name = [pic.strip() for pic in src.readlines()]

    with open(json_file, 'r') as src:
        lines = src.readlines()

    all_pics_url_list = []
    for line in lines:
        if pics_file == multimodal_rumor_pics_file:
            weibo = json.loads(line, encoding='utf-8')['reportedWeibo']
            if isinstance(weibo, str):
                continue
            if isinstance(weibo['piclists'], list) and len(weibo['piclists']) != 0:
                all_pics_url_list += weibo['piclists']
        else:
            weibo = json.loads(line, encoding='utf-8')
            if isinstance(weibo['piclist'], list) and len(weibo['piclist']) != 0:
                all_pics_url_list += weibo['piclist']

    # 遍历所有的url，把pics_name中存在thumb的挑出来
    thumb_pics_url_list = []
    for url in all_pics_url_list:
        if 'thumb150' in url:
            name = url.split('/')[-1]
            if name in pics_name:
                thumb_pics_url_list.append(url)

    return thumb_pics_url_list


def main():
    multimodal_rumor_pics = get_all_thumb_pics_url(multimodal_rumor_pics_file, rumor_file)
    multimodal_truth_pics = get_all_thumb_pics_url(multimodal_truth_pics_file, truth_file)

    multimodal_rumor_pics = [r.replace('thumb150', 'mw690') for r in multimodal_rumor_pics]
    multimodal_truth_pics = [t.replace('thumb150', 'mw690') for t in multimodal_truth_pics]

    print(len(multimodal_rumor_pics))
    print(len(multimodal_truth_pics))

    crawler(multimodal_rumor_pics, set(multimodal_rumor_pics), 'file/crawler/recover_rumor.txt',
            'file/crawler/recover_rumor_err.txt', '../../recover_multimodal_rumor')
    crawler(multimodal_truth_pics, set(multimodal_truth_pics), 'file/crawler/recover_truth.txt',
            'file/crawler/recover_truth_err.txt', '../../recover_multimodal_truth')


# main()

# test
with open(multimodal_truth_pics_file, 'r') as src:
    pics_name = [pic.strip() for pic in src.readlines()]
for _,_,files in os.walk('../../recover_multimodal_truth'):
    for file in files:
        if file in pics_name:
            print(file)