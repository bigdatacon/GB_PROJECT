
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link,self.vacancy_parse)

    def vacancy_parse (self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.bloko-header-1::text').extract()
        salary = response.css('div.vacancy-title p.vacancy-salary span.bloko-header-2::text').extract()
        link = response.url
        allowed_domains = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, link = link, allowed_domains = allowed_domains)




