# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

import sys
import os
#获取文件所在电脑的路径，方便调试系统scrapy crawl jobbole
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","hunter"])
