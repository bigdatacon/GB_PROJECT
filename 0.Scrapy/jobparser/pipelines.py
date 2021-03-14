# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy256

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            vacancy_salary = self.salary_parse(item['salary'])
        elif spider.name == 'sjru':
            vacancy_salary = self.salary_parse_sj(item['salary'])
        vacancy_name = ''.join(item['name'])
        vacancy_link = item['link']

        vacancy_site = item['allowed_domains']
        vacancy_json = {
            'vacancy_name': vacancy_name,
            'vacancy_link' : vacancy_link,
            'vacancy_salary' : vacancy_salary,
            'vacancy_site': vacancy_site
        }
        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_json)
        return vacancy_json

    def salary_parse(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        if salary[0] == " до ":
            salary_min = None
            salary_max = salary[1]
            salary_currency = salary[-2]
        elif salary[0] == "от " and " до " not in salary[2]:
            salary_min = salary[1]
            salary_max = None
            salary_currency = salary[-2]
        elif salary[0] == "от " and " до " in salary[2]:
            salary_min = salary[1]
            salary_max = salary[3]
            salary_currency = salary[-2]

        result = [
            salary_min,
            salary_max,
            salary_currency
        ]
        return result

    def salary_parse_sj(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\[ха0', '')
        if salary[0] == 'до':
            salary_max = salary[2]
            salary_currency = salary[2][-4:]
        elif len(salary) == 3 and salary[0].isdigit():
            salary_max = salary[0]
            salary_currency = salary[0][-4:]
        elif salary[0] == 'от':
            salary_min = salary[2]
            salary_currency = salary[2][-4:]
        elif len(salary)>3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]
            salary_currency = salary[2][-4:]
        if 'По договорённости' in salary[-1]:
            salary_currency = 'По договоренности'
        result = [
            salary_min,
            salary_max,
            salary_currency
        ]
        return result

    def _get_name_currency(self, currency_name):
        currency_dict = {
            'EUR': {''},
            'RUR': {'руб.'},
            'USD': {'долл.', '$'}
        }
        name = None
        for key, val in currency_dict.items():
            if currency_name in val:
                name = key
        return name