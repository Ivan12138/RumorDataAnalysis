# encoding:utf-8

# =========== 爬虫：根据json文件中的图片URL进行下载 =========== #

from urllib.request import urlretrieve
import json
import socket
import time

with open('weibo_truth_unicode.txt', 'r') as src:
    lines = src.readlines()
    pic_lists = []
    for json_obj in lines:
        weibo_dict = json.loads(json_obj)
        for key, value in weibo_dict.items():
            if key == 'weibo':
                for single_weibo in value:
                    if 'piclist' in single_weibo.keys():
                        curr_pic = single_weibo['piclist']
                        if curr_pic is not None:
                            pic_lists += curr_pic

pic_set = set(pic_lists)

start_time = time.time()
# 设置超时时间为30s
socket.setdefaulttimeout(10)

size = len(pic_set)
ok_i = 0
err_i = 0
with open('downloading_img_log.txt', 'w') as ok_out:
    with open('downloading_img_err_log.txt', 'w') as err_out:
        # 数量统计
        ok_out.write('-------------------------\n')
        ok_out.write('There are {} imgs in pic_lists.'.format(len(pic_lists)))
        ok_out.write('Unique imgs are {}.'.format(len(pic_set)))
        ok_out.write('-------------------------\n')

        for pic_url in pic_set:
            pic_name = pic_url.split('/')[-1]
            try:
                urlretrieve(pic_url, './img/' + pic_name)
                ok_i += 1
            except socket.timeout:
                count = 1
                while count <= 5:
                    try:
                        urlretrieve(pic_url, pic_name)
                        break
                    except socket.timeout:
                        err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                        print(err_info)
                        count += 1
                if count > 5:
                    print("downloading picture failed!")
            except:
                err_i += 1
                err_out.write("[Error] Something wrong in downloading {} !\n".format(pic_url))
            finally:
                # ok_i += 1
                if (ok_i + err_i) % 100 == 0:
                    ok_out.write('Downloading {} pics and {} err_pics, {:.2f}%, {:.2f} sec...\n'.format(ok_i, err_i, (
                        ok_i + err_i) / size * 100, time.time() - start_time))
