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
| **多模态数据集(文本+图片)** | 谣言 |      **文本去重**       |  7880  | 10371  | `text/filtering/file/weibo_rumor_text_filtered.json`<br />`text/filtering/file/weibo_rumor_text_filtered_pretty.json` | `text_filtered_img_rumor/` |
|                             | 真实 | **文本去重 + 文本采样** |  7909  | 16105  | `sampling/file/weibo_truth_sampling.json`<br />`sampling/file/weibo_truth_sampling_pretty.json` | `text_filtered_img_truth/` |
|       **图片数据集**        | 谣言 |      **图片去重**       |   -    | 17588  |                              -                               | `pics_filtered_img_rumor/` |
|                             | 真实 |      **图片采样**       |   -    | 17716  |                              -                               | `pics_sampling_img_truth/` |

### 处理流程

|              |   类别   | (1)原始数据 | (2.1)对(1)的文本去重 | (2.2)对(2.1)进行样本均衡 | (2.3))删去(2.2)的topic图片 | (3.1)对(1)的图片去重 | (3.2)对(3.1)进行样本均衡 | (3.3)删去(3.2)的topic图片，并再去重 |
| :----------: | :------: | :---------: | :------------------: | :----------------------: | :------------------------: | :------------------: | :----------------------: | :---------------------------------: |
| **真实微博** | **文本** |   154114    |        38180         |           7909           |            7909            |          -           |            -             |                  -                  |
|              | **图片** |   183831    |        82058         |          16660           |           16083            | 183831<br />(未处理) |          22304           |                17716                |
| **谣言微博** | **文本** |    34611    |         7880         |           7880           |            7880            |          -           |            -             |                  -                  |
|              | **图片** |    26586    |        11937         |          11937           |           10310            |        21963         |          21963           |                17588                |
|   **备注**   |          |             |  **采用TF-IDF去重**  |                          |                            |   **采用SIFT去重**   |                          |          **采用pHash去重**          |

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

4. 流程(2.3)：去掉微博数据爬虫中残留的“话题”图片

   - 话题图片的尺寸：`160*160`，`180*180`，`200*200`

5. 流程(3.1)：图片去重

   - 在流程**(1)**的基础上进一步处理
   - 利用SIFT提取局部特征，进行相似性判定

6. 流程(3.2)：样本均衡

   - 在流程**(3.1)**的基础上进一步处理
   - 采样原则：保证事件间的图片数量比例不变

7. 流程(3.3)

   - 话题图片过滤
   - phash的二次去重
   - truth图片的随机采样

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

## Text Filtering 

### 过滤原则

#### 谣言微博

- 尽量选取图片数多的微博
- 图片数相同时，选取**转赞评**多的微博

#### 真实微博

- 随机选取**有图片**的微博

### 过滤结果
|                   |        微博数量        | 图片数量  |               userCertify 分布                |
| :---------------: | :--------------------: | :-------: | :-------------------------------------------: |
|     谣言微博      |         34611          |   26586   |       （27916）22745:4148:1023 = 22:4:1       |
|   **过滤结果**    |        **7880**        | **11937** |  **（5942）4439:1284:219 = 20.3 : 5.9 : 1**   |
|                   |                        |           |                                               |
|     真实微博      |         158299         |  183831   |      （154114）60646:24750:68718 = 5:2:5      |
|   **直接过滤**    |     57268（36827）     |   79076   |   （36827）13967:6581:16279 = 2.1 : 1 : 2.5   |
|    **4折过滤**    | 8482 + 4148（无图片）  |           |                                               |
|                   | 8715 + 4827（无图片）  |           |                                               |
|                   | 11088 + 4905（无图片） |           |                                               |
|                   | 9895 + 7162（无图片）  |           |                                               |
|                   |       **38180**        | **82058** | **（38180）14396:6724:17060 = 2.1 : 1 : 2.5** |
| **4折 - 2次过滤** |         35256          |   75967   |   （35256）13414:6168:15674 = 2.2 : 1 : 2.5   |

### 附：参数文件说明

|     类别      | 文件名                                      | 说明                                                         |         参数          |
| :-----------: | :------------------------------------------ | :----------------------------------------------------------- | :-------------------: |
|  **语料库**   | `file/corpus/corpus_of_rumor.txt`           | 所有谣言微博的内容集合。通过**行号**对应微博的索引           |           -           |
|               | `file/corpus/corpus_of_truth.txt`           | 所有真实微博的内容集合，其中**前缀(a,b)** 对应 (事件的索引,微博的索引) |           -           |
|               | `file/corpus/cut_corpus_of_rumor`           | 分词后的谣言微博语料库                                       |           -           |
|               | `file/corpus/cut_corpus_of_truth.txt`       | 分词后的真实微博语料库                                       |           -           |
| **tf_idf 值** | `file/pkl/tf_idf_rumor.pkl`                 | 词表中保留全部词                                             | `vocabulary, tf_idf`  |
|               | `file/pkl/tf_idf_rumor_4000.pkl`            | 词表中保留词频最高的4000词 (max_features)                    | `vocabulary, tf_idf`  |
|               | `file/pkl/tf_idf_truth_4000.pkl`            | 词表中保留词频最高的4000词 (max_features)                    | `vocabulary, tf_idf`  |
| **聚类结果**  | `file/pkl/tf_idf_[CATEGORY]_clustering.pkl` | `[CATEGORY]`可为`rumor`,`truth`, `rumor_test`, `truth_test`等 | `single_pass_cluster` |

## Sampling of Truth Weibos

### 采样原则

- 保证事件的微博数量比例
- 保证`userCertify`的分布与谣言微博相同

### 采样结果

#### 不进行文本过滤

|              |         微博数量         | 图片数量 |            userCertify 分布             |
| :----------: | :----------------------: | :------: | :-------------------------------------: |
|   谣言微博   |          34611           |  26586   |    （27916）22745:4148:1023 = 22:4:1    |
|   真实微博   | 158299（来自5979个事件） |  183831  |   （154114）60646:24750:68718 = 5:2:5   |
|              |                          |          |                                         |
| **采样结果** |          35358           |  38550   | （35358）= 29209:4857:1292 = 22.6:3.8:1 |

#### 进行文本过滤

|                         | 微博数量 | 图片数量 |             userCertify 分布              |
| :---------------------: | :------: | :------: | :---------------------------------------: |
|        谣言微博         |   7880   |  11937   |  （5942）4439:1284:219 = 20.3 : 5.9 : 1   |
|        真实微博         |  38180   |  82058   | （38180）14396:6724:17060 = 2.1 : 1 : 2.5 |
|                         |          |          |                                           |
| **真实微博 - 采样结果** |   7909   |  16660   |   (7909）5892:1723:294 = 20.0 : 5.9 : 1   |

### 附：参数文件说明

| 文件名                                    |         说明         | 参数                                                         |
| :---------------------------------------- | :------------------: | :----------------------------------------------------------- |
| `file/pkl/event_features.pkl`             |  真实微博的事件特性  | `event_features_list`                                        |
| `file/pkl/event_sampling_factor.pkl`      |       取样因子       | `events_num, weibos_num, event_weibos_num_list, global_sampling_factor, event_sampling_factor_list` |
| `file/pkl/certify_num_of_every_event.pkl` | 每个事件的需取样情况 | `sampling_num_of_event, certify_num_of_event`                |
| `file/pkl/result.pkl`                     |  每个事件的取样结果  | `certify_num_of_event, result_index_of_event`                |

## Pictures Filtering

### SIFT

- SIFT原理：[OpenCV-Python教程:36.SIFT(尺度不变特征变换)](https://www.jianshu.com/p/c0379c931e74)

### Dependency

- python == 3.5
- pip install **opencv-contrib-python**==**3.3**.1.11

### 过滤结果

#### 在文本过滤的基础上

|          | 微博数量 |           userCertify 分布           |   图片数量   | 过滤后 |
| :------: | :------: | :----------------------------------: | :----------: | :----: |
| 谣言微博 |   7880   | (5942)4439:1284:219 = 20.3 : 5.9 : 1 | (11937)10773 |   -    |
| 真实微博 |   7909   | (7909)5892:1723:294 = 20.0 : 5.9 : 1 | (16660)16367 |   -    |

#### 全量的Rumor图片

|          |    图片数量    | 过滤后 |
| :------: | :------------: | :----: |
| 谣言微博 |  26586   | 21963 |
| 真实微博**（采样）** |  183831  |22304|

### References

- [相似图片检测系统的搭建](https://juejin.im/post/59e7101a51882521ad0f3bfa)
- [图像检索：BoW图像检索原理与实战](https://yongyuan.name/blog/CBIR-BoW-for-image-retrieval-and-practice.html)
- [基于感知哈希算法的视觉目标跟踪](https://blog.csdn.net/zouxy09/article/details/17471401)

