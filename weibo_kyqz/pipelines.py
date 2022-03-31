# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class WeiboKyqzPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri  # MongoDB的uri
        self.mongo_db = mongo_db  # mongodb对应的数据库名

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        try:
            self.db[item['table_name']].update_one({"id": item['source_data']['id']},
                                                   {"$set": dict(item['source_data'])},
                                                   upsert=True)
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        self.client.close()
