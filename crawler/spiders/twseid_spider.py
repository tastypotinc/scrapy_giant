# -*- coding: utf-8 -*-

import re
import string

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from crawler.items import TwseIdItem

# TWSE id : http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
# 權證ID rule http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
# ref https://github.com/samho5888/pyStockGravity/blob/master/src/StockIdDb.py

__all__ = ['TwseIdSpider']

class TwseIdSpider(CrawlSpider):
    name = 'twseid'
    allowed_domains = ['http://isin.twse.com.tw']
    download_delay = 2

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseIdSpider, self).__init__()
        self.start_urls = ['http://isin.twse.com.tw/isin/C_public.jsp?strMode=2']

    def parse(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = TwseIdItem()
        item['data'] = []
        elems = sel.xpath('.//tr')
        for elem in elems[1:]:
            its = elem.xpath('./td/text()').extract()
            # skip 權證
            if len(its) < 6:
                continue
            its = [it.strip(string.whitespace).replace(',', '') for it in its]
            m = re.search(r'([0-9a-zA-Z]+)(\W+)?', its[0].replace(u' ', u'').replace(u'\u3000', u''))
            yy, mm, dd = its[2].split('/') if its[2] else [None]*3
            sub = {
                'stockid': m.group(1) if m else None,
                'stocknm':  m.group(2) if m else None,
                'onmarket': u"%s-%s-%s" % (yy, mm, dd) if None not in [yy, mm, dd] else None,
                'industry': its[4] if its[4] else None
            }
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
