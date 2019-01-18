# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.commands import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #print("tttt")
        #print(response)
        #print(response.css)
        post_nodes = response.css("#archive .floated-thumb .post-thumb")  # a selector, 可以在这个基础上继续做 selector
        print(post_nodes)
        for post_node in post_nodes:
            post_url = post_node.css("a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),callback=self.parse_detail)

        pass
