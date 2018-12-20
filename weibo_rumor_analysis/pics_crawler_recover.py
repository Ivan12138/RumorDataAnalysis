# -*- coding: utf-8 -*-
"""
@author: RMSnow
@file: pics_crawler_recover.py
@time: 18-12-20 上午11:14
@contact: xueyao_98@foxmail.com

# 重新抓取thumb的图片
"""

import pandas as pd
from rumor_pic_crawler import crawler

r_file = 'file/rumorThumbImage.csv'
t_file = 'file/truthThumbImage.csv'
r_df = pd.read_csv(r_file)
t_df = pd.read_csv(t_file)

rumor_pics = r_df['urls'].tolist()
truth_pics = t_df['urls'].tolist()

print(len(rumor_pics))
print(len(truth_pics))

rumor_pics = [r.replace('thumb150', 'mw690') for r in rumor_pics]
truth_pics = [t.replace('thumb150', 'mw690') for t in truth_pics]

crawler(rumor_pics, set(rumor_pics),'file/crawler/recover_rumor.txt',
        'file/crawler/recover_rumor_err.txt', '../../recover_rumor')
crawler(truth_pics, set(truth_pics),'file/crawler/recover_truth.txt',
        'file/crawler/recover_truth_err.txt', '../../recover_truth')
