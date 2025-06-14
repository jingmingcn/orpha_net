import scrapy
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

class OrphaSpider(scrapy.Spider):
    name = "orpha_extra"
   
    # start_urls = ["https://orpha.com"]

    async def start(self):
        #https://www.orpha.net/en/disease/detail/90636?name=90636&mode=orpha
        base_url = "https://www.orpha.net/en/disease/detail/"

        with open('OrphaCode.csv', 'r') as file:
            lines = file.readlines()
            for orphacode in lines[1:]:
                yield scrapy.Request(url=base_url+orphacode+"?name="+orphacode+"&mode=orpha",callback=self.parse)

    def parse(self, response):

        url = response.url
        parsed_url = urlparse(url)
        qs = parse_qs(parsed_url.query)
        orphacode = qs['name'][0]

        

        for i in response.xpath('//div[contains(@class, "result-detail")]/div[contains(@class, "mx-4 mb-4 p-4 bg-gray")]'):
            yield {
                "orphacode":orphacode,
                "Prevalence":i.xpath('//strong[text()="Prevalence: "]/following-sibling::span/text()').get(),
                "Inheritance":i.xpath('//strong[text()="Inheritance: "]/following-sibling::span/text()').get(),
                "Age of onset":i.xpath('//strong[text()="Age of onset: "]/following-sibling::span/text()').get(),
                "Synonym":i.xpath('//strong[text()="Synonym(s): "]/following-sibling::ul/li/text()').get(),
            }