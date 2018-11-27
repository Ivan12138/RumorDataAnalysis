# encoding:utf-8

# ============================ 真实微博：相似文本去重 (Strategy: word2vec) ============================

import json
import Word2VecSinglePassOfContent
import traceback
import time

userServer = True

weibo_file = '../weibo_truth_analysis/file/_sample_weibo_truth.txt'
text_similarity_file = 'file/_sample_text_similarity.txt'
filtered_weibo_file = 'file/_sample_filtered_weibo_truth.txt'
filtered_weibo_file_pretty = 'file/_sample_filtered_weibo_truth_pretty.txt'

if userServer is True:
    weibo_file = '../weibo_truth_analysis/file/weibo_truth.txt'
    text_similarity_file = 'file/text_similarity.txt'
    filtered_weibo_file = 'file/filtered_weibo_truth.txt'
    filtered_weibo_file_pretty = 'file/filtered_weibo_truth_pretty.txt'

log_file = 'file/log.txt'


def main():
    with open(log_file, 'w') as log:
        with open(weibo_file, 'r') as src:
            out_pretty = open(filtered_weibo_file_pretty, 'w')
            out = open(filtered_weibo_file, 'w')

            lines = src.readlines()
            for line in lines:
                try:
                    start_time = time.time()
                    event = json.loads(line)
                    if 'weibo' not in event.keys():
                        continue
                    event_weibos = event['weibo']

                    # 存储微博的属性信息，包括微博内容(content)、图片数(pic_num)、转赞评之和(propagation_num)
                    weibos_dict_list = []
                    for weibo in event_weibos:
                        if not isinstance(weibo, dict):
                            continue

                        content = weibo['content']

                        if 'piclist' in weibo.keys() and isinstance(weibo['piclist'], list):
                            pic_num = len(weibo['piclist'])
                        else:
                            pic_num = 0

                        propagation_num = 0
                        if 'forward' in weibo.keys():
                            try:
                                propagation_num += int(weibo['forward'])
                            except:
                                pass
                        if 'praise' in weibo.keys():
                            try:
                                propagation_num += int(weibo['praise'])
                            except:
                                pass
                        if 'comment' in weibo.keys():
                            try:
                                propagation_num += int(weibo['comment'])
                            except:
                                pass

                        weibos_dict_list.append(
                            {'content': content, 'pic_num': pic_num, 'propagation_num': propagation_num})

                    # 开始进行SinglePass
                    weibos_content_list = [weibos_dict['content'] for weibos_dict in weibos_dict_list]
                    single_pass_clustering = Word2VecSinglePassOfContent.SinglePassClusterOfContent(weibos_content_list)

                    # 保留规则：#1 图片数 #2 转赞评之和
                    reserved_weibos_index = []
                    for cluster_unit in single_pass_clustering.cluster_list:
                        index_list = cluster_unit.node_list
                        reserved_index = index_list[0]
                        for index in index_list[1:]:
                            pic_num_a = weibos_dict_list[index]['pic_num']
                            pic_num_b = weibos_dict_list[reserved_index]['pic_num']
                            if pic_num_a > pic_num_b:
                                reserved_index = index
                            elif pic_num_a == pic_num_b:
                                propagation_num_a = weibos_dict_list[index]['propagation_num']
                                propagation_num_b = weibos_dict_list[reserved_index]['propagation_num']
                                if propagation_num_a > propagation_num_b:
                                    reserved_index = index
                        reserved_weibos_index.append(reserved_index)

                    # 打印聚类结果
                    log.write('[{}] 事件 {}/{} 聚类完成，耗时{:.1f}s，聚类结果：\n'.format(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        lines.index(line) + 1, len(lines), time.time() - start_time))
                    log.write('聚类前共有微博{}条，聚类后有{}条。把结果写入文件...\n'.format(len(event_weibos), len(reserved_weibos_index)))

                    # 将聚类后的结果写入新的文件
                    filtered_event = {'id': event['id'], 'keywords': event['keywords'],
                                      'filtered_weibo': [event_weibos[index] for index in reserved_weibos_index]}

                    out.write('{}\n'.format(json.dumps(filtered_event, ensure_ascii=False)))
                    out_pretty.write(
                        '{}\n'.format(json.dumps(filtered_event, ensure_ascii=False, indent=4, separators=(',', ':'))))

                except:
                    log.write('-------------------------------------------\n')
                    log.write('{}\n'.format(traceback.print_exc()))
                    log.write('-------------------------------------------\n')
                finally:
                    log.flush()
                    out.flush()
                    out_pretty.flush()

            out_pretty.close()
            out.close()


main()
