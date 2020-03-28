# -*- coding: utf-8 -*-
import time

# Scrapy settings for MDSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MDSpider'

SPIDER_MODULES = ['MDSpider.spiders']
NEWSPIDER_MODULE = 'MDSpider.spiders'

# Item Processor(即 Item Pipeline) 同时处理(每个response的)item的最大值。默认: 100
CONCURRENT_ITEMS = 100

# Scrapy downloader 并发请求(concurrent requests)的最大值。默认: 16
CONCURRENT_REQUESTS = 32

# 对单个网站进行并发请求的最大值。默认：8
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。默认：0
# 如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。
# 也就是说，并发限制将针对IP，而不是网站。
# 该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，下载延迟应用在IP而不是网站上。
# CONCURRENT_REQUESTS_PER_IP = 0

# 下载器在下载同一个网站下一个页面前需要等待的时间。默认：0
# 该选项可以用来限制爬取速度， 减轻服务器压力。同时也支持小数。如0.25： # 250 ms of delay
# 该设定影响(默认启用的) RANDOMIZE_DOWNLOAD_DELAY 设定。
# 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY 的结果作为等待间隔。
# 当 CONCURRENT_REQUESTS_PER_IP 非0时，延迟针对的是每个ip而不是网站。
DOWNLOAD_DELAY = 3

# 如果启用，当从相同的网站获取数据时，Scrapy将会等待一个随机的值 (0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY)。
# 若 DOWNLOAD_DELAY 为0(默认值)，该选项将不起作用。默认：true
RANDOMIZE_DOWNLOAD_DELAY = True

# Scrapy HTTP Request使用的默认header。由 DefaultHeadersMiddleware 产生。
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
# }

# 爬取网站最大允许的深度(depth)值。如果为0，则没有限制。默认：0
# DEPTH_LIMIT = 0



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MDSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'MDSpider.middlewares.MdspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'MDSpider.middlewares.MdspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'MDSpider.pipelines.MongoPipeline1': 300,
    'MDSpider.pipelines.ExcelPipeline': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# excel存储配置
# 设置excel表表头
excel_header = ['数据来源','商品型号','商品价格','采集时间']
# 设置excel表内容字段
excel_content = ['source','product_model','product_price','ProgramStarttime']
# 设置excel表名称
excel_name = "excel冰箱价格.xlsx"

#csv存储配置
csv_name = "csv冰箱价格.csv"
# 列出导出哪些field值，None表示导出所有field，默认值为None
FIELDS_TO_EXPORT = None

# mongodb存储配置
# 连接
MONGO_URI = 'mongodb://10.2.46.149:1500'
# 数据库名
MONGO_DATABASE = 'fridgeProduct'
# 表名
collection_name = 'fridge_data'
# 数据库地址
MONGO_HOST = 'localhost'
# 数据库端口号
MONGO_PORT = 27017

# mysql存储配置
# 主机名
mysql_host = 'localhost'
# 登录名
mysql_user = 'root'
# 密码
mysql_passwd = '*****'
# 数据库名
mysql_db = 'test'
# 端口号
mysql_port = 3306

LOG_FILE = 'md电冰箱_log_%s.txt' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
