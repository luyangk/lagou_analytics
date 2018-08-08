import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SlotPolicy
from scrapy import FormRequest

import re

import numpy as np
import pandas as pd

import codecs

class LagouAndroidSpider(scrapy.Spider):
    name = "mi_auto"
    #allowed_domains = []

    start_urls = [
        #"https://www.lagou.com/jobs/list_android?city=上海&cl=false&fromSearch=true&labelWords=&suginput=",
        #"https://www.lagou.com/jobs/list_android?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=",
        "https://www.google.com/search?q=material+informatics",
        #"https://www.lagou.com/zhaopin/tuxiangshibie/?labelWords=label",
        #"http://www.baidu.com/",
    ]

    tmp_list = []
    tmp_url = ""
    tmp_page = 0
    tmp_max_page = 0

    text = ""

    def start_requests(self):
        for url in self.start_urls:
            self.tmp_url = url
            yield SplashRequest(
                url,
                self.parse_first,
                slot_policy=SlotPolicy.SINGLE_SLOT,
                args={'wait':15, 'timeout':3600}
            )

    script = """
    function main(splash)
        splash.resource_timeout = 3600
        assert(splash:go(splash.args.url))
        splash:wait(25)
        splash:runjs('$("span[page=\\'ToBeReplaced\\']").click();')
        splash:wait(25)
        return splash:html()
    end
    """

    def parse_first(self, response):
        print('@@@start first page@@@')
        sel = scrapy.Selector(response)
        result_links = sel.xpath('//h3[@class="r"]')
        print("result counts: " + str(len(result_links)))
        for result in result_links:
            url = result.xpath('./a/@href').extract()[0]
            if url[-4:] == ".pdf":
                continue
            yield SplashRequest(
                url,
                self.parse,
                #endpoint='execute',
                slot_policy=SlotPolicy.SINGLE_SLOT,
                args={
                    'wait': 25,
                    'timeout': 3600  # ,
                    # 'lua_source': tmp_script
                }
            )

        pages = sel.xpath('//td/a[@class="fl"]')
        count=0
        for page in pages:
            # if count > 1:
            #     break
            url = 'https://www.google.com' + page.xpath('@href').extract()[0]
            print(url)
            yield SplashRequest(
                url,
                self.parse_page,
                #endpoint='execute',
                slot_policy=SlotPolicy.SINGLE_SLOT,
                args={
                    'wait': 15,
                    'timeout': 3600 #,
                    #'lua_source': tmp_script
                }
            )
            count+=1

    def parse_page(self, response):
        print("parse one page")
        sel = scrapy.Selector(response)
        result_links = sel.xpath('//h3[@class="r"]')
        for result in result_links:
            url = result.xpath('./a/@href').extract()[0]
            if url[-4:] == ".pdf":
                continue
            yield SplashRequest(
                url,
                self.parse,
                #endpoint='execute',
                slot_policy=SlotPolicy.SINGLE_SLOT,
                args={
                    'wait': 25,
                    'timeout': 3600 #,
                    #'lua_source': tmp_script
                }
            )

    def parse(self, response):
        print("parse one result")
        sel = scrapy.Selector(response)
        #for test in sel.xpath('//*').extract():
        #    print(test)
        nodes = sel.xpath('//p[text()]')
        self.text = ""
        for node in nodes:
            self.text += node.xpath('./text()').extract()[0]

        with codecs.open("output.txt", "a", "utf-8") as text_file:
            text_file.write("\n@@@@@@\n" + self.text)

