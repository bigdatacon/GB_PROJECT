from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import requests
import getpass
from pprint import pprint
import json
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}
main_link = 'https://api.vk.com/method/friends.get?v=5.52&access_token='
token = '' ### тут токен
repos = requests.get(f'{main_link}{token}')
data =json.loads(repos.text)
pprint(data['response']['items'])
