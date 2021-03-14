from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}
main_link = 'https://www.kinopoisk.ru'

req = requests.get(main_link + '/afisha/new/city/1/', headers =headers).text
parsed_html = bs(req,'lxml')
films_block = parsed_html.find('div', {'class': 'filmsListNew'})
films_list = films_block.findChildren(recursive=False)
film_info_l = []
for film in films_list:
    films = {}
    main_info = film.find('div', {'class': 'name'}).findChild()
    film_name = main_info.getText()
    film_link = main_link + main_info['href']
    genre = film.findAll('div', {'class': 'gray'})[1].getText().replace(' ', '')[9:]
    rating = film.find('span', {'class': ['rating_ball_green', 'rating_ball_red', 'rating_ball_grey']})
    if not rating:
        rating = 0
    else:
        rating = rating.getText()
    films['name'] = film_name
    films['link'] = film_link
    films['genre'] = genre
    films['rating'] = rating
    film_info_l.append(films)
pprint(film_info_l)
