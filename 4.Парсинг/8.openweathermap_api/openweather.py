from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import requests
from pprint import pprint
import json

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}

main_link = 'https://api.openweathermap.org/data/2.5/weather'
city = 'London'
appid ='a8b228d1034444c470c0219e77683a08'
req = requests.get(f'{main_link}?q={city}&appid={appid}')
data2 = req.json()
print('in LONDON TEMP CALVIN {}'.format(data2['main']['temp']))
