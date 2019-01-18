# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_name(value):  # 接受的值就是title所有值,这值是列表的遍历
    return value + 'ok'


def date_convert(value):
    # 对时间进行处理格式
    value = value.strip().replace('·', '').strip()
    try:
        create_data = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_data = datetime.datetime.now().date()
    return create_data


def get_nums(value):
    # 处理评论和点赞的数
    math_re = re.search(r'(\d+)', value)
    if math_re:
        value = math_re.group(1)
    else:
        value = 0
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义Itemloader
    default_output_processor = TakeFirst()  # 自定义ouput_processor


class ArticleItem(scrapy.Item):
    # 标题
    title = Field(
        input_processor=MapCompose(add_name, lambda x: x + 'no')  # 可以传递任意多的函数进行从左到右处理。
    )
    # 时间
    create_date = Field(
        input_processor=MapCompose(date_convert),
    )
    # 文章url
    url = Field()
    # 对url进行md5
    url_object_id = Field()
    # 文章图片
    image_url = Field(  # 因为要求返回list，不能用str
        output_processor=MapCompose(lambda x: x)    # 变为一个list，但是在插入mysql的时候要求是str。
    )
    image_path = Field()
    # 点赞数
    praise_nums = Field()
    # 评论数
    comment_nums = Field(
        input_processor=MapCompose(get_nums)
    )
    # 点赞数
    fav_nums = Field(
        input_processor=MapCompose(get_nums)
    )
    # 内容
    content = Field(
        output_processor=Join('\n')  # 不选择第一个使用Join来进行链接
    )
