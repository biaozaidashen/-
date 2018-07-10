import json

from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from beike.items import SpiderBeiKeItem


class BeiKei(Spider):
    name = 'ershou'
    domains_url = 'https://cd.ke.com'

    start_urls_ershoufang = 'https://cd.ke.com/ershoufang/'

    def start_requests(self):
        #请求资源，该函数是从父类继承而来，是固定写法

        yield Request(self.start_urls_ershoufang, callback=self.parse_ershou)

    def parse_ershou(self, response):
        sel = Selector(response)
        areas = sel.xpath('//*[@data-role="ershoufang"]/div/a')

        for area in areas:
            area_href = area.xpath('./@href').extract()[0]  # 得到区域的链接

            yield Request(self.domains_url + area_href, callback=self.parse_page,
                          meta={'href': area_href})
            # meta参数的作用是进行函数回调时将参数值传给函数

    def parse_page(self, response):
        sel = Selector(response)
        page = sel.xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract()[0]

        total_page = json.loads(page).get('totalPage')

        # 得到指定区域的总页数

        for i in range(1, int(total_page) + 1):  # 分页
            item = SpiderBeiKeItem()
            item['url'] = self.domains_url + response.meta.get('href')+'pg'+str(i)
            yield item



