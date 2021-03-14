from lxml import html
import requests
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

def requests_to_yandex():
    str='Суши'
    try:
        request = requests.get('https://www.yandex.ru/search/',
                                   params={'text':str}, headers=header)
        root = html.fromstring(request.text)

        result_list = root.xpath(
                "//a[contains(@class, 'organic__url')]/@href")
        if result_list:
            for i in result_list:
                print(i)
        else:
                print("At your request no results were found. Please, check your request.")

    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)

requests_to_yandex()