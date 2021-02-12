from func import *
categ = None
if __name__ == "__main__":
    with open("csvjs.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    """ограничиваем объем данных 2000 строками, всего данных в базе 3200"""
    data = data[:2000]
    list_all = prep_data(data)
    list_all = get_closer_conquer(list_all)
    list_all = get_closer_metro_info(list_all)
    list_all = get_square(list_all)

    try:
           with open("FOR_CHEK_SPISOK_TEK_KOORD_WITH_ALL_INFO.json", "w") as write_file:
               json.dump(list_all, write_file)
           print('SPIDOK COORDINAT ZAPISEN')
    except Exception as e:
           print('not write to file ')

    with open("FOR_CHEK_SPISOK_TEK_KOORD_WITH_ALL_INFO.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    pprint(data)









