from pprint import pprint
import pandas as pd
import requests
from lxml import html
from pprint import pprint
main_link='https://www.lenta.ru'
req = requests.get(main_link).text
root = html.fromstring(req)

NEWS = []
hrefs_first = root.xpath('//div[contains(@class, "js-main__content")]//div[@class="first-item"]/a/@href') ## список ссылок на главную новость
names_first = root.xpath('//div[contains(@class, "js-main__content")]//div[@class="first-item"]/a/text()') ## список главных новостей (она одна)

hrefs = root.xpath('//div[contains(@class, "js-main__content")]//div[@class="item"]/a/@href') ## cписок ссылок всех новостей
names = root.xpath('//div[contains(@class, "js-main__content")]//div[@class="item"]/a/text()') ### список всех новостей
first_data = root.xpath('//div[@class="first-item"]//*//a//time/@datetime') ## список даты 1 новости
data = root.xpath('//div[contains(@class, "js-main__content")]//div[@class="item"]/a//time/@datetime') ## список всех дат
hrefs.append(hrefs_first[0])
names.append(hrefs_first[0])
data.append(first_data[0])
### Создаем списко полных ссылок для каждой новости
full_hrefs = []
for i in hrefs:
    full_hrefs.append(main_link+i)
## Собираем дату с каждой страницы так как на общей странице дата только в текстовом формате
data_pages = []
for i in full_hrefs:
    try:
        news_page = requests.get(i).text
        root_page = html.fromstring(news_page)
        if root_page is not None:
            try:
                data_page = root_page.xpath('//div[contains(@class, "b-topic__info")]//time[contains(@class, "g-date")]/@datetime')
                data_pages.append((str(data_page[0])[:10]).replace('-', '.'))
            except requests.exceptions.ConnectionError:
                print('NO root')
    except requests.exceptions.ConnectionError:
        data_pages.append('None')
        # print('NO LINK')

#объединяем все в 1 список
if len(hrefs) == len(names)==len(data)==len(data_pages):
    for i in zip(hrefs, names, data, data_pages):
        NEWS.append({'href': main_link + i[0], 'news': i[1].replace('\xa0', ''), 'data_text': i[2], 'data_time': i[3]})
else:
    print('NO MATCH LEN')
df = pd.DataFrame(NEWS)
print(df)

