# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy
from scrapy import Selector
import jionlp as jio

from untils.map_dict import month_dict, category_dict, level_dict
from untils.tools import formatting_time
from ..items import WeiboKyqzItem

ft_time = lambda ttime: formatting_time([ttime.replace(k, v) for k, v in month_dict.items() if k in ttime][0])


class AiWeiboKyqzSpider(scrapy.Spider):
    name = 'ai_weibo_kyqz'
    allowed_domains = ['weibo.cn']
    # 用户信息
    # 用户首页
    base_user_index_url = 'https://m.weibo.cn/profile/{user_id}'
    # 用户chat_message
    base_chat_message_box_url = 'https://m.weibo.cn/message/chat?uid={user_id}'
    # 详情页基础链接
    base_detail_url = 'https://m.weibo.cn/statuses/extend?id={detail_id}'
    share_detail_url = 'https://m.weibo.cn/status/{detail_id}'

    # 评论接口基础链接
    base_comment_url = 'https://m.weibo.cn/comments/hotflow?id={detail_id}&mid={mid}&max_id_type=0'
    start_urls = [
        # 抗疫救助上海
        'https://m.weibo.cn/api/container/getIndex?extparam=%E6%8A%97%E7%96%AB%E6%B1%82%E5%8A%A9&containerid=10080889902a1e60cd81187b008223d86da809__4752855407132993_-_tag_status_sort&luicode=10000011&lfid=100808fb9b9095ff03a9c13211bb1daf41f0e2_-_sort_time&since_id=0',
        # 上海抗疫救助
        'https://m.weibo.cn/api/container/getIndex?extparam=%E4%B8%8A%E6%B5%B7%E6%8A%97%E7%96%AB%E6%B1%82%E5%8A%A9&containerid=100808fb9b9095ff03a9c13211bb1daf41f0e2_-_sort_time&luicode=10000011&lfid=10080889902a1e60cd81187b008223d86da809__4752855407132993_-_tag_status_sort&since_id=0',
        # 吉林

    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        '''
        解析列表页数据
        :param response:
        :return:
        '''
        result = json.loads(response.text)
        temp_data = result.get('data', {})
        cards = temp_data.get('cards')
        for card in cards:
            datas = card.get('card_group', [])
            for data in datas:
                source_data = data.get('mblog')
                if source_data:
                    item = WeiboKyqzItem()
                    # 源数据
                    item['source_data'] = source_data
                    # 表名
                    item['table_name'] = 'list_source_data'
                    yield item
                    source_id = source_data.get('id')
                    # 解析详情页数据
                    yield scrapy.Request(url=self.base_detail_url.format(detail_id=source_id),
                                         callback=self.parse_detail, meta={
                            "id": source_id,
                            "user_id": source_data.get('user', {}).get('id'),
                            "user_name": source_data.get('user', {}).get('screen_name'),
                            "created_at": source_data.get('created_at'),
                            "latest_update": source_data.get('latest_update'),
                        }
                                         )
                    # 解析评论数据
                    yield scrapy.Request(url=self.base_comment_url.format(detail_id=source_id, mid=source_id),
                                         callback=self.parse_comment, meta={"id": source_id})
        # 获取下一页url
        page_num = temp_data.get('pageInfo', {}).get('since_id')
        if page_num:
            next_url = re.sub("since_id=(\d+)", "since_id={}".format(page_num), response.url)
            # 进行翻页
            yield scrapy.Request(url=next_url, callback=self.parse_list)

        pass

    def parse_detail(self, response):
        '''
        解析详情页内容
        :param response:
        :return:
        '''
        meta = response.meta
        result = json.loads(response.text)
        data = result.get('data')
        if data:
            item = WeiboKyqzItem()
            # # 详情页ID
            data['id'] = meta.get('id')
            # # 作者名
            data['user_name'] = meta.get('user_name')
            data['latest_update'] = ft_time(meta.get('latest_update'))
            data['created_at'] = ft_time(meta.get('created_at'))
            # 详情页内容
            data['detail_url'] = self.share_detail_url.format(detail_id=meta.get('id'))
            # 用户首页
            data['user_index_url'] = self.base_user_index_url.format(user_id=meta.get('user_id'))
            # 直接和作者聊天链接
            data['chat_message_box_url'] = self.base_chat_message_box_url.format(user_id=meta.get('user_id'))
            # 解析出来的正文内容
            content_text = ''.join(Selector(text=data.get('longTextContent', '')).xpath('//text()').extract())
            # 分类打标签
            data['categories'] = ['其它']
            data['category_tags'] = []
            categories = {v for k, v in category_dict.items() if k in content_text}
            if categories:
                data['categories'] = list(categories)
                data['category_tags'] = [k for k, v in category_dict.items() if k in content_text]
            # 等级打标签
            data['level'] = '其它'
            data['level_tags'] = []
            categories = {v for k, v in level_dict.items() if k in content_text}
            if categories:
                data['level'] = min(list(categories))
                data['level_tags'] = [k for k, v in level_dict.items() if k in content_text]
            data['content_text'] = content_text
            if content_text.strip():
                # 抽取地址信息
                location_infos = jio.parse_location(location_text=content_text)
                data.update(location_infos)
                # 抽取手机号
                phone_number = jio.extract_phone_number(content_text)
                data['phone_number'] = phone_number
                # 是否提供有联系方式
                data['is_phone_number'] = '是' if phone_number else '否'
                # # 身份证信息
                # data['id_card'] = jio.extract_id_card(content_text)
                # # 解析QQ号因为里面可能包含本地的电话号
                # data['qq_info'] = jio.extract_qq(content_text)
                # # 解析链接有的可能是转发的
                # data['urls'] = jio.extract_url(content_text)
            # 数据采集时间
            data['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 源数据
            item['source_data'] = data
            # 表名
            item['table_name'] = 'detail_source_data'
            yield item

    def parse_comment(self, response):
        '''
        解析评论页内容
        *注：因为没有登录的原因就只能获取前20条数据
        :param response:
        :return:
        '''
        meta = response.meta
        result = json.loads(response.text)
        datas = result.get('data', {}).get('data')
        if datas:
            for data in datas:
                item = WeiboKyqzItem()
                # 源数据
                data['detil_id'] = meta.get('id')
                data['created_at'] = ft_time(data.get('created_at'))
                data['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 解析出来的正文内容
                content_text = ''.join(Selector(text=data.get('text', '')).xpath('//text()').extract())
                data['content_text'] = content_text
                if content_text.strip():
                    # 抽取地址信息
                    location_infos = jio.parse_location(location_text=content_text)
                    data.update(location_infos)
                    # 抽取手机号
                    data['phone_number'] = jio.extract_phone_number(content_text)
                    # # 身份证信息
                    # data['id_card'] = jio.extract_id_card(content_text)
                    # # 解析QQ号因为里面可能包含本地的电话号
                    # data['qq_info'] = jio.extract_qq(content_text)
                    # # 解析链接有的可能是转发的
                    # data['urls'] = jio.extract_url(content_text)
                item['source_data'] = data
                # 表名
                item['table_name'] = 'comment_source_data'
                yield item
