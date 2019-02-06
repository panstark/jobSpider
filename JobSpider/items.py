# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
import re

class JobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def date_now():

    create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def return_value(value):
    return value


class JobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

# class JobHunterItem(scrapy.Item):
#     job_detail_url=scrapy.Field()
#     job_name = scrapy.Field()
#     salary_year = scrapy.Field()
#     work_area= scrapy.Field()
#     education= scrapy.Field()
#     work_years= scrapy.Field()
#     post_date= scrapy.Field()
#     company_name= scrapy.Field()
#     company_type= scrapy.Field()
#     company_tags= scrapy.Field()

def remove_html(value):
    ##去掉内容中的/r/n""
    return value.replace("\r","").replace("\n","").replace(" ","")


class LiePinJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


#猎聘网职位信息
class LiePinJobItem(scrapy.Item):
    job_url_md5 = scrapy.Field()
    job_url = scrapy.Field()
    job_name = scrapy.Field()
    job_addr = scrapy.Field()
    job_desc = scrapy.Field()
    salary = scrapy.Field(
       input_processor =  MapCompose(remove_html),
    )
    welfare = scrapy.Field()
    education = scrapy.Field()
    work_years = scrapy.Field()
    language = scrapy.Field()
    age = scrapy.Field()
    company_name = scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_addr = scrapy.Field()
    company_desc = scrapy.Field(
        input_processor=MapCompose(remove_html),
    )
    publish_date = scrapy.Field()
    crawl_date = scrapy.Field()





