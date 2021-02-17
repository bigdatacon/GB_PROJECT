from func import *
import pandas as pd
import openpyxl
if __name__ == "__main__":
    with open("csvjs.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    """ Ограничиваю размер данных 5 компаниями для быстрого выполнения, по 700 компаниям прогружается ~80 минут, всего в базе 3200 компаний"""
    data = data[:3]
    """ обработка данных, добавление новых фичей и форматов"""
    list_all = prep_data(data)
    """Получаем список сгенерированных координат, данный список может быть больше при установке шага менее чем 0,02 но это влияет на скорость существеннее всего"""
    new_coords_list = get_new_spisok_coordinat(get_new_coordinates_lat(55.5751502, 55.9108559, 0.2),
                                               get_new_coordinates_long(37.3697764, 37.8415861, 0.2))
    new_coords_list = get_closer_metro_info_p(new_coords_list)
    """получаем данные по расстоянию до ближайшего конкурента для каждой компании"""
    list_all = get_closer_conquer(list_all)
    """получаем данные по расстоянию до ближайшего метро для каждой компании"""
    list_all = get_closer_metro_info(list_all)
    """получаем данные по площади в радиусе до конкурента и численности населения в радиусе до ближайшего конкурента """
    list_all = get_square(list_all)
    list_all_2 = list_all.copy()
    """ Получаем оценку и все данные по расстоянию до конкурента и метро, численности для вновь сгенеренных координат"""
    itog_list_coords = get_dots_all_info(new_coords_list, list_all)
    """ Подбираем из новых координат точек только те, у которых оценка раастояния до метро, конкурента, численности населения выше среднего"""
    itog_list_coords = get_itog_dots_list_with_options(itog_list_coords)
    """ добавляем списко новых координат которые удовлетворяют требованиям в итоговый список"""
    ITOGI = get_one_list_from_twoe(list_all_2, itog_list_coords)

    with open("ITOGI_fift_done.json", "w") as write_file:
        json.dump(ITOGI, write_file)
    print(f'WRITE FILE: {len(ITOGI)}')
    for i in ITOGI:
        print(i)
        print('--------------------------------------------------------')
    """запись данных в эксель файл"""
    df2 = pd.DataFrame(ITOGI).to_excel("ITOGI_FOR_MANY_POINS.xlsx")

    print('END')


