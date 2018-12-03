# Rumor Data Analysis

## Overview

### Project Structure

|   Category   |         Dir          |       Description        |
| :----------: | :------------------: | :----------------------: |
| **数据分析** | weibo_rumor_analysis |                          |
|              | weibo_truth_analysis |                          |
| **图片过滤** | pic_filtering_phash  | 基于**phash**的图片过滤  |
|              |  pic_filtering_sift  |  基于**SIFT**的图片过滤  |
| **文本过滤** |    text_filtering    | 基于**tf-idf**的文本过滤 |
|   **采样**   |       sampling       |                          |

### Dataset

|            名称             | 标签 |        处理过程         | 微博数 | 图片数 |                           文本文件                           |          图片文件          |
| :-------------------------: | :--: | :---------------------: | :----: | :----: | :----------------------------------------------------------: | :------------------------: |
| **多模态数据集(文本+图片)** | 谣言 |      **文本去重**       |  7880  | 10773  | `file/weibo_rumor_text_filtered.json`<br />`file/weibo_rumor_text_filtered_pretty.json` | `text_filtered_img_rumor/` |
|                             | 真实 | **文本去重 + 文本采样** |  7909  | 16367  | `sampling/file/weibo_truth_sampling.json`<br />`sampling/file/weibo_truth_sampling_pretty.json` | `text_filtered_img_truth/` |
|       **图片数据集**        | 谣言 |      **图片去重**       |   -    | 21963  |                              -                               | `pics_filtered_img_rumor/` |
|                             | 真实 |      **图片采样**       |   -    | 22304  |                              -                               | `pics_sampling_img_truth/` |

### 处理流程

|              |   类别   | (1)原始数据 | (2.1)对(1)的文本去重 | (2.2)对(2.1)进行样本均衡 | (3.1)对(1)的图片去重 | (3.2)对(3.1)进行样本均衡 |
| :----------: | :------: | :---------: | :------------------: | :----------------------: | :------------------: | :----------------------: |
| **真实微博** | **文本** |   154114    |        38180         |           7909           |          -           |            -             |
|              | **图片** |   183831    |        82058         |          16660           | 183831<br />(未处理) |          21963           |
| **谣言微博** | **文本** |    34611    |         7880         |           7880           |          -           |            -             |
|              | **图片** |    26586    |        11937         |          11937           |        21963         |          21963           |
|   **备注**   |          |             |  **采用TF-IDF去重**  |                          |   **采用SIFT去重**   |                          |

#### 备注

1. 流程(1)：原始数据

   - 真实微博：来源于[AI识谣系统](https://www.newsverify.com/)
     - 在`newsclues_ready`表中筛选`label:'truth'`且类别不在`'军事','娱乐'`中的事件(选出5979个事件id)
     - 通过事件id，在`event_ready`表中查找对应的`truth`微博，共154114条
   - 谣言微博：来源于[微博社区管理中心](https://service.account.weibo.com/?type=5&status=4)
     - 爬取事件`2018-11-08 01:51`之前的所有结果，共34611条

2. 流程(2.1)：文本去重

   - 在流程**(1)**的基础上进一步处理

   - 采用TF-IDF进行相似性判定(库依赖：`sklearn.feature_extraction.text.TfidfTransformer`)

   - 聚类结果：`text_filtering/file/clustering/`文件夹中，`rumor_4000.txt`、`truth_[NUM].txt`等

   - 去重原则：

     谣言微博

     - 尽量选取图片数多的微博
     - 图片数相同时，选取**转赞评**多的微博

     真实微博

     - 随机选取**有图片**的微博

3. 流程(2.2)：样本均衡

   - 在流程**(2.1)**的基础上进一步处理
   - 采样原则：
     - 保证事件间的微博数量比例不变
     - 保证`userCertify`的分布与谣言微博相同

4. 流程(3.1)：图片去重

   - 在流程**(1)**的基础上进一步处理
   - 利用SIFT提取局部特征，进行相似性判定

5. 流程(3.2)：样本均衡

   - 在流程**(3.1)**的基础上进一步处理
   - 采样原则：保证事件间的图片数量比例不变

## Original Data Description

### Statistics

|            类别             |                         文件                         |   数目统计   |
| :-------------------------: | :--------------------------------------------------: | :----------: |
| **真实微博** - 事件线索数量 |     `weibo_truth_analysis/file/weibo_truth.txt`      |     5979     |
|   **真实微博** - 微博数量   |                          -                           |    154114    |
|   **真实微博** - 图片数量   |                   `raw_img_truth/`                   | 183831 (41G) |
|                             |                                                      |              |
|  **谣言微博** -  微博数量   | `weibo_rumor_analysis/file/rumor_weibo_updated.json` |    34611     |
|   **谣言微博** - 图片数量   |                   `raw_img_rumor/`                   | 26586 (845M) |

### Source

- 真实微博：来源于[AI识谣系统](https://www.newsverify.com/)
- 谣言微博：来源于[微博社区管理中心](https://service.account.weibo.com/?type=5&status=4)

## Feature Engineering

### Overview

- [真实微博](https://github.com/RMSnow/RumorDataAnalysis/blob/master/weibo_truth_analysis/TruthAnalysis.ipynb)
- [谣言微博](https://github.com/RMSnow/RumorDataAnalysis/blob/master/weibo_rumor_analysis/RumorAnalysis.ipynb)

### References

- [seaborn](https://seaborn.pydata.org/tutorial.html)

