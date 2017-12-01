# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class GetpatentPipeline(object):
    def open_spider(self,spider):
        host = '127.0.0.1'
        port = 27017
        dbname = 'patent'  # 设置数据库,也就是这话怕论文的
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.all = tdb['google2']
    def process_item(self, item, spider):
        # items = dict(item)
        #公开号为唯一性的标准,目前这个Title,有的没有
        self.all.update({'Publication_number': item['Publication_number']}, {'$set': dict(item)}, True)
        # self.all.insert(items)
        return item