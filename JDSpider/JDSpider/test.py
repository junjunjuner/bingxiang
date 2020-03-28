from lxml import etree
import time
# with open('ceshi.html', 'r') as f:
#     page_source = f.read()
# # print(page_source)
#
# sel = etree.HTML(page_source)
# module = sel.xpath(".//li[@class='jSubObject']/span/@data-id")
# html = sel.xpath(".//li[@class='jSubObject']/div[@class='jItem']/div[@class='jPic']/a/@href")
# next_page=sel.xpath(".//div[@class='jPage']/a[text()='下一页']/@href")
# if next_page:
#     print(next_page)
# # print(next_page)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))