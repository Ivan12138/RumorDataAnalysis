# encoding:utf-8
import os
import matplotlib.pyplot as plt
from sklearn.externals import joblib

import SinglePass


# 获取各个事件中的图片
def get_pics_of_event():
    path = '../pic_filtering_phash/clustering'
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if '.jpg' in file_path:
                images.append(file_path)

    return images


events_id = ['B4344055DFF83CC9E409148781C675FC1462253821989', '04C1CE33DFEDE89DFDAFB00D2C7F49E51467841215809',
             'BE9E022D9F145539DE139A0081F6C0A11475173120114', '9D28A3577411682499450EB5DCC4F8111475151757776',
             'D5BC29F8B211769AE7E036F83A0C74E01462102720442', 'C54C036D3E6D32CE6B3130BA6374A0DB1474855155064']


# 查看如何调整阈值
def see_how_to_tune_threshold(event_id, images):
    im_features, image_paths, idf, numWords, voc = joblib.load("pkl/{}.pkl".format(event_id))

    # Get sorted_index of Images
    path = os.path.join('../pic_filtering_phash/clustering', event_id)
    im_index = [image_paths.index(os.path.join(path, i)) for i in images]

    # Plot
    for i in im_index:
        for j in im_index:
            plt.figure(figsize=(12, 4))

            plt.subplot(1, 2, 1)
            plt.imshow(plt.imread(image_paths[i]))
            plt.title('{:.3f}'.format(SinglePass.cosine_similarity(im_features[i], im_features[j])))
            plt.axis('off')

            plt.subplot(1, 2, 2)
            plt.imshow(plt.imread(image_paths[j]))
            plt.axis('off')


def show_images(event_id, images, nb_rows=3, nb_cols=4):
    path = os.path.join('../pic_filtering_phash/clustering', event_id)

    plt.figure(figsize=(15, 15))
    for k in range(nb_rows * nb_cols):
        plt.subplot(nb_rows, nb_cols, k + 1)
        plt.imshow(plt.imread(os.path.join(path, images[k])))
        plt.axis('off')
