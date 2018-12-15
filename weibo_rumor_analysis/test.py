# encoding:utf-8

import json

src_file = 'file/rumor_weibo_updated.json'
out_file = 'file/rumor_weibo_updated_pretty.json'

with open(src_file, 'r') as src:
    with open(out_file, 'w') as out:
        lines = src.readlines()
        for line in lines:
            js = json.loads(line, encoding='utf-8')
            out.write('{}\n'.format(
                json.dumps(js, ensure_ascii=False, indent=4, separators=(',', ':'))))
