# This is a test spider

from ImageCrawl.spiders import GoogleSearch_spider
import scrapy

if __name__ == '__main__':
    print("This is some output.")
    googleSpider = GoogleSearch_spider()
    googleSpider.parse()

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title = h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback = self.parse)
