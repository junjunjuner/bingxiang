import scrapy
from bs4 import BeautifulSoup
import requests
import re
import json
from JDSpider.items import JdBingxiangItem
import time,random
import pandas as pd
import csv

class jdspider(scrapy.Spider):
    name="jd_spider"
    allowed_domains=["jd.com"]
    start_urls=[
        "https://list.jd.com/list.html?cat=737,794,878&ev=exbrand_7817%7C%7C12380"   #京东电冰箱
    ]
    num=0
    pagenum=0
    ProgramStarttime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    with open("price.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ProductID", "PreferentialPrice", "price"])

    def parse(self, response):
        sel=scrapy.Selector(response)

        '''''''''
        方法二
        '''''''''
        productid_list1=sel.xpath(".//div[@id='plist']/ul/li/div[contains(@class,'gl-i-wrap')]/@data-sku").extract()
        #单件，套餐……
        productid_list2 = sel.xpath( ".//div[@class='gl-i-tab-content']/div[@class='tab-content-item tab-cnt-i-selected j-sku-item']/@data-sku").extract()
        productid_list=productid_list1+productid_list2
        print(productid_list)
        print(len(productid_list))
        productid_str='%2CJ_'.join(productid_list)
        # time.sleep(random.randint(60,120))
        price_web="https://p.3.cn/prices/mgets?ext=11000000&pin=&type=1&area=1_72_4137_0&skuIds=J_"+str(productid_str)
        price_webs = requests.get(price_web, timeout=1000).text
        price_jsons = json.loads(price_webs)
        if len(price_jsons)>50:
            self.pagenum=self.pagenum+1
            print("第"+str(self.pagenum)+"页")
        for price_json in price_jsons:
            try:
                id = price_json['id']
                ProductID = id[2:]
                PreferentialPrice = price_json['p']
                price = price_json['m']
            except:
                ProductID=None
                PreferentialPrice = None
                price = None  # 商品价格
            if ProductID:
                item=JdBingxiangItem()
                with open("price.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([ProductID,PreferentialPrice,price])
                item['ProductID']=ProductID
                item['price'] = PreferentialPrice
                # item['price'] = price
                goods_web = "https://item.jd.com/" + str(ProductID) + ".html"
                request = scrapy.Request(url=goods_web, callback=self.goods, meta={'item': item}, dont_filter=True)
                yield request
            else:
                print("ProductID未获取到")
                self.num=self.num+1
            if (self.num)>60:
                print("ProductID多次未获取到")
                exit()

        ''''''''''
        方法一
        '''''''''''
        # # url="https://item.jd.hk/18739277759.html"    #京东全球购与普通网址不同，不同的地方为“https://item.jd.com/4251335.html”
        # goods_info=sel.xpath(".//div[@id='plist']/ul/li")
        # for goods in goods_info:
        #     ProductID_info=goods.xpath(".//div[@class='gl-i-wrap j-sku-item']/@data-sku").extract()       #商品编号
        #     if len(ProductID_info)==0:
        #         ProductID_info=goods.xpath(".//div[@class='gl-i-tab-content']/div[@class='tab-content-item tab-cnt-i-selected j-sku-item']/@data-sku").extract()
        #         ProductID=ProductID_info[0]
        #     else:
        #         ProductID=ProductID_info[0]
        #     # print(ProductID)
        #     if len(ProductID)!=0:
        #         goods_web="https://item.jd.com/"+str(ProductID)+".html"         #商品链接   包含商品型号,店铺名称,类别,品牌,型号等
        #         item=JdItem(ProductID=ProductID)
        #         request=scrapy.Request(url=goods_web,callback=self.goods,meta={'item':item},dont_filter=True)
        #         yield request
        #     else:
        #         print("parse中ProductID为空  没有读到")

        # #测试用
        # productid_list1=sel.xpath(".//div[@id='plist']/ul/li/div[contains(@class,'gl-i-wrap')]/@data-sku").extract()
        # #单件，套餐……
        # productid_list2 = sel.xpath( ".//div[@class='gl-i-tab-content']/div[@class='tab-content-item tab-cnt-i-selected j-sku-item']/@data-sku").extract()
        # productid_list=productid_list1+productid_list2
        # print(productid_list)
        # print(len(productid_list))
        # for ProductID in productid_list:
        #     item = JinghuaqiItem(ProductID=ProductID,price=2.00,PreferentialPrice=2.00)
        #     # url="https://item.jd.hk/1971910764.html"
        #     url="https://item.jd.com/" + str(ProductID) + ".html"
        #     request = scrapy.Request(url=url, callback=self.goods,meta={'item':item}, dont_filter=True)
        #     yield request
        # item = JdBingxiangItem()
        # ProductID = '2788652'
        # item['ProductID'] = ProductID
        # item['price'] = None
        # # item['price'] = price
        # goods_web = "https://item.jd.com/" + str(ProductID) + ".html"
        # request = scrapy.Request(url=goods_web, callback=self.goods, meta={'item': item}, dont_filter=True)
        # yield request

        # #翻页功能
        # time.sleep(random.randint(60, 120))
        # next_page=sel.xpath(".//div[@class='p-wrap']/span[@class='p-num']/a[@class='pn-next']/@href").extract()
        # if next_page:
        #     next="https://list.jd.com/"+next_page[0]
        #     yield scrapy.Request(next,callback=self.parse)

    def goods(self,response):
        item=response.meta['item']
        sel=scrapy.Selector(response)
        url=response.url
        body=response.body
        ProductID=item['ProductID']
        # PreferentialPrice = item['PreferentialPrice']
        price = item['price']

        if "error" in url or "2017?t" in url:        #302重定向页面,写回原页面处理
            url="https://item.jd.com/"+str(ProductID)+".html"
            item = JdBingxiangItem(ProductID=ProductID, price=price)
            yield scrapy.Request(url, callback=self.goods, meta={'item':item})
            return None

        # --------------------全球购网页---------------------------------------------
        elif "hk" in url:
            print("全球购：", url)

            #京东商品介绍部分
            detail_info = sel.xpath(".//div[@class='p-parameter']")  # 包含商品详情内容
            detail = detail_info.xpath(".//li/text()").extract()
            if detail[0]=='品牌： ':
                detail_brand=detail_info.xpath(".//li[1]/@title").extract()[0]
                detail[0]=detail[0]+detail_brand
            product_detail = '\"'+' '.join(detail).replace('\t', '').replace('\n', '').replace('  ','')+'\"'
            detail_1 = detail_info.extract()          #缩小范围，从商品介绍部分获取想要的内容
            goods_dict = {}
            # 商品介绍部分更新为dict
            for d in detail:
                d_list = d.split('：', 1)
                if len(d_list) > 1:
                    goods_dict[d_list[0]] = d_list[1].strip(' ')

            #商品名称
            try:
                p_Name = sel.xpath(".//div[@class='sku-name']/text()").extract()[-1].strip('\"').strip('\n').strip().replace('\t', '').split(' ')[0]
                print(p_Name)
            except:
                p_Name = None

            # detail_info=sel.xpath(".//div[@class='p-parameter']/text()").extract()

            #店铺名称
            try:
                shop_name = sel.xpath(".//div[@class='shopName']/strong/span/a/text()").extract()[0]  # 店铺名称
                goods_dict['店铺'] = shop_name
            except:
                try:
                    shop = sel.xpath(".//div[@class='p-parameter']/ul[@class='parameter2']/li[3]/@title").extract()[0]
                    if '店' in shop:
                        goods_dict['店铺'] = shop
                    else:
                        pass
                except:
                    pass


            #京东规格与包装部分（将这部分的内容读为字典形式，x为字典）
            try:
                s = BeautifulSoup(body, 'lxml')
                guige = s.find('div', id_='specifications')
                # x = {}
                guige2 = guige.find_all('td', class_='tdTitle')
                guige3 = guige.find_all('td', class_=None)
                for i in range(len(guige2)):
                    dt = re.findall(">(.*?)<", str(guige2[i]))
                    dd = re.findall(">(.*?)<", str(guige3[i]))
                    goods_dict.setdefault(dt[0], dd[0])
            except:
                pass

            # 型号
            if '型号' in goods_dict:
                product_model = goods_dict['型号']
            elif '认证型号' in goods_dict:
                product_model = goods_dict['认证型号']
            else:
                product_model = None

        # ---------------------普通网页-----------------------------------
        else:

            #商品名称（1.从名称处读；2.从表头的名称处读）
            try:
                p_Name = sel.xpath(".//div[@class='sku-name']/text()").extract()[0].strip('\"').strip('\n').strip().replace('\t', '')  # 商品名称
                if len(p_Name) == 0:     # 如发生商品名称读取结果为空的情况
                    p_Name = sel.xpath(".//div[@class='item ellipsis']/@title").extract()[0].replace('\t', '')
            except:
                try:
                    p_Name = sel.xpath(".//div[@class='item ellipsis']/@title").extract()[0].replace('\t', '')
                except:
                    p_Name = None

            goods_dict = {}

            #京东商品介绍部分
            detail_info = sel.xpath(".//div[@class='p-parameter']")  # 包含商品详情内容
            detail = detail_info.xpath(".//li/text()").extract()
            if detail[0]=='品牌： ':
                detail_brand=detail_info.xpath(".//li[1]/@title").extract()[0]
                detail[0]=detail[0]+detail_brand
            product_detail = '\"'+' '.join(detail).replace('\t', '').replace('\n', '').replace('  ','')+'\"'
            detail_1 = detail_info.extract()
            # 商品介绍部分更新为dict
            for d in detail:
                d_list = d.split('：', 1)
                if len(d_list) > 1:
                    goods_dict[d_list[0]] = d_list[1].strip(' ')

            #京东规格与包装部分（读取为字典格式）
            try:
                s = BeautifulSoup(body, 'lxml')
                # print(s)
                guige = s.find('div', class_='Ptable')
                # print (guige)
                guige1 = guige.find_all('div', class_='Ptable-item')
                # print (guige1)
                # x = {}
                for gg in guige1:
                    guige2 = gg.find_all('dt', class_=None)
                    guige3 = gg.find_all('dd', class_=None)
                    for i in range(len(guige2)):
                        dt = re.findall(">(.*?)<", str(guige2[i]))
                        dd = re.findall(">(.*?)<", str(guige3[i]))
                        goods_dict.setdefault(dt[0], dd[0])
            except:
                pass

            #店铺名称
            if '店铺' not in goods_dict:
                try:
                    shop_name = sel.xpath(".//div[@class='name']/a/text()").extract()[0]  # 店铺名称
                    goods_dict['店铺'] = shop_name
                except:
                    pass

            #不是品牌：**的形式，不用find
            if '品牌' not in goods_dict:
                try:
                    brand = detail_info.xpath(".//ul[@id='parameter-brand']/li/a/text()").extract()[0].strip()
                    goods_dict['品牌'] = brand
                except:
                    pass

            # 型号
            if '型号' in goods_dict:
                product_model = goods_dict['型号']
            elif '认证型号' in goods_dict:
                product_model = goods_dict['认证型号']
            else:
                product_model = None

        print(goods_dict)

        ''''''''''
        方法一
        '''''''''''
        if float(price)>0.00:
            item['ProductID'] = ProductID
            item['detail'] = product_detail
            item['product_name'] = p_Name
            item['product_href'] = url
            item['product_price']=price
            item['product_detail'] = goods_dict
            item['product_model']= product_model

            item['source']="京东"
            item['ProgramStarttime']=self.ProgramStarttime
            yield item
        else:
            print('广告及无效页面:',url)
