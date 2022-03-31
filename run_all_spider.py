# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/31 15:45
# @Author : BruceLong
# @FileName: run_all_spider.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
from scrapy.utils import project

# 获取项目的配置信息
settings = project.get_project_settings()
# SpiderLoader用来加载Spider类的。每个Spider类都有一个name属性，它就是Spider的名称。SpiderLoader可以根据Spider的名称，来获取其对应的Spider类。
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
# 获取所有的spider
spiders = spider_loader.list()
# 加载类
classes = [spider_loader.load(name) for name in spiders]
# CrawlerProcess可以控制多个Crawler同时进行多种爬取任务
# CrawlerRunner是CrawlerProcess的父类，CrawlerProcess通过实现start方法来启动一个Twisted的reactor（另有shutdown信号处理、顶层logging功能）
process = CrawlerProcess(settings)
for cls in classes:
    process.crawl(cls)
process.start()
