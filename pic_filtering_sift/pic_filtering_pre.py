# encoding:utf-8

import json
import os

import BoW

rumor_src_file = '../text_filtering/file/weibo_rumor_text_filtered.json'
truth_src_file = '../sampling/file/weibo_truth_sampling.json'
rumor_out_file = 'file/rumor_pics.txt'
truth_out_file = 'file/truth_pics.txt'


def get_pics_file():
    with open(rumor_src_file, 'r') as src:
        with open(rumor_out_file, 'w') as out:
            lines = src.readlines()
            for line in lines:
                rumor = json.loads(line, encoding='utf-8')
                pic_lists = rumor['reportedWeibo']['piclists']
                for pic in pic_lists:
                    out.write('{}\n'.format(pic.split('/')[-1]))

    with open(truth_src_file, 'r') as src:
        with open(truth_out_file, 'w') as out:
            lines = src.readlines()
            for line in lines:
                event = json.loads(line, encoding='utf-8')
                weibos = event['weibo']
                for weibo in weibos:
                    pic_lists = weibo['piclist']
                    for pic in pic_lists:
                        out.write('{}\n'.format(pic.split('/')[-1]))


def cp_script():
    root_dir = '/media/Data/qipeng/modified_complete_images/crawler'
    rumor_src_dir = os.path.join(root_dir, 'raw_img_rumor')
    rumor_out_dir = os.path.join(root_dir, 'sampling_img_rumor')
    truth_src_dir = os.path.join(root_dir, 'raw_img_truth')
    truth_out_dir = os.path.join(root_dir, 'sampling_img_truth')

    # rumor
    valid_pics_num = 0
    with open(rumor_out_file, 'r') as src:
        with open('file/valid_rumor_pics.txt', 'w') as out:
            lines = src.readlines()
            for pic in lines:
                pic_path = os.path.join(rumor_src_dir, pic.strip('\n'))
                cmd = 'cp {} {}'.format(pic_path, rumor_out_dir)
                code = os.system(cmd)
                if code == 0:
                    valid_pics_num += 1
                    out.write(pic)
    print('有效的rumor_pics为{}张'.format(valid_pics_num))

    # truth
    valid_pics_num = 0
    with open(truth_out_file, 'r') as src:
        with open('file/valid_truth_pics.txt', 'w') as out:
            lines = src.readlines()
            for pic in lines:
                pic_path = os.path.join(truth_src_dir, pic.strip('\n'))
                cmd = 'cp {} {}'.format(pic_path, truth_out_dir)
                code = os.system(cmd)
                if code == 0:
                    valid_pics_num += 1
                    out.write(pic)
    print('有效的truth_pics为{}张'.format(valid_pics_num))


def get_descriptors():
    # Rumor
    # with open('file/sampling_pics_rumor.txt', 'r') as src:
    #     lines = src.readlines()
    # image_paths = ['../../sampling_img_rumor/' + line.strip('\n') for line in lines]
    # BoW.get_descriptors_list('rumor', image_paths)

    # Truth
    with open('file/sampling_pics_truth.txt', 'r') as src:
        lines = src.readlines()
    image_paths = ['../../sampling_img_truth/' + line.strip('\n') for line in lines]
    BoW.get_descriptors_list('truth', image_paths)


get_descriptors()
