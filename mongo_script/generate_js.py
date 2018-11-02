# encoding:utf-8

# 生成js脚本文件
# var c = db.﻿event_ready.find({clue_id : process.argv[2], update:true});
# while(c.hasNext()) {
#     printjsononeline(c.next());
# }

# mongo localhost:27017/NewsCertify dump.js > feed.json

import os

js_path = ''
json_path = './json/'

with open('clues_id.txt', 'r') as src:
    id_list = src.readlines()
    for clue_id in id_list:
        clue_id = clue_id.split()[0]

        # 生成js文件
        js_file = js_path + clue_id + '.js'
        with open(js_file, 'w') as out:
            out.write('var c = db.﻿event_ready.find({clue_id :' + clue_id + ', update:true});\n')
            out.write('while(c.hasNext()) { \n\tprintjsononeline(c.next()); \n}\n')

        # 执行mongo命令，输出json
        json_file = json_path + clue_id + '.json'
        os.system('mongo localhost:27017/NewsCertify {} > {}'.format(js_file, json_file))

        break
