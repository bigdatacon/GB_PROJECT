import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    main_link = 'https://www.superjob.ru'
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = 'https://www.superjob.ru'+ response.xpath('//div[contains(@class, "_3zucV L1p51 undefined _1Fty7 _2tD21 _3SGgo")]/a[contains(@class, "f-test-button-dalshe")]/@href').get()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.xpath('//div[contains(@class, "_3mfro PlM3e _2JVkc _3LJqf")]//a/@href').getall()
        for link in vacancy:
            link_full = 'https://www.superjob.ru' + link
            yield response.follow(link_full,self.vacancy_parse)

    def vacancy_parse (self, response: HtmlResponse):
        name = response.css('div._3MVeX h1.s1nFK::text').extract_first()
        salary = response.css('div._2tD21 div._3MVeX span.ZON4b span._2Wp8I::text').extract()
        link = response.url
        allowed_domains = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, link = link, allowed_domains = allowed_domains)

