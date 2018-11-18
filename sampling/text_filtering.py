# encoding:utf-8

# ============================ 真实微博：相似文本去重 ============================

import synonyms
import json

weibo_file = '../weibo_truth_analysis/file/_sample_weibo_truth.txt'
text_similarity_file = 'file/_sample_text_similarity.txt'


def show_threshold():
    with open(weibo_file, 'r') as src:
        with open(text_similarity_file, 'w') as out:
            lines = src.readlines()
            for line in lines:
                event = json.loads(line)
                event_weibos = event['weibo']
                contents = []
                for weibo in event_weibos:
                    contents.append(weibo['content'])

                for index_x, content_x in enumerate(contents):
                    for index_y, content_y in enumerate(contents):
                        if index_x != index_y:
                            similarity = synonyms.compare(content_x, content_y)
                            out.write('{}\n{}\n{}\n\n'.format(content_x, content_y, similarity))


def test():
    sen1 = '\n\t\t【5大主题高铁春游线路饱览最美春色】2016年春游期间，上海铁路局开行图定旅客列车总对数达772.5对，较去年同比增加84.5对;其中高铁动车组列车为518.5对，较去年同比增加81对。特点：上海、杭州、南京至上饶(三清山)、武夷山等地二日往返(合福高铁赣闽段) （分享自 @凤凰网） http://t.cn/Rqhv0n3\n\t\t'
    sen2 = '\n\t\t本周五《我是歌手》第四季“歌王之战”总决赛帮帮唱阵容出炉↓↓↓@CoCo李玟 &amp;Ne-Yo@張信哲JeffChang &amp;Akon@李克勤 &amp;#林子祥##叶倩文# @容祖儿 &amp;@William威廉陈伟霆 @徐佳瑩 &amp;@林俊杰 @黄致列HCY &amp;Gummy朴志妍\n\t\t\t...展开全文c\n\t\t'
    sen3 = '山东,济宁学院大一男生因分手问题将女友捅死 两人均19岁 http://t.cn/RGD99DC'
    sen4 = '正在图书馆一惊一乍的看这些恐怖电影解析，突然听到图书管理员跟男盆友打电话说济宁学院一个男生把前女友捅死后若无其事的回宿舍吃薯条打游戏可怕'
    print(synonyms.compare(sen3, sen4))


# show_threshold()
test()
