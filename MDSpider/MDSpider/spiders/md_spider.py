import scrapy
import requests
from MDSpider.items import MdspiderItem
import json
# from html.parser import HTMLParser
from lxml import etree
import math
import time

class MDSpider(scrapy.Spider):
    # 爬虫启动名称
    name = 'md_spider'
    # 允许爬取的范围，防止爬取到其他网站
    allowed_domains = ['midea.cn']
    nowTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 从哪一页开始
    page = 1
    # 拼接开头
    url_head = 'https://www.midea.cn/search/search_ajax_data?category_id=10008&is_onsale=1&pageno='
    # 开启爬取的地址
    start_urls = [
        # 'https://www.midea.cn/10008.html?mtag=40003.3.1'
        url_head + str(page)
    ]
    # 获取自定义开始 def start_requests(self)
    def parse(self, response):
        # sel = scrapy.Selector(response)
        body = json.loads(response.body)
        sel = etree.HTML(body['data'])
        # 获取每个商品
        goods_list = sel.xpath(".//li[@class='hproduct']")
        for goods in goods_list:
            # 获取商品链接
            href = goods.xpath(".//a/@href")[0]
            # print(href)
            # 获取价格
            price = goods.xpath(".//div[@class='ft_message']/div[@class='price_new']/span[@class='price']/em/text()")[0]
            # 获取商品名称
            product_name = goods.xpath("normalize-space(.//a[@class='fn']/text())")
            if 'http' not in href:
                goods_href = 'https://www.midea.cn' + href
            else:
                goods_href = href
            # 定义item
            item = MdspiderItem()
            item['product_href'] = goods_href
            item['product_price'] = price
            item['product_name'] = product_name
            request = scrapy.Request(url=goods_href, callback=self.goods, meta={'item': item})
            yield request

        #翻页
        # 共多少个数据
        total = body['total']
        print("共有%d个数据"%total)
        total_page = math.ceil(int(total)/24)
        print("共有%d页"%total_page)
        if self.page < total_page:
            # 下一页
            self.page = self.page + 1
            url = self.url_head + str(self.page)
            request = scrapy.Request(url=url, callback=self.parse)
            yield request


    def goods(self, response):
        item = response.meta['item']
        sel = scrapy.Selector(response)
        detail = sel.xpath(".//div[@class='tabs_content_wrap']/div[@id='product_spec']")
        detail_wrap = detail.xpath(".//div[@class='spec_wrap']")
        detail_dict = {}
        detail_tr = detail_wrap.xpath(".//tr")
        for tr in detail_tr:
            detail_key = tr.xpath(".//td[1]/text()").extract()[0].strip('：')
            detail_value = tr.xpath(".//td[2]/text()").extract()[0]
            # print(detail_key,detail_value)
            detail_dict[detail_key] = detail_value
        # print(detail_dict)
        item['source'] = '美的官网'
        item['product_detail'] = detail_dict
        item['product_model'] = detail_dict['产品型号']
        item['product_brand'] = '美的'
        item['ProgramStarttime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['nowTime'] = self.nowTime
        yield item
