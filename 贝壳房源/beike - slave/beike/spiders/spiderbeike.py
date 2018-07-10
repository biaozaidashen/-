
from scrapy import Request
from scrapy.selector import Selector

from scrapy_redis.spiders import RedisSpider

from beike.items import BeiKespiderItem


class LianJiaSpider(RedisSpider):
    name = 'ershou'

    redis_key = 'beike:start_urls'

    def parse(self, response):
        sel = Selector(response)
        lis = sel.xpath('/html/body/div[4]/div[1]/ul/li')
        for li in lis:
            #所有信息都在li标签里，所以重点解析该标签
            item = BeiKespiderItem()

            # 房屋编号，具有唯一性
            item['house_code'] = li.xpath('./div[1]/div[6]/div[2]/@data-rid').extract()[0]

            # 所在城市
            item['city'] = '成都'

            # 区域名
            item['area'] = sel.xpath('//*[@data-role="ershoufang"]/div/a[@class="selected CLICKDATA"]/text()').extract()[0]

            # 爬取图片
            if li.xpath('./a/img[@class="lj-lazy"]/@src').extract():
                item['img_src'] = li.xpath('./a/img[@class="lj-lazy"]/@src').extract()[0]
            else:
                item['img_src'] = '暂时无图片'

            # 爬取房子标题
            if li.xpath('./div[1]/div[1]/a/text()').extract():
                item['title'] = li.xpath('./div[1]/div[1]/a/text()').extract()[0]

            # 房屋地址
            item['address'] = li.xpath('./div[1]/div[2]/div/a/text()').extract()[0]

            contents = li.xpath('./div[1]/div[2]/div/text()').extract()[0]
            content_list = self.split_house_info(contents)

            # 房子信息
            item['info'] = content_list

            #楼层
            item['flood'] = li.xpath('./div[1]/div[3]/div/text()').extract()[0]+li.xpath('./div[1]/div[3]/div/a/text()').extract()[0]

            #交通等

            item['tag'] = li.xpath('./div[1]/div[5]/span[1]/text()').extract()[0] if li.xpath('./div[1]/div[5]/span[1]/text()') else '' + (li.xpath('./div[1]/div[5]/span[2]/text()').extract()[0] if li.xpath('./div[1]/div[5]/span[2]/text()') else '') + (li.xpath('./div[1]/div[5]/span[3]/text()').extract()[0] if li.xpath('./div[1]/div[5]/span[3]/text()') else '')

            # 房屋单价
            item['price'] = li.xpath('./div[1]/div[6]/div[2]/span/text()').extract()[0]

            #房子总价
            item['total_price'] = li.xpath('./div[1]/div[6]/div[1]/span/text()').extract()[0]+li.xpath('./div[1]/div[6]/div[1]/text()').extract()[0].replace('\n', '').strip()

            # 房屋类型是二手房
            item['type'] = '二手房'

            yield item

    def split_house_info(self, info):
        return [i.strip() for i in info.split('|')[1:]] #对info值进行切片操作

