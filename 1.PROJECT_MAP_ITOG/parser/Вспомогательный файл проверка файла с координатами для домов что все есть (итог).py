place = "Москва, ул. Вавилова, д. 44, к. 3"
import googlemaps
import pandas as pd
import json
import pprint

from datetime import datetime
"""Это работает """
# gmaps = googlemaps.Client(key='AIzaSyDepsv_CnygZyJEtiUUaAs495UaRCBxPg0')
# geocode_result = gmaps.geocode(place)
# print(geocode_result)

"""Прочитать файл"""
# with open("gosjkh.json", "r", encoding='utf-8') as read_file:
#     data = json.load(read_file)
#
# # for i in data:
# #     print(i)
# # pprint(data)
# df = pd.DataFrame(data)
# # print(df.columns)
# # print(df.isna().sum())
# # print(df.groupby('Зарегистрировано жителей').size())
# df['Зарегистрировано жителей'] = df['Зарегистрировано жителей'].replace('—', 274.00)
# # print(df)
# # rslt_df = df[df['Зарегистрировано жителей'] == '—']
# # print(rslt_df['Зарегистрировано жителей'])
# # df.to_csv('file1.csv')
# # print('записано')
#
# import json
# json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
# with open("houses_obrabotannie.json", "w") as write_file:
#     json.dump(json_list, write_file)




""" чтение из csv файла """
# import csv
# with open("file1.csv", encoding='utf-8') as r_file:
#     # Создаем объект reader, указываем символ-разделитель ","
#     file_reader = csv.reader(r_file, delimiter = ",")
#     # Счетчик для подсчета количества строк и вывода заголовков столбцов
#
#     for i in file_reader:
#         print(i)

# with open("houses_obrabotannie.json", "r", encoding='utf-8') as read_file:
#     data = json.load(read_file)

with open("ITOG_NEW_COORDS_WITH_ALL_INFO_24.02.2020_s_old.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)


pprint(data)