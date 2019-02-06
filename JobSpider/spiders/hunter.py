# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from datetime import  datetime
from JobSpider.items import LiePinJobItemLoader,LiePinJobItem
from JobSpider.utils.common import get_md5


class HunterSpider(scrapy.Spider):
    name = 'hunter'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/it/']
    #java_url https://www.liepin.com/zhaopin/;jsessionid=908F9AAC51E7828500235C88B104BBFB?imscid=R000000035&key=Java&dqs=010
    def parse(self,response):
        """""
        1、获取文章列表页中的文章url并交给解析函数进行具体字段的解析
        2、获取下一页的url并交给scrapy
        """""
        #xpath可以通过浏览器直接获取
        #虚拟环境调试：scrapy shell https://www.liepin.com/it/
        #re_selector= response.xpath('//*[@id="subsite"]/div[1]/div[1]/ul/li[1]/div/p/a[1]/@href');
        sid_bar_urls= response.css(".sidebar dd a")
        for sid_bar_url in sid_bar_urls:
            url = sid_bar_url.css("::attr(href)").extract_first("").replace("&dqs=140020","&dqs=010")
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)
            #yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)
        # print(parse.urljoin(response.url, url))

    def parse_detail(self, response):
        job_divs = response.css(".sojob-item-main");
        for job_div in job_divs:
            job_detail_url = job_div.css(".job-info h3 a::attr(href)").extract()[0]
            yield Request(url=parse.urljoin(response.url, job_detail_url), callback=self.job_detail)
        next_url = response.css(".pagerbar a::attr(href)").extract()[7]
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_detail)

    def job_detail(self, response):
        # 解析猎聘网职位
        item_loader = LiePinJobItemLoader(item=LiePinJobItem(), response=response)
        item_loader.add_value("job_url", response.url)
        item_loader.add_value("job_url_md5", get_md5(response.url))

        job_url = response.url;
        if("/a/" in job_url):
            item_loader.add_css("job_name", ".title-info h1::attr(title)")
            item_loader.add_css("job_desc", ".job-description .content-word::text")
            item_loader.add_css("company_desc", ".company-info-main .info-word::text")
            item_loader.add_css("publish_date", ".basic-infor time::attr(title)")
            item_loader.add_value("crawl_date", datetime.now().strftime('%Y-%m-%d'))
            item_loader.add_xpath("job_addr", "//*[@class='basic-infor']/span/text()")
            item_loader.add_xpath("salary", "//*[@class='job-title-left']/p[1]/text()")
            item_loader.add_xpath("education", "//*[@class='resume clearfix']/span[1]/text()")
            item_loader.add_xpath("work_years", "//*[@class='resume clearfix']/span[2]/text()")
            item_loader.add_xpath("language", "//*[@class='resume clearfix']/span[3]/text()")
            item_loader.add_xpath("age", "//*[@class='resume clearfix']/span[4]/text()")
            item_loader.add_css("company_name", ".title-info h3::text")
            item_loader.add_css("company_type", ".content-word ul li a::attr(title)")
            item_loader.add_css("company_size", ".content-word ul li::text")
            item_loader.add_xpath("company_addr", "//*[@class='new-compintro']/li[3]/text()")
            item_loader.add_css("welfare", ".comp-tag-list li span::text")
        elif("/job/" in job_url):
            item_loader.add_css("job_name", ".title-info h1::attr(title)")
            item_loader.add_css("job_desc", ".job-description .content-word::text")
            item_loader.add_css("company_desc", ".company-info-main .info-word::text")
            item_loader.add_css("publish_date", ".basic-infor time::attr(title)")
            item_loader.add_value("crawl_date", datetime.now().strftime('%Y-%m-%d'))
            item_loader.add_css("job_addr", ".basic-infor a::text")
            # salary 这个字段需要重新加工，直接获取的值包含很多不需要的字符
            item_loader.add_css("salary", ".job-item-title::text")
            item_loader.add_xpath("education", "//*[@class='job-qualifications']/span[1]/text()")
            item_loader.add_xpath("work_years", "//*[@class='job-qualifications']/span[2]/text()")
            item_loader.add_xpath("language", "//*[@class='job-qualifications']/span[3]/text()")
            item_loader.add_xpath("age", "//*[@class='job-qualifications']/span[4]/text()")
            item_loader.add_css("company_name", ".title-info h3 a::attr(title)")
            item_loader.add_xpath("company_type", "//*[@class='new-compintro']/li[1]/a/text()")
            item_loader.add_xpath("company_size", "//*[@class='new-compintro']/li[2]/text()")
            item_loader.add_xpath("company_addr", "//*[@class='new-compintro']/li[3]/text()")
            item_loader.add_css("welfare", ".comp-tag-list li span::text")
        # else:
        #     item_loader.add_css("job_name", ".job-title h1::text")
        #     item_loader.add_css("job_desc", ".job-description .content-word::text")
        #     item_loader.add_css("company_desc", ".company-info-main .info-word::text")
        #     item_loader.add_css("publish_date", ".basic-infor time::attr(title)")
        #     item_loader.add_value("crawl_date", datetime.now().strftime('%Y-%m-%d'))
        #     item_loader.add_css("job_addr", ".job-main-tip span::text")
        #     # salary 这个字段需要重新加工，直接获取的值包含很多不需要的字符
        #     item_loader.add_css("salary", ".job-item-title::text")
        #     item_loader.add_xpath("education", "//*[@class='job-qualifications']/span[1]/text()")
        #     item_loader.add_xpath("work_years", "//*[@class='job-qualifications']/span[2]/text()")
        #     item_loader.add_xpath("language", "//*[@class='job-qualifications']/span[3]/text()")
        #     item_loader.add_xpath("age", "//*[@class='job-qualifications']/span[4]/text()")
        #     item_loader.add_css("company_name", ".title-info h3 a::attr(title)")
        #     item_loader.add_xpath("company_type", "//*[@class='new-compintro']/li[1]/a/text()")
        #     item_loader.add_xpath("company_size", "//*[@class='new-compintro']/li[2]/text()")
        #     item_loader.add_xpath("company_addr", "//*[@class='new-compintro']/li[3]/text()")
        #     item_loader.add_css("welfare", ".comp-tag-list li span::text")
        job_item = item_loader.load_item()
        return job_item
