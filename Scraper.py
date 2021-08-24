import scrapy
import urlparse
from scrapy.http import Request


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ['https://www.lyst.com/shop/dresses/']

    def parse(self, response):
        for i in range(0, len(response.xpath('//*[contains(@href, "/clothing/")]/@href').extract())):
            relative_path = response.xpath('//*[contains(@href, "/clothing/")]/@href').extract()[i]
            follow = urlparse.urljoin("https://www.lyst.com", relative_path)
            yield Request(url=follow, callback=self.parse_contents, meta={"url": follow})

    def parse_contents(self,response):
            yield {
                "Brand": response.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/article/div[2]/div[1]/h1/div[1]/a/text()').extract(),
                "Description": response.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/article/div[2]/div[1]/h1/div[2]/text()').extract(),
                "Price": response.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/article/div[2]/div[2]/div/div[1]/div/div/span/span[2]/text()').extract(),
                "Image urls": response.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/article/div[1]/div[2]/div[1]//a/@href').extract(),
            }
            next_page = response.xpath('//*[contains(@rel, "next")]/@href').extract()
