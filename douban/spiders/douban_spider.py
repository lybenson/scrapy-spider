# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

# douban genspider douban_spider movie.douban.com

root_url = 'http://movie.douban.com/top250'
class DoubanSpiderSpider(scrapy.Spider):

    # 爬虫名
    name = "douban_spider"
    # 运行的域名
    allowed_domains = ["movie.douban.com"]
    # 入口url, 会传到调度器
    start_urls = [root_url]

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()

            content = item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()

            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s

            douban_item['star'] = item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = item.xpath(".//p[@class='quote']/span/text()").extract_first()

            # yield 传入item pipelines
            yield douban_item

        # 解析下一页
        next_link = response.xpath("//span[@class='next']/link/@href").extract()

        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(root_url + next_link, callback=self.parse)


