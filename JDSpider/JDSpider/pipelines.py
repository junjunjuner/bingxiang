# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.utils.project import get_project_settings
from JDSpider.settings import FIELDS_TO_EXPORT
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import time

settings = get_project_settings()

class JdspiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话,在settings.py底部追加
        # MINGO_USER = "username"
        # MONGO_PSW = "password"
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        insert_item = dict(item)  # 把item转化成字典形式
        # 插入之前查询text是否存在，不存在的时候才插入。
        # self.coll.update({"time": insert_item['time']}, {
        #                  '$setOnInsert': insert_item}, True)
        self.coll.insert(insert_item)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写


class CSVPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # file = open('jd电烤箱_%s.csv' % (self.printfNow()), 'wb')
        file = open('jd电冰箱_%s.csv' % (self.printfNow()), 'wb')
        # file = open('%s_pages_%s.csv' % (spider.name,self.printfNow()), 'a+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = FIELDS_TO_EXPORT
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())