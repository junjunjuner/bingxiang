# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class MdspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item

# 第一种方法：存储到mongodb（scrapy自带的代码）
import pymongo
# from MDSpider.settings import MONGO_URL
# from MDSpider.settings import MONGO_DATABASE
from MDSpider.settings import collection_name

class MongoPipeline1(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # get中有两个参数，一个是配置的MONGO_URL，另一个若不配置默认为localhost
            mongo_uri=crawler.settings.get('MONGO_URI'),
            # 第一个参数是数据库配置的，第二个参数是数据库名
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[collection_name].insert_one(dict(item))
        return item

import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

# 第二种方法：存储到mongodb（自定义的）
class MongoPipeline2(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
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
        # 参数1 {'zmmc': item['zmmc']}: 用于查询表中是否已经存在zmmc对应的documents文档。
        # 参数2 要保存或者更新的数据
        # 参数3 True: 更新(True)还是插入(False, insert_one())
        # self.db['job'].update_one({'zmmc': item['zmmc']}, {'$set': dict(item)}, True)
        self.coll.insert(insert_item)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写

# 第一种方法：存储到mysql（同步）
import pymysql
class MysqlPileline1(object):
    def __init__(self):
        # 数据库主机名（默认为本地主机），数据库登录名（默认为当前用户），数据库密码（默认为空），要打开的数据库名称（无默认，可缺省），MySQL使用的TCP端口（默认为3306，可缺省），数据库字符编码（可缺省）
        # self.conn = pymysql.connect(host, user, passwd, db, port, charset='utf-8')
        self.conn = pymysql.connect(host=settings['mysql_host'],db=settings['mysql_db'],
                                    port=settings['mysql_port'],charset='utf-8')
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        inset into test_zxf(quote,author,tags) VALUES(%s, %s, %s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql,(item['quote'], item['author'],item['tags']))
        # 提交执行
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

# 第二种方法：存储到mysql（异步）
import pymysql
from twisted.enterprise import adbapi

class MysqlPipeline2(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    # 函数名固定，会被scrapy调用，直接可用settings的值
    def from_settings(cls, settings):
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['mysql_host'],
            db=settings['mysql_db'],
            user=settings['mysql_user'],
            passward=settings['mysql_passwd'],
            cursorclass=pymysql.cursors.DictCursor   #指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
       使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
       """
        # 指定操作方法和操作数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        # sql语句
        insert_sql = """
                inset into test_zxf(quote,author,tags) VALUES(%s, %s, %s)
                """
        # 执行插入数据到数据库操作
        cursor.execute(insert_sql, (item['quote'], item['author'], item['tags']))

    def handle_error(self, failure):
        if failure:
            print(failure)





# 存储到csv（scrapy带exporter csv模块）
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from MDSpider.settings import csv_name
from MDSpider.settings import FIELDS_TO_EXPORT

class CsvPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(csv_name)
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        # 列出导出哪些field值，None表示导出所有field，默认值为None
        self.exporter.fields_to_export = FIELDS_TO_EXPORT
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 存储到excel表
from openpyxl import Workbook
from MDSpider.settings import excel_header
from MDSpider.settings import excel_content
from MDSpider.settings import excel_name
# 存储到excel表
class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        # 设置表头（可将配置写在setting.py中方便统一管理）
        self.ws.append(excel_header)

    def process_item(self, item ,spider):
        line = []
        for content in excel_content:
            line.append(item[content])
        self.ws.append(line)
        self.wb.save(excel_name)
        return item


# 存储到excel表另一种方法
from scrapy.exporters import BaseItemExporter
import xlwt

class ExcelItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook(encoding='utf-8')
        self.wsheet = self.wbook.add_sheet('scrapy')
        self._header_not_written = True
        self.fields_to_export = list()
        # excel表行坐标
        self.row = 0

    def finish_exporting(self):
        self.wbook.save(self.file)

    # 判断是否存在第一行字段声明，若不存在则调用
    def export_item(self, item):
        if self._header_not_written:
            self._header_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        # 获取item所有字段的迭代器
        fields = self._get_serialized_fields(item)
        for col, v in enumerate(x for _, x in fields):
            print(self.row, col, str(v))
            # 将各字段写入excel表
            self.wsheet.write(self.row, col, str(v))
        self.row += 1

    # 根据item属性名写入第一行
    def _write_headers_and_set_fields_to_export(self, item):
        if not self.fields_to_export:
            if isinstance(item, dict):
                self.fields_to_export = list(item.keys())
            else:
                self.fields_to_export = list(item.fields.keys())
        for columns,v in enumerate(self.fields_to_export):
            self.wsheet.write(self.row, columns, v)
        self.row += 1