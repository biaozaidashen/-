# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings

from beike.items import BeiKespiderItem


class BeikePipeline(object):
    def process_item(self, item, spider):
        return item


class PymongoBeiKePipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[BeiKespiderItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, BeiKespiderItem):
            self.collection.update({'house_code': item['house_code']}, {'$set': item}, True)

        return item
