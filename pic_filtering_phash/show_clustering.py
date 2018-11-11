# encoding:utf-8
import json
import os

clustered_31 = ['7cd4f999jw1f3a4dk0x3xj20k00f0jst.jpg', '62bfcf76gw1f3bc9qyobqg208r04ye82.gif',
                '4e5b54d8gw1f3bke7g7x6g208r04y1ky.gif', 'c0855202jw1f3a51n9lzoj20dt09tabe.jpg',
                '9e5389bbjw1f3bhv9ccd0g208r04yqv7.gif', '6379d5b0gw1f3b49je2iuj20b40d8gmb.jpg',
                '736f0c7ejw1f3bb39q8n7j20nq0dcjtj.jpg', '62bfcf76gw1f3ad8pjproj20b40d83zw.jpg']
clustered_32 = ['72d63766gw1f3dteh48azj20hs0vkn0i.jpg', '684ebae3jw1f3dmz6baclj20ax06074f.jpg',
                '6ac50c69jw1f3erjefwyoj20hb0qndis.jpg', '6e916bdegw1f3dq8qrtckj20hm0ef0u5.jpg',
                '005D4gq0gw1f3dlgg18bkj30hs0vk77h.jpg', '8f9dc803jw1f3en5ttja2j20h80q3774.jpg']
clustered_33 = ['63207a53jw1f5ho55vra2j20c80g7jsa.jpg', '4d355e80jw1f5gtmlb9izj20k00qowhw.jpg',
                '5fd734e4jw1f5hmpc5k29j20go0b43zm.jpg', '006fhfuwjw1f5jclamox5j30c80g9gmp.jpg',
                'e4ba8981jw1f5hvk0en3hj20c80g9gmp.jpg', '8cd8e608gw1f5hskw2tosj20j60pk0xs.jpg',
                '67dd74e0gw1f5ib4aacc8j20j60npaed.jpg', 'c2556596jw1f5j6iz016uj20cd3et7hj.jpg',
                '9b76532djw1f5hnefe8epj20j60pkn28.jpg', '56e9a168jw1f5hzfyopejj20j60pkq80.jpg',
                '62b963a9gw1f5hzeswgh3j20dw0iizlo.jpg', '7f1c1c22gw1f5ibrkl521j20dm0f0q4f.jpg',
                'db3b4907jw1f5j1rzp4f7j20cd3etnf4.jpg']
clustered_51 = ['652f5916gw1f85odypvc3j20c80jujsx.jpg', '517fd2acgw1f84rorugt9j20qo0qotbh.jpg',
                'ad194221jw1f83n1eefp8j20qx0qoq8h.jpg', 'b9a15f9djw1f84tjc30xpj20ea0ea3z5.jpg',
                '006mXsPYgw1f851omrgjmj30k00uw76w.jpg', '66b630bfgw1f85r4ljqmpj20c80lp415.jpg',
                '4b8a01b7jw1f852yolr48j20qo1be102.jpg', '738b85begw1f85ynf2h19j20c80lpacp.jpg',
                'a716fd45jw1f84whaa8w0j20fa0esq5a.jpg', '78221efbgw1f83qvaipyij20ku112n2p.jpg',
                'a716fd45jw1f84wha9akij20c80jf773.jpg', '78221efbgw1f83qvbaczrj20ku112q9f.jpg',
                '66b630bfgw1f85r4lkde1j20c80jfq5f.jpg', '80e5c22ejw1f85xjakiilj20ck0c5wfx.jpg',
                '80e5c22ejw1f85xjauw63j20c80jfacj.jpg']
clustered_52 = ['486f6b64gw1f86qfjdn2lj20dw09875g.jpg', '692aad1bgw1f871sqoj7uj20ez0az75l.jpg',
                '6b658c6bjw1f8auph0e4aj20i80c8gmn.jpg', '6204ece1gw1f86t90mgodj20f00d2myl.jpg',
                '486f6b64gw1f86qhig46ag20ah05n7ks.gif', '9e5389bbjw1f8aqizwuynj20i80c80tq.jpg',
                '005u8wFGjw1f8ax4ixekwj30hs0dc3yu.jpg', '486f6b64gw1f86qg7osjgj20dw07swey.jpg']
clustered_53 = ['be66262fgw1f860j0nxusj21be0qotek.jpg', '8e989a9cjw1f84spug1lij20ws0wx76z.jpg',
                '8e989a9cjw1f84sptpif7j20ww0wntbj.jpg', '005VEqiNjw1f886c34pm1j30hp0bnmyx.jpg',
                '9dcea99bjw1f85riid1m3j20e009r3z5.jpg', 'e7592aa5gw1f84uj41jfsj20go0m8gmq.jpg',
                'a716fd45jw1f6tbuu2ypaj20hs1y3n85.jpg', 'be66262fgw1f860j4aqm4j20qo1bhk0v.jpg',
                '488877fcgw1f84abi4pg7j20j60iywgm.jpg', '488877fcgw1f84abgywboj20j60j576l.jpg',
                '81c10930jw1f83drcwncbj20qo0hota0.jpg']
clustered_pic_list = [clustered_31, clustered_32, clustered_33, clustered_51, clustered_52, clustered_53]

with open('../mongo_script/file/weibo_truth.txt', 'r') as src:
    lines = src.readlines()
    json_31 = json.loads(lines[30])
    json_32 = json.loads(lines[31])
    json_33 = json.loads(lines[32])
    json_51 = json.loads(lines[50])
    json_52 = json.loads(lines[51])
    json_53 = json.loads(lines[52])
json_list = [json_31, json_32, json_33, json_51, json_52, json_53]

for event_json in json_list:
    event_id = event_json['id']
    event_weibo_list = event_json['weibo']
    event_pics = []

    # 提取事件中的图片
    for weibo_dict in event_weibo_list:
        if 'piclist' in weibo_dict.keys():
            curr_pics = weibo_dict['piclist']
            if curr_pics is not None:
                for curr_pic in curr_pics:
                    event_pics.append(curr_pic.split('/')[-1])

    event_pics = list(set(event_pics))

    des_dir = '../show_filtering'
    src_dir = '../img/'

    # 聚类之前的图片
    for pic in event_pics:
        src_file = src_dir + pic
        des_file = des_dir + '{}-'.format(json_list.index(event_json)) + pic
        os.system('cp {} {}'.format(src_file, des_file))

    # 聚类之后的图片
    for pic in clustered_pic_list[json_list.index(event_json)]:
        src_file = src_dir + '1-' + pic
        des_file = des_dir + '1-' + pic
        os.system('expect scp.sh ' + src_file + ' ' + des_file)

    print('----------------')
