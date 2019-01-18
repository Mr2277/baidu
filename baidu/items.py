# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # Field()能够接收和传递任何类型的值,类似于字典的形式
    create_date = scrapy.Field()  # 创建时间
    url = scrapy.Field()  # 文章路径
    front_img_url_download = scrapy.Field()
    fav_nums = scrapy.Field()  # 收藏数
    comment_nums = scrapy.Field()  # 评论数
    vote_nums = scrapy.Field()  # 点赞数
    tags = scrapy.Field()  # 标签分类 label
    content = scrapy.Field()  # 文章内容
    #object_id = scrapy.Field()  # 文章内容的md5的哈希值，能够将长度不定的 url 转换成定长的序列



    pass
