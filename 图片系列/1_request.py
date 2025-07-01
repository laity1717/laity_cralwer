""""
利用request爬取彼岸图网的图片
"""
import requests
import parsel
import os
import re

url = 'https://pic.netbian.com/e/search/result/?searchid=147'

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}
# 创建目录images
if not os.path.exists('./images'):
    os.mkdir('./images')

res = 0
for num in range(0,15):
    url = f'https://pic.netbian.com/e/search/result/index.php?page={num}&searchid=147'
    response = requests.get(url, headers=headers)
    selector = parsel.Selector(response.text)
    data_list = selector.xpath('//div[@class="slist"]/ul/li')

    # 处理数据
    for li in data_list:
        title = li.css('a b::text').get()
        print(title)
        title = title.replace(' ','').replace("*",'-')
        de_src = 'https://pic.netbian.com' + li.css('a img::attr(src)').get()

        # 保存到本地
        img_data = requests.get(de_src,headers=headers).content
        with open('./images/' + title + '.jpg','wb') as f:
            f.write(img_data)
        print("已下载:",title,"网址为:",de_src)
        res += 1
    print(f'第{num}页爬取完成')
print(f'共爬取{res}张')