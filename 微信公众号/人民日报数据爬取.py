# -*- coding: utf-8 -*-  python 3.12
# @Time    : 2025/9/23
# @Desc    : 爬取人民日报微信公众号数据
# @Author  : laity
# @Contact : 微信公众号：laity的渗透测试之路




import requests
import json
from time import sleep
import time
import parsel
import csv
import os


class FetchData:
    def __init__(self):
        self.cookies = {
            'appmsglist_action_3937507372': 'card',
            'RK': 'HLf13ZN/48',
            'ptcz': '8aa06e9b742da4ea6b0dea3ab898973185470dcbd30c19e5a118121cb7eb03b2',
            'pgv_pvid': '8853584578',
            'pac_uid': '0_TW3fwxP6xFG9P',
            '_qimei_uuid42': '1951e101f3a100dca057f7e4cf958d81f3fa6f6ae6',
            '_qimei_fingerprint': '9eea1b61b578da6d51064297e4c56a75',
            '_qimei_h38': '8f95452ca057f7e4cf958d810200000b11951e',
            '_qimei_q32': 'ae202252c280736fb099d1bff3886c4a',
            '_qimei_q36': '2542e4b62d5928e2bb5fb78d30001c11941c',
            'omgid': '0_TW3fwxP6xFG9P',
            'ua_id': 'WEBe6MXDSBblB0f7AAAAAM2o2LWQ7JqJwahzPh8_1Sc=',
            'wxuin': '50312903643481',
            'mm_lang': 'zh_CN',
            'yyb_muid': '0CE8650EBEBF603A256B70D0BFD261B6',
            '_qimei_i_3': '2ce05380c65e56dfc397fa36598127b3ffebf0f3160e07d7e58e7d5873c2723d353134943c89e286a89f',
            'uin': 'null',
            'skey': 'null',
            'luin': 'null',
            'lskey': 'null',
            'user_id': 'null',
            'session_id': 'null',
            'rewardsn': '',
            'wxtokenkey': '777',
            '_clck': '3937507372|1|fzk|0',
            'uuid': 'c61fb26a4914cef6a3a524b1368ed06a',
            'rand_info': 'CAESIF1BR+ZfpYA20ltan5JvVR4DEawSM8oWgco0weL+CAs9',
            'slave_bizuin': '3937507372',
            'data_bizuin': '3937507372',
            'bizuin': '3937507372',
            'data_ticket': 'hkHVkmlHB6ESmFlT+2Z26kpmSxqf6bEeBk7ZJZdr4dNBfhSsVVnPHIyVad/j8t6q',
            'slave_sid': 'dmZSdDU3VTRYNEM4VndQYnBZX1ZPbFRmWlBQWXh1S1FwNGd1OUNzdmZBT3NObF9RTjZxT2tWWHVObTh0dFhkaHJoY2RJSjhuTHh4Y19FTEdaTUVpUldiNENfY2d5WjI0a2JocV9xbTk4UlZ3d1BTd3RpOEhiRndpODRONHNOTnRET0FaRVlocWdET3VTZkpM',
            'slave_user': 'gh_0cee669cba87',
            'xid': '52b40ea9c5139fa976056bc013825b65',
            '_clsk': '1o2q7st|1758593517465|5|1|mp.weixin.qq.com/weheat-agent/payload/record',
        }

        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'priority': 'u=1, i',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=0&token=1186604474&lang=zh_CN&timestamp=1758512686251',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.params = {
            'sub': 'list',
            'search_field': 'null',
            'begin': '1',
            'count': '5',
            'query': '',
            'fakeid': 'MjM5MjAxNDM4MA==',
            'type': '101_1',
            'free_publish_type': '1',
            'sub_action': 'list_ex',
            'fingerprint': '47d72002763c00ef44e7b3eaef4a3767',
            'token': 'xxx',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        self.url = 'https://mp.weixin.qq.com/cgi-bin/appmsgpublish'
        self.filename = 'articles.csv'
        self.fieldnames = ['title', 'link', 'time', 'content']
    # 时间戳转换
    def timestamp_to_date(self,timestamp):
        return time.strftime('%Y-%m-%d', time.localtime(timestamp))

    # 创建或初始化CSV文件
    def init_csv_file(self):
        # 如果文件不存在，则创建文件并写入表头
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    # 追加数据到CSV文件
    def append_to_csv(self, articles):
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            for article in articles:
                writer.writerow(article)


    # 爬取数据
    def get_data(self):
        self.init_csv_file()
        for page in range(1, 10):
            print(f"正在爬取第{page}页数据")
            if page > 1:
                self.params['begin'] = str(page * 5)
            response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers)
            data = json.loads(response.text)
            date_public = json.loads(data.get('publish_page')).get('publish_list')
            articles = []

            for item in date_public:
                data_res = json.loads(item.get('publish_info'))
                appmsgex = data_res.get('appmsgex')
                for data_detail in appmsgex:
                    title = data_detail.get('title', "")
                    link = data_detail.get('link', "")
                    create_time = self.timestamp_to_date(item.get('create_time'))
                    detail_article = requests.get(link,headers=self.headers)
                    selectors = parsel.Selector(detail_article.text)
                    data = selectors.xpath('//div[@id="js_content"]')
                    data_detail = data.css('*::text').getall()
                    page_info = " ".join(i for i in data_detail)
                    articles.append({'title': title,
                                     'link': link,
                                     'time': create_time,
                                     'content': page_info,
                                     })
                    sleep(1)
            self.append_to_csv(articles)


