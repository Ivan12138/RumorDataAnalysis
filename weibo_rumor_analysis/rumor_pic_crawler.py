# encoding:utf-8
import json
import time
import socket
import urllib
from urllib.request import urlretrieve
import traceback
import os


def crawler(pic_lists, pic_set, file_of_img, file_of_err_img, stored_path):
    start_time = time.time()
    # 设置超时时间为10s
    socket.setdefaulttimeout(10)

    size = len(pic_set)
    ok_i = 0
    err_i = 0
    with open(file_of_img, 'w') as ok_out:
        with open(file_of_err_img, 'w') as err_out:
            # 数量统计
            ok_out.write('-------------------------\n')
            ok_out.write('There are {} imgs in pic_lists.\n'.format(len(pic_lists)))
            ok_out.write('Unique imgs are {}.\n'.format(len(pic_set)))
            ok_out.write('-------------------------\n')

            for pic_url in pic_set:
                pic_name = pic_url.split('/')[-1]
                try:
                    # 如果url中不含http: / https:前缀，则自动补全
                    if 'http:' not in pic_url and 'https:' not in pic_url:
                        pic_url = 'http:' + pic_url
                    urlretrieve(pic_url, os.path.join(stored_path, pic_name))
                    ok_i += 1
                except:
                    err_i += 1
                    err_out.write("[Error] Something wrong in downloading {} !\n".format(pic_url))
                finally:
                    if (ok_i + err_i) % 100 == 0:
                        ok_out.write('{}: Downloading {} pics and {} err_pics, {:.2f}%, {:.2f} sec...\n'.format(
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ok_i, err_i,
                            (ok_i + err_i) / size * 100, time.time() - start_time))


def crawler_once():
    with open('file/rumor_weibo.json', 'r') as src:
        lines = src.readlines()
        pic_lists = []
        for judge_weibo_json in lines:
            judge_info = json.loads(judge_weibo_json)
            if 'reportedWeibo' in judge_info.keys():
                reported_weibo = judge_info['reportedWeibo']
                if isinstance(reported_weibo, dict):
                    if 'piclists' in reported_weibo.keys():
                        curr_pics = reported_weibo['piclists']
                        if curr_pics is not None:
                            pic_lists += curr_pics

    pic_set = set(pic_lists)
    crawler(pic_lists, pic_set, 'downloading_rumor_img_log.txt', 'downloading_rumor_img_err_log.txt', '../img_rumor')


def crawler_twice():
    with open('downloading_rumor_img_err_log.txt', 'r') as src:
        lines = src.readlines()
        url_list = []
        for line in lines:
            url = line.split('[Error] Something wrong in downloading ')[1].split(' !')[0]
            # 去掉http:前缀
            url = url.split('http:')[1]
            url_list.append(url)

    url_set = set(url_list)
    crawler(url_list, url_set, 'downloading_twice_rumor_img_log.txt', 'downloading_twice_rumor_img_err_log.txt',
            '../img_rumor')


crawler_twice()
