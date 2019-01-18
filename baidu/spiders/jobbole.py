# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.commands import parse
from scrapy.http import response

from baidu.items import BaiduItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="archive"]//div[@class="post-thumb"]')     # 首先获取文章的所有url
        print(post_nodes)
        for post_node in post_nodes:

         post_url = post_node.xpath('.//a/@href').extract_first()  # 文章的地址
         image_url = post_node.xpath('.//img/@src').extract_first()  # 文章图片的地址
         image_url = parse.urljoin(response.url, image_url)  # 以前的文章图片是在本域名下，所以拼接一下。
         yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail,
                      meta={'image_url': image_url})  # 用回调函数分析文章页面的元素
        # 提取下一页的url

         next_url = response.xpath('//*[@id="archive"]//a[contains(@class,"next")]/@href').extract_first()
         if next_url:
             yield Request(url=next_url, callback=self.parse)

        pass
