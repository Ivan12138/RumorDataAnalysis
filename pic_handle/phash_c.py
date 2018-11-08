# encoding:utf-8

import imagehash
from PIL import Image

path = 'sample/'


def is_similarity(file1, file2, threshold=0.5):
    hash1 = imagehash.phash(Image.open(path + file1))
    hash2 = imagehash.phash(Image.open(path + file2))
    similarity = 1 - (hash1 - hash2) / len(hash1.hash) ** 2
    print('{}: Similarity between {} and {} is {}.'.format(similarity >= threshold, file1, file2, similarity))
    return similarity >= threshold


is_similarity('pic1.jpg', 'pic4.jpg')
