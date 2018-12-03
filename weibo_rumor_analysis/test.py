# encoding:utf-8

import json

file = 'file/rumor_weibo_updated.json'

reportTime = []
with open(file, 'r') as src:
    lines = src.readlines()
    for line in lines:
        rumor = json.loads(line, encoding='utf-8')
        if rumor['reportTime'] != '':
            reportTime.append(rumor['reportTime'])

sz = len(reportTime)

# print(reportTime[:10])
# print(reportTime[sz-10:])
# print('-----------------------------------------')

reportTime.sort()
print(reportTime[:10])
print(reportTime[sz - 10:])
print()

with open(file, 'r') as src:
    lines = src.readlines()
    for line in lines:
        rumor = json.loads(line, encoding='utf-8')
        if rumor['reportTime'] == reportTime[-1]:
            print(rumor)