# encoding:utf-8

import cv2
import os
import time

root_dir = '../../'
rumor_all_dir = 'pics_filtered_img_rumor_todo'
truth_sampling_dir = 'pics_sampling_img_truth_todo'
rumor_text_filtered_dir = 'text_filtered_img_rumor'
truth_text_filtered_dir = 'text_filtered_img_truth'

dirs_4_category = [rumor_all_dir, truth_sampling_dir, rumor_text_filtered_dir, truth_text_filtered_dir]


def get_files_list(pics_dir):
    handled_dir = os.path.join(root_dir, pics_dir)
    for root, dirs, files in os.walk(handled_dir):
        files_list = files
    files_list = [os.path.join(handled_dir, f) for f in files_list]
    return files_list


files_4_category = [get_files_list(d) for d in dirs_4_category]


# 去除180*180的图片
def del_topic_pics(category_no):
    print('-----------------------------------')
    print('正在处理{}...'.format(dirs_4_category[category_no]))

    num = 0
    err_num = 0
    for index, file in enumerate(files_4_category[category_no]):
        img = cv2.imread(file)
        try:
            shape = img.shape
        except AttributeError:  # 无效文件
            os.system('mv {} {}'.format(file, root_dir + 'topic_' + dirs_4_category[category_no]))
            err_num += 1
            continue

        if shape[0] == 180 and shape[1] == 180:
            # 执行move命令
            os.system('mv {} {}'.format(file, root_dir + 'topic_' + dirs_4_category[category_no]))
            num += 1

        if shape[0] == 160 and shape[1] == 160:
            # 执行move命令
            os.system('mv {} {}'.format(file, root_dir + 'topic_' + dirs_4_category[category_no]))
            num += 1

        if shape[0] == 200 and shape[1] == 200:
            # 执行move命令
            os.system('mv {} {}'.format(file, root_dir + 'topic_' + dirs_4_category[category_no]))
            num += 1

        if index % 200 == 0:
            print('[{}] 已处理{}/{}张图片，其中共有{}张topic图片，{}张无效图片...'.format(
                time.strftime('%H:%M:%S', time.localtime()), index + 1,
                len(files_4_category[category_no]), num, err_num
            ))

    print('{}处理完成，共有{}张topic图片，{}张无效图片.'.format(dirs_4_category[category_no], num, err_num))


# 处理200*200的图片
for i in range(4):
    del_topic_pics(i)


def recover_some_pics():
    pics = ['4de3cfd3jw1e3z61ria75j204g04g745', '5f8f0430tw1e12oz3wd8dj']
    pass
