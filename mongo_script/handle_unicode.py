# encoding:utf-8

import json

file = 'weibo_truth_unicode.txt'

with open(file, 'r') as src:
    with open('weibo_truth_pretty.txt', 'w') as out:
        lines = src.readlines()
        for line in lines:
            weibo_json = json.loads(line)
            out.write(json.dumps(weibo_json, ensure_ascii=False, indent=4, separators=(',', ':')))
            # break
