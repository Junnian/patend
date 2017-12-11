# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from getpatent.settings import FIELD 
class GetpatentPipeline(object):
    def open_spider(self,spider):
        host = '127.0.0.1'
        port = 27017
        dbname = 'patent'  # 设置数据库
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        t = FIELD
        if t==0:
            self.all = tdb['test']
            self.allc = tdb['test_c']
            self.allc2 = tdb['test_c2']
            self.allc3 = tdb['test_c3']

        if t==1:
            self.all = tdb['aerospace']
            self.allc = tdb['aerospace_c']
            self.allc2 = tdb['aerospace_c2']
            self.allc3 = tdb['aerospace_c3']

        if t==2:
            self.all = tdb['bigdata']
            self.allc = tdb['bigdata_c']
            self.allc2 = tdb['bigdata_c2']
            self.allc3 = tdb['bigdata_c3']

        if t==3:
            self.all = tdb['infornet']
            self.allc = tdb['infornet_c']
            self.allc2 = tdb['infornet_c2']
            self.allc3 = tdb['infornet_c3']

        if t==4:
            self.all = tdb['newM']
            self.allc = tdb['newM_c']
            self.allc2 = tdb['newM_c2']
            self.allc3 = tdb['newM_c3']

        if t==5:
            self.all = tdb['QC']
            self.allc = tdb['QC_c']
            self.allc2 = tdb['QC_c2']
            self.allc3 = tdb['QC_c3']

        if t==6:
            self.all = tdb['shipBuild']
            self.allc = tdb['shipBuild_c']
            self.allc2 = tdb['shipBuild_c2']
            self.allc3 = tdb['shipBuild_c3']

        if t==7:
            self.all = tdb['biology']
            self.allc = tdb['biology_c']
            self.allc2 = tdb['biology_c2']
            self.allc3 = tdb['biology_c3']


    def process_item(self, item, spider):
        if spider.name =="patent":
            self.all.update({'Publication_number': item['Publication_number']}, {'$set': dict(item)}, True)
        if spider.name =="patent2":
            self.allc.update({'Publication_number': item['Publication_number']}, {'$set': dict(item)}, True)
        if spider.name =="patent3":
            self.allc2.update({'Publication_number': item['Publication_number']}, {'$set': dict(item)}, True)
        if spider.name =="patent4":
            self.allc3.update({'Publication_number': item['Publication_number']}, {'$set': dict(item)}, True)
        return item