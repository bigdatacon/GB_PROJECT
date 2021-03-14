from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import json
site = 'HH.RU'
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}
MAIN_link = 'https://hh.ru'
main_link = 'https://hh.ru/search/vacancy?text=Python'
html = requests.get(main_link, headers=headers).text
parsed_html = bs(html,'lxml')
vacancy_list = parsed_html.findAll('div',{'data-qa':'vacancy-serp__vacancy'})
main_link =  MAIN_link + parsed_html.find('a',{'data-qa':'pager-next'})['href']
print(main_link)
vaq_dict = []

def parse(main_link, MAIN_link, headers):
    vaq_dict = []
    for i in range(5):
        html = requests.get(main_link, headers=headers).text
        parsed_html = bs(html, 'lxml')
        vacancy_list = parsed_html.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
        main_link = MAIN_link + parsed_html.find('a', {'data-qa': 'pager-next'})['href']

        for vaq in vacancy_list:
                vaq_all_list = {}

                main_info = vaq.find('span',{'class':'g-user-content'}).findChild()
                name = main_info.getText()
                link = main_info['href']
                salary = vaq.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})


                if not salary:
                    salary_min = 'None'
                    salary_max = 'None'
                    currency = 'None'
                else:
                    salary_data = re.findall('(\d+[\s\d]*)', salary.getText())
                    currency = str(re.findall('([A-zА-я]{3}\.)', salary.getText()))[2:6]
                    if len(salary_data) >1:
                        salary_min = salary_data[0].replace('\xa0', ' ')
                        salary_max = salary_data[1].replace('\xa0', ' ')

                    else:
                        salary_min = salary_data[0].replace('\xa0', ' ')
                        salary_max = 'None'
                    vaq_all_list['name'] = name
                    vaq_all_list['link'] = link
                    vaq_all_list['salary_min'] = salary_min
                    vaq_all_list['salary_max'] = salary_max
                    vaq_all_list['currency'] = currency
                    vaq_all_list['page'] = i+1

                    vaq_dict.append(vaq_all_list)
    pprint(vaq_dict)


parse(main_link, MAIN_link, headers)
