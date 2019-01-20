# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.commands import parse
from scrapy.http import response

from baidu.items import  ArticleItemLoader, ArticleItem


def get_md5(url):
    pass


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="archive"]//div[@class="post-thumb"]')     # 首先获取文章的所有url
        print(post_nodes)
        for post_node in post_nodes:

         post_url = post_node.xpath('.//a/@href').extract_first()  # 文章的地址
         print(post_url)
        # image_url = post_node.xpath('.//img/@src').extract_first()  # 文章图片的地址
        # print(image_url)
         #image_url = parse.urljoin(response.url, image_url)  # 以前的文章图片是在本域名下，所以拼接一下。
         #yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail,meta={'image_url': image_url})  # 用回调函数分析文章页面的元素
         # 提取下一页的url

         next_url = response.xpath('//*[@id="archive"]//a[contains(@class,"next")]/@href').extract_first()
         if next_url:
             yield Request(url=next_url, callback=self.parse)

         def parse_detail(self, response):
             # 通过Itemloader加载Item
             image_url = response.meta.get('image_url')  # 传递图片的url
             item_loader = ArticleItemLoader(item=ArticleItem(), response=response)  # 将类设置为自定义的Itemloader类
             item_loader.add_xpath('title', '//*[@class="entry-header"]/h1/text()')  # 通过xpath来提取数据
             item_loader.add_value('url', response.url)  # 直接添加值
             item_loader.add_value('url_object_id', get_md5(response.url))
             item_loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()[1]')
             item_loader.add_value('image_url', [image_url])
             item_loader.add_xpath('praise_nums', "//span[contains(@class,'vote-post-up')]/h10/text()")
             item_loader.add_xpath('fav_nums', "//span[contains(@class,'bookmark-btn')]/text()")
             item_loader.add_xpath('comment_nums', "//a[@href='#article-comment']/span/text()")
             item_loader.add_xpath('content', '//*[@class="entry"]/p | //*[@class="entry"]/h3 | //*[@class="entry"]/ul')

             article_item = item_loader.load_item()  # 将规则进行解析，返回的是list
             yield article_item

        pass
