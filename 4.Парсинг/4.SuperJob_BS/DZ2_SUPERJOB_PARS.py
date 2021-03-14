from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import json
site = 'HH.RU'
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}
MAIN_link = 'https://www.superjob.ru'
main_link = 'https://www.superjob.ru/vacancy/search/?keywords=Python'
def parse(main_link, MAIN_link, headers):
    vaq_list = []
    for i in range(2):
        html = requests.get(main_link, headers=headers).text
        parsed_html = bs(html, 'lxml')
        vacancy_list = parsed_html.findAll('div', {'_2g1F-'})
        main_link = MAIN_link + parsed_html.find('a', {'rel': 'next'})['href']

        for vaq in vacancy_list:
            vaq_dict = {}
            main = vaq.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'})
            if main:
                # link = main['href']
                name = main.getText()
                vaq_dict['name'] = name
            link = vaq.find('a', {'target': '_blank'})
            if link:
                link = link['href']
                vaq_dict['link'] = MAIN_link + link
                vaq_dict['page'] = i+1
            salary_block = vaq.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})

            if salary_block:
                salary = salary_block.getText().replace('\xa0', '')
                if 'огов' in salary:
                    salary_min = 'По договоренности'
                    vaq_dict['salary_min'] =salary_min
                    salary_max = 'None'
                    vaq_dict['salary_max'] = salary_max
                    vaq_dict['currency'] = "None"
                    vaq_list.append(vaq_dict)
                elif 'от' in salary:
                    salary_min = salary[2:-4]
                    vaq_dict['salary_min'] =salary_min
                    salary_max = 'None'
                    vaq_dict['salary_max'] = salary_max
                    vaq_dict['currency'] = re.findall('([а-я]{3})', salary)[0]
                    vaq_list.append(vaq_dict)
                elif 'до' in salary:
                    salary_min = 'None'
                    vaq_dict['salary_min'] =salary_min
                    salary_max = salary[2:-4]
                    vaq_dict['salary_max'] = salary_max
                    vaq_dict['currency'] = re.findall('([а-я]{3})', salary)[0]
                    vaq_list.append(vaq_dict)
                elif '—' in salary:
                    salary_data = re.findall('(\d*\W\d*)', salary)[0]
                    salary_data = '-'.join(salary_data.split('-'))
                    if len(salary_data)>2:
                        salary_data_min =salary_data.rpartition('—')[0]
                        salary_data_max = salary_data.partition('—')[2]
                        vaq_dict['salary_min'] =salary_data.rpartition('—')[0]
                        vaq_dict['salary_max'] = salary_data.partition('—')[2]
                        vaq_dict['currency'] = re.findall('([а-я]{3})', salary)[0]
                        vaq_list.append(vaq_dict)
        pprint(vaq_list)
parse(main_link, MAIN_link, headers)

