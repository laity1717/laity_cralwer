
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os

if not os.path.exists('./images'):
    os.mkdir('./images')

driver = webdriver.Edge()
driver.get('https://pic.netbian.com/e/search/result/?searchid=147')
for num in range(0,14): # 多页爬取
    data_img=driver.find_elements(by=By.XPATH, value='//div[@class="slist"]/ul/li/a/img')  # 使用xpath定位到图片资源
    for img in data_img:
        img_url=img.get_attribute('src')
        response=requests.get(img_url)
        img_data=response.content           # 获取到图片的二进制数据
        with open('./images/'+img_url.split('/')[-1], 'wb') as f:
            f.write(img_data)
        print("下载成功;",img_url.split('/')[-1])
    print(f"第{num}页下载完成")
    sleep(2)
    driver.find_element(by=By.XPATH, value='//a[text()="下一页"]').click()
