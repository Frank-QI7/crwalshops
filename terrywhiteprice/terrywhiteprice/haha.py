from pyquery import PyQuery as pq
import re
import requests

selector = pq(filename='text.html')
pattern = re.compile('page=(\d+)')
urls = 'https://www.chemistwarehouse.com.au/Shop-Online/260/Medical-Aids?size=120' + '&page={page_count}'
# products = selector('#p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem tr td').items()
# category = selector('#category_title_h1 #category_title_span').text().strip()
# for product in products:
#     img = product('img[class!=product_image_overlay]').attr('src')
#     name = product('img[class!=product_image_overlay]').attr('alt').strip()
#     price = product('.Price').text().strip()
#     print("img:",img)
#     print('name:',name)
#     print('price:',price)
#     print('category:',category)
try:
    page_count = pattern.findall(str(selector('.last-page').attr('href')))[0]
    for i in range(2, int(page_count) + 1):
        # 在这里 可以不添加 callback，因为默认就是parse，
        # 但是是其他的就必须添加，其实是自己忘记添加了，才发现默认就是parse！！！！！！！！！！！！！！！！！！！！
        print(urls.format(page_count=i))
except:
    page_count = selector('.next-page').attr('href')
    url = 'https://www.chemistwarehouse.com.au' + page_count
    print(url)