# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#建立模型


class BeiKespiderItem(scrapy.Item):
    collections = 'ershoufang'

    house_code = scrapy.Field() #房子id
    city = scrapy.Field()  # 城市
    area = scrapy.Field()  # 区域
    img_src = scrapy.Field() #图片
    title = scrapy.Field() #标题
    address = scrapy.Field() #地址
    info = scrapy.Field() #房子信息

    flood = scrapy.Field() #楼层，建筑年份等

    tag = scrapy.Field() #交通,看房时间等

    price = scrapy.Field() #房子单价
    total_price = scrapy.Field()  #房子总价
    type = scrapy.Field() #房子类型

