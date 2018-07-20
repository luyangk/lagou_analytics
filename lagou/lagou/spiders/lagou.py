import scrapy
from scrapy_splash import SplashRequest

import numpy as np
import pandas as pd


class LagouAndroidSpider(scrapy.Spider):
    name = "lagou_pos"
    allowed_domains = ["lagou.com"]

    start_urls = [
        "https://www.lagou.com/jobs/list_android?city=上海&cl=false&fromSearch=true&labelWords=&suginput=",
        #"https://www.lagou.com/zhaopin/tuxiangshibie/?labelWords=label",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_list, args={'wait': 30})

    def parse_list(self, response):
        print('@@@start@@@')
        sel = scrapy.Selector(response)
        max_page = int(sel.xpath('//div[@class="pager_container"]/span').extract()[-2])

    def parse(self, response):

        sel = scrapy.Selector(response)
        li_nodes = sel.xpath('//ul[@class="item_con_list"]/li[contains(@class, "con_list_item")]')
        tmp_list = []
        for node in li_nodes:
            pos_id = node.xpath('@data-positionid').extract()[0]
            salary = node.xpath('@data-salary').extract()[0]
            company_id = node.xpath('@data-companyid').extract()[0]
            company_name = node.xpath('@data-company').extract()[0]
            pos_name = node.xpath('@data-positionname').extract()[0]
            tmp_df = pd.DataFrame([[pos_id, pos_name, salary, company_id, company_name]], \
                                  columns=['pos_id', 'pos_name', 'salary', 'company_id', 'company_name'])
            #tmp_df.to_csv("test.csv")
            tmp_list.append(tmp_df)

        #print(tmp_list)
        pos_df = pd.concat(tmp_list, ignore_index=True)
        pos_df.to_csv("test.csv")
        #print(pos_df)
        #print(pos_df.head())
        #print(pos_df.tail())
