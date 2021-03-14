from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome()
driver.get('https://www.mvideo.ru/televizory-i-video')
time.sleep(5)
print('Вход на страницу МВИДЕО')

while True:
    try:
        iframe = driver.find_element_by_class_name('flocktory-widget')
        driver.switch_to.frame(iframe)
        button = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'PushTip-close'))
        )
        button.click()
        driver.get('https://www.mvideo.ru/televizory-i-video')
        time.sleep(2)
        while True:
            try:
                iframe = driver.find_element_by_class_name('flocktory-widget')
                driver.switch_to.frame(iframe)
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'Widget-close'))
                )
                #path-1
                button.click()

                driver.get('https://www.mvideo.ru/televizory-i-video')
            except Exception as e:
                print('Не было всплывающего окна 2')
                break
    except Exception as e:
        print('Не было всплывающего окна')
        break

pages = 1
while pages<6:
    try:
        button = WebDriverWait(driver,30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'sel-hits-button-next'))
        )
        button.click()
        pages +=1
        print(f'переход на страницу {pages} произведен')
    except Exception as e:
        print(e)
        break

goods = driver.find_elements_by_class_name('product-tile-info')

goods_list = []
good_dict = {}
for good in goods:
    good_dict['descr'] = good.find_element_by_class_name('sel-product-tile-title').text
    good_dict['link'] = good.find_element_by_class_name('sel-product-tile-title').get_attribute('href')
    good_dict['price'] = good.find_element_by_class_name('product-price').text
    goods_list.append(good_dict)

for i in goods_list:
    print(i)