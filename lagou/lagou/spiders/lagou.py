import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SlotPolicy
from scrapy import FormRequest

import re

import numpy as np
import pandas as pd


class LagouAndroidSpider(scrapy.Spider):
    name = "lagou_pos"
    allowed_domains = ["lagou.com"]

    start_urls = [
        #"https://www.lagou.com/jobs/list_android?city=上海&cl=false&fromSearch=true&labelWords=&suginput=",
        #"https://www.lagou.com/jobs/list_android?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=",
        "https://www.lagou.com/jobs/list_%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=",
        #"https://www.lagou.com/zhaopin/tuxiangshibie/?labelWords=label",
        #"http://www.baidu.com/",
    ]

    tmp_list = []
    tmp_url = ""
    tmp_page = 0
    tmp_max_page = 0

    def start_requests(self):
        for url in self.start_urls:
            self.tmp_url = url
            yield SplashRequest(
                url,
                self.parse_first,
                slot_policy=SlotPolicy.SINGLE_SLOT,
                args={'wait':25, 'timeout':3600}
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
        #for test in sel.xpath('//*').extract():
        #    print(test)
        li_nodes = sel.xpath('//ul[@class="item_con_list"]/li[contains(@class, "con_list_item")]')

        for node in li_nodes:
            pos_id = node.xpath('@data-positionid').extract()[0]
            salary = node.xpath('@data-salary').extract()[0]
            company_id = node.xpath('@data-companyid').extract()[0]
            company_name = node.xpath('@data-company').extract()[0]
            pos_name = node.xpath('@data-positionname').extract()[0]
            pos_desc = node.xpath('./div[@class="list_item_bot"]/div[@class="li_b_r"]/text()').extract()[0].replace("“", "").replace("”", "").strip()
            print(company_name + " @ " + pos_name + " @ " + salary + " @ " + pos_desc + "\n")
            tmp_df = pd.DataFrame([[pos_id, pos_name, salary, company_id, company_name, pos_desc]], \
                                  columns=['pos_id', 'pos_name', 'salary', 'company_id', 'company_name', 'pos_desc'])
            # tmp_df.to_csv("test.csv")
            self.tmp_list.append(tmp_df)

        max_page_str = sel.xpath('//div[@class="item_con_pager"]/div[@class="pager_container"]/span/text()').extract()[-2]
        max_page_str = max_page_str.replace("\\n", "").strip()
        max_page = int(max_page_str)
        self.tmp_max_page = max_page
        print("max page:" + str(max_page))
        if (max_page > 1):
            for page_num in range(2, max_page + 1):
                print("page num:"+str(page_num))
                print("tmp_url" + self.tmp_url)
                tmp_script = self.script.replace("ToBeReplaced", str(page_num))
                print("script:" + tmp_script)
                self.tmp_page = page_num
                yield SplashRequest(
                    self.tmp_url,
                    self.parse,
                    endpoint='execute',
                    slot_policy=SlotPolicy.SINGLE_SLOT,
                    args={
                        'wait':25,
                        'timeout':3600,
                        'lua_source': tmp_script
                    }
                )

    def parse(self, response):
        print("parse one turn")
        sel = scrapy.Selector(response)
        #for test in sel.xpath('//*').extract():
        #    print(test)
        li_nodes = sel.xpath('//ul[@class="item_con_list"]/li[contains(@class, "con_list_item")]')
        for node in li_nodes:
            pos_id = node.xpath('@data-positionid').extract()[0]
            salary = node.xpath('@data-salary').extract()[0]
            company_id = node.xpath('@data-companyid').extract()[0]
            company_name = node.xpath('@data-company').extract()[0]
            pos_name = node.xpath('@data-positionname').extract()[0]
            pos_desc = node.xpath('./div[@class="list_item_bot"]/div[@class="li_b_r"]/text()').extract()[0].replace("“", "").replace("”", "").strip()
            print(company_name + " @ " + pos_name + " @ " + salary + " @ " + pos_desc + "\n")
            tmp_df = pd.DataFrame([[pos_id, pos_name, salary, company_id, company_name, pos_desc]], \
                                  columns=['pos_id', 'pos_name', 'salary', 'company_id', 'company_name', 'pos_desc'])
            self.tmp_list.append(tmp_df)

        #print(tmp_list)
        if (self.tmp_page == self.tmp_max_page):
            pos_df = pd.concat(self.tmp_list, ignore_index=True)
            pos_df.to_csv("pos_output.csv", index=False)
        #print(pos_df)
        #print(pos_df.head())
        #print(pos_df.tail())
