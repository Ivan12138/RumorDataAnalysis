# Crawler

|                         |        |      |
| ----------------------- | ------ | ---- |
| clue_id.txt             | 5979   |      |
| weibo_truth_unicode.txt | 5979   |      |
|                         |        |      |
| pic_lists               | 203957 |      |
| unique images           | 184528 |      |

[qipeng@localhost crawler-truth]$ nohup python3.5 crawler.py >> log2.txt &
[1] 159765
[qipeng@localhost crawler-truth]$ nohup: ignoring input and redirecting stderr to stdout

# MongoDB Cmd

﻿db.getCollection('newsclues_ready').find({label:"truth", category:{$nin:["军事", "娱乐"]}}).sort({timestamp:-1})
﻿db.getCollection('event_ready').find({clue_id:"87b620c2f8aedb60f999f93950c8ac80", update:true})

﻿db.getCollection('event_ready').find({weibo:{$elemMatch:{userCertify:2}}}).sort({timestamp:-1}).limit(10)

﻿db.getCollection('event_ready').find({timestamp:{$gt:﻿1539458594654}}).sort({timestamp:-1}).count()