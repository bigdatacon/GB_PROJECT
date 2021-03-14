import requests
from lxml import html
from pprint import pprint
main_link='https://www.kinopoisk.ru'
req = requests.get(main_link+'/afisha/new/city/458/').text

root = html.fromstring(req)


#films_block = root.xpath("//div[contains(@class, 'filmsListNew')]")

hrefs = root.xpath('//div[@class="name"]/a/@href')
names = root.xpath('//div[@class="name"]/a/text()')
genre = root.xpath('//div[@class="gray"][last()]/text()')
rating = root.xpath('//div[@class="rating"]/span/text()')
print(rating)
//div[@class="item"]
//div[@class="item"]/a
//div[@class="first-item"]/a
//div/time[@class="g-date"]

### ВОТ НОРМАЛЬНЫЙ ССЫЛКИ
//div[contains(@class, 'js-main__content')]//div[@class="item"]/a
//div[contains(@class, 'js-main__content')]//div[@class="first-item"]/a
# <div class="span8 js-main__content" xpath="1">

# //a[@data-statlog="services_new.item.video.1"l]
# <a data-id="video" class="home-link services-new__item services-new__item_search_yes home-link_black_yes" href="https://yandex.ru/video/?utm_source=main_stripe_big" target="_blank" rel="noopener" data-statlog="services_new.item.video.1" xpath="1">