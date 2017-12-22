# -*- coding: utf-8 -*-

# Scrapy settings for getpatent project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'getpatent'

SPIDER_MODULES = ['getpatent.spiders']
NEWSPIDER_MODULE = 'getpatent.spiders'

FIELD = 0
start_urls=[]
if FIELD == 0:
    key1s = ['test']  # new
    key2s = ['test']  # key
if FIELD == 1:
    key1s = ['aerospace']  # new
    key2s = ['aerospace']  # key
if FIELD == 2:
    key1s = ['bigdata']
    key2s = ['bigData', 'bigData2', 'big_data']
if FIELD == 3:
    key1s = ['infornet']
    key2s = ['informationNetworks']
if FIELD == 4:
    key1s = ['newM']
    key2s = ['newMaterials']
if FIELD == 5:
    key1s = ['QC']
    key2s = ['quantumCommunication']
if FIELD == 6:
    key1s = ['ShipB']
    key2s = ['shipBuilding']
if FIELD == 7:
    key1s = ['biology']
    key2s = ['biology', 'Biological Engineering']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'getpatent (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
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
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'getpatent.middlewares.GetpatentSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'getpatent.middlewares.UserAgentMiddleware': 543,
}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'getpatent.pipelines.GetpatentPipeline': 300,
}

#LOG_LEVEL = 'INFO'
# 禁止cookies:
#COOKIES_ENABLED = False
#宽度优先
#SCHEDULER_ORDER = "BFO"
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
