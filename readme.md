# Crawler

|          文件           |   数目统计   |
| :---------------------: | :----------: |
|       clue_id.txt       |     5979     |
| weibo_truth_unicode.txt |     5979     |
|     weibo_truth.txt     |     5979     |
|      **图片数量**       | **数目统计** |
|        pic_lists        |    203957    |
|      unique images      |    184528    |
|      **爬取结果**       | **数目统计** |
|           img           | 97230 (20G)  |
|        img_twice        | 86899 (22G)  |
|           err           |      64      |
|         **img**         | 183831 (41G) |

爬虫耗时：10h + 13h

2018-11-02 17:06:14 ～ 2018-11-03 03:10:25

2018-11-06 16:07:12 ～ 2018-11-07 05:25:12

## MongoDB Cmd

```
db.getCollection('newsclues_ready').find({label:"truth", category:{$nin:["军事", "娱乐"]}}).sort({timestamp:-1})
db.getCollection('event_ready').find({clue_id:"87b620c2f8aedb60f999f93950c8ac80", update:true})

db.getCollection('event_ready').find({weibo:{$elemMatch:{userCertify:2}}}).sort({timestamp:-1}).limit(10)

db.getCollection('event_ready').find({timestamp:{$gt:1539458594654}}).sort({timestamp:-1}).count()


﻿// db.getCollection('judgeWeibo').find({'reportedWeibo.userCertify' : 2})

// 查询reportedUser
// db.getCollection('judgeWeibo').find({'reportedUser' : {$exists: false}})

// 查询reportedWeibo
// db.getCollection('judgeWeibo').find({'reportedWeibo.userCertify' : {$exists: false}})
// db.getCollection('judgeWeibo').find({'reportedWeibo' : {$type: 'object'}, 'reportedWeibo.piclists' : {$exists: false}})

// 全量数据
db.getCollection('judgeWeibo').find()

```

# Pics Filtering

## SIFT

open-cv版本：

pip install opencv-contrib-python==3.3.1.11

# Linux Cmd

- ls img_rumor -lR |grep "^-"|wc -l
- nohup