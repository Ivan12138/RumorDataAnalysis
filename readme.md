|                         |        |      |
| ----------------------- | ------ | ---- |
| clue_id.txt             | 5979   |      |
| weibo_truth_unicode.txt | 5979   |      |
|                         |        |      |
| pic_lists               | 203957 |      |
| unique images           | 184528 |      |


﻿db.getCollection('newsclues_ready').find({label:"truth", category:{$nin:["军事", "娱乐"]}}).sort({timestamp:-1})
﻿db.getCollection('event_ready').find({clue_id:"87b620c2f8aedb60f999f93950c8ac80", update:true})