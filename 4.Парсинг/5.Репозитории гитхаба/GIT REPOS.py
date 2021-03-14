from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import requests
import getpass
from pprint import pprint
import json
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 RuxitSynthetic/1.0 v8089137528 t38550 ath9b965f92 altpub cvcv=2'}
main_link = 'https://api.github.com/users/bigdatacon/repos'
repos = requests.get(main_link)
data =json.loads(repos.text)

lists = {}
for i in range(len(data)):
    lists[i+1] = data[i]['name']

pprint(lists)

