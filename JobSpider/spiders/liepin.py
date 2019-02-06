# -*- coding: utf-8 -*-
import time
from datetime import  datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JobSpider.items import LiePinJobItemLoader,LiePinJobItem
from JobSpider.utils.common import get_md5

class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com']

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*")), follow=False),
        Rule(LinkExtractor(allow=("it/.*")), follow=True),
        Rule(LinkExtractor(allow=r'job/\d+.shtml'), callback='parse_job', follow=True),
        Rule(LinkExtractor(allow=r'cjob/\d+.shtml'), callback='parse_job', follow=True),
        Rule(LinkExtractor(allow=r'a/\d+.shtml'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        #解析猎聘网职位
        item_loader = LiePinJobItemLoader(item=LiePinJobItem(), response=response)
        item_loader.add_value("job_url",response.url)
        item_loader.add_value("job_url_md5", get_md5(response.url))
        item_loader.add_css("job_name", ".title-info h1::attr(title)")
        item_loader.add_css("job_addr", ".basic-infor a::text")
        item_loader.add_css("job_desc", ".job-description .content-word::text")
        #salary 这个字段需要重新加工，直接获取的值包含很多不需要的字符
        item_loader.add_css("salary", ".job-item-title::text")
        item_loader.add_xpath("education", "//*[@class='job-qualifications']/span[1]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job-qualifications']/span[2]/text()")
        item_loader.add_xpath("language", "//*[@class='job-qualifications']/span[3]/text()")
        item_loader.add_xpath("age", "//*[@class='job-qualifications']/span[4]/text()")
        item_loader.add_css("company_name", ".title-info h3 a::attr(title)")
        item_loader.add_xpath("company_type", "//*[@class='new-compintro']/li[1]/a/text()")
        item_loader.add_xpath("company_size", "//*[@class='new-compintro']/li[2]/text()")
        item_loader.add_xpath("company_addr", "//*[@class='new-compintro']/li[3]/text()")
        item_loader.add_css("company_desc", ".company-info-main .info-word::text")
        item_loader.add_css("welfare", ".comp-tag-list li span::text")
        item_loader.add_css("publish_date", ".basic-infor time::attr(title)")
        item_loader.add_value("crawl_date",datetime.now().strftime('%Y-%m-%d'))
        job_item = item_loader.load_item()

        return job_item
