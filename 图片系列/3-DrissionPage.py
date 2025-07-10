from DrissionPage import ChromiumPage
from time import sleep
from DrissionPage import SessionPage

browser = ChromiumPage()    # 打开浏览器
browser.get('https://pic.netbian.com/e/search/result/?searchid=147')
for num in range(1,10):
    img_list = browser.eles('css:.slist ul li')
    for li in img_list:
        try:
            img_src = li.ele("css:a img").attr('src')
            img_name = li.ele('css:a b').text
            img_name = img_src.split('/')[-1]  # 以/为分割符分隔，取列表最后一个元素（照片命名）
            save_path = r'./image1'
            page = SessionPage()
            res = page.download(img_src, save_path)
            print(res, img_name, img_src)
        except Exception as e:
            print(e)
    sleep(1)
    browser.ele('@text()=下一页').click()


