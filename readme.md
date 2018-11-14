# Rumor Data Analysis

## Data Description

### Statistics

|            类别             |       文件       |   数目统计   |
| :-------------------------: | :--------------: | :----------: |
| **真实微博** - 事件线索数量 | weibo_truth.txt  |     5979     |
|   **真实微博** - 微博数量   |        -         |    154114    |
|   **真实微博** - 图片数量   |    img_truth     | 183831 (41G) |
|                             |                  |              |
|  **谣言微博** -  微博数量   | rumor_weibo.json |    34611     |
|   **谣言微博** - 图片数量   |    img_rumor     | 26586 (845M) |

### Source

- 真实微博：来源于[AI识谣系统](https://www.newsverify.com/)
- 谣言微博：来源于[微博社区管理中心](https://service.account.weibo.com/?type=5&status=4)

## Feature Engineering

### Overview

- [真实微博](https://github.com/RMSnow/RumorDataAnalysis/blob/master/weibo_truth_analysis/TruthAnalysis.ipynb)
- [谣言微博](https://github.com/RMSnow/RumorDataAnalysis/blob/master/weibo_rumor_analysis/RumorAnalysis.ipynb)

### References

- [seaborn](https://seaborn.pydata.org/tutorial.html)

## Pictures Filtering

### SIFT

- SIFT原理：[OpenCV-Python教程:36.SIFT（尺度不变特征变换）](https://www.jianshu.com/p/c0379c931e74)

### Dependency

- python == 3.5
- pip install **opencv-contrib-python**==**3.3**.1.11

### References

- [相似图片检测系统的搭建](https://juejin.im/post/59e7101a51882521ad0f3bfa)
- [图像检索：BoW图像检索原理与实战](https://yongyuan.name/blog/CBIR-BoW-for-image-retrieval-and-practice.html)