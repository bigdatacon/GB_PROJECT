import pandas as pd
import numpy as np


def prefilter_items(data, take_n_popular=2000, item_features=None, user_features=None):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)

    top_popular = popularity[popularity['share_unique_users'] > 0.2].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]

    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.02].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]

    # Уберем товары, которые не продавались за последние 12 месяцев

    # Уберем не интересные для рекоммендаций категории (department)
    if item_features is not None:
        department_size = pd.DataFrame(item_features.\
                                        groupby('department')['item_id'].nunique().\
                                        sort_values(ascending=False)).reset_index()

        department_size.columns = ['department', 'n_items']
        rare_departments = department_size[department_size['n_items'] < 150].department.tolist()
        items_in_rare_departments = item_features[item_features['department'].isin(rare_departments)].item_id.unique().tolist()

        data = data[~data['item_id'].isin(items_in_rare_departments)]


    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    data['price'] = data['sales_value'] / (np.maximum(data['quantity'], 1))
    data = data[data['price'] > 2]

    # Уберем слишком дорогие товарыs
    data = data[data['price'] < 50]

    # Возбмем топ по популярности
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)

    top = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
    
    # Заведем фиктивный item_id (если юзер покупал товары из топ-5000, то он "купил" такой товар)
    data.loc[~data['item_id'].isin(top), 'item_id'] = 999999
    
    # ...
    
    
    ###Делаю мерджи всех таблиц чтобы было больше эмбедингов (не знаю будет работать или нет) 
    data = data.merge(user_features, on='user_id', how='left')
    data = data.merge(item_features, on='item_id', how='left')
    
    ### То что в кавычках потом удалить
    return data





def new_user_feat(data, user_features):
    user_features.columns = [col.lower() for col in user_features.columns]

    user_features.rename(columns={'household_key': 'user_id'}, inplace=True)
    #ТУТ НОВОВВЕДЕНИЯ 
    """Новые признаки для пользователей"""
    # data['price']=data['sales_value']/data['quantity']
    new_user_features = user_features.merge(data, on='user_id', how='left')



    ##### Обычное время покупки
    time = new_user_features.groupby('user_id')['trans_time'].mean().reset_index()
    time.rename(columns={'trans_time': 'mean_time'}, inplace=True)
    time = time.astype(np.float32)
    user_features = user_features.merge(time, how='left')


    ##### Возраст
    user_features['age'] = user_features['age_desc'].replace(
        {'65+': 70, '45-54': 50, '25-34': 30, '35-44': 40, '19-24':20, '55-64':60}
    )
    user_features = user_features.drop('age_desc', axis=1)


    ##### Доход
    user_features['income'] = user_features['income_desc'].replace(
        {'35-49K': 45,
     '50-74K': 70,
     '25-34K': 30,
     '75-99K': 95,
     'Under 15K': 15,
     '100-124K': 120,
     '15-24K': 20,
     '125-149K': 145,
     '150-174K': 170,
     '250K+': 250,
     '175-199K': 195,
     '200-249K': 245}
    )
    user_features = user_features.drop('income_desc', axis=1)


    ##### Дети
    user_features['kids'] = 0
    user_features.loc[(user_features['kid_category_desc'] == '1'), 'kids'] = 1
    user_features.loc[(user_features['kid_category_desc'] == '2'), 'kids'] = 2
    user_features.loc[(user_features['kid_category_desc'] == '3'), 'kids'] = 3
    user_features = user_features.drop('kid_category_desc', axis=1)


    ##### Средний чек, средний чек в неделю
    basket = new_user_features.groupby(['user_id'])['price'].sum().reset_index()

    baskets_qnt = new_user_features.groupby('user_id')['basket_id'].count().reset_index()
    baskets_qnt.rename(columns={'basket_id': 'baskets_qnt'}, inplace=True)

    average_basket = basket.merge(baskets_qnt)

    average_basket['average_basket'] = average_basket.price / average_basket.baskets_qnt
    average_basket['sum_per_week'] = average_basket.price / new_user_features.week_no.nunique()

    average_basket = average_basket.drop(['price', 'baskets_qnt'], axis=1)
    user_features = user_features.merge(average_basket, how='left')
    

    
    check = data.groupby('user_id')['sales_value'].sum().reset_index()
    check['check_day'] = check['sales_value']/new_user_features.week_no.nunique()

    quant = data.groupby('user_id')['quantity'].sum().reset_index()
    quant['day_qaunt'] = quant['quantity']/new_user_features.week_no.nunique()


    frequency = data.groupby('user_id')['day'].count().reset_index()
    frequency['day'] = frequency['day']/new_user_features.week_no.nunique()
    avg = data.groupby('user_id')['price'].mean().reset_index()
    avg.rename(columns={'price': 'avg_check'}, inplace=True)
    
    
    
    user_features=user_features.merge(avg, on='user_id', how='left')
    user_features=user_features.merge(frequency, on='user_id', how='left')

    user_features=user_features.merge(quant, on='user_id', how='left')
    user_features=user_features.merge(check, on='user_id', how='left')
    user_features.fillna(0.0, inplace=True)
    return user_features

def new_item_feat(data, item_features):
    item_frequency = data.groupby('item_id')['day'].count().reset_index()

    # item_features=item_features.merge(data, on='item_id', how='left')

    ### ТУТ НОВОВОВВЕДЕНИЯ 

    """Новые признаки для продуктов"""
    new_item_features = item_features.merge(data, on='item_id', how='left')
    item_frequency['day'] = item_frequency ['day']/new_item_features.week_no.nunique()
    item_features=item_features.merge(item_frequency, on='item_id', how='left')

    ##### discount
    mean_disc = new_item_features.groupby('item_id')['coupon_disc'].mean().reset_index().sort_values('coupon_disc')
    item_features = item_features.merge(mean_disc, on='item_id', how='left')

    ###### manufacturer
    rare_manufacturer = item_features.manufacturer.value_counts()[item_features.manufacturer.value_counts() < 50].index
    item_features.loc[item_features.manufacturer.isin(rare_manufacturer), 'manufacturer'] = 999999999
    item_features.manufacturer = item_features.manufacturer.astype('object')

    ##### 1 Количество продаж и среднее количество продаж товара
    item_qnt = new_item_features.groupby(['item_id'])['quantity'].count().reset_index()
    item_qnt.rename(columns={'quantity': 'quantity_of_sales'}, inplace=True)

    item_qnt['quantity_of_sales_per_week'] = item_qnt['quantity_of_sales'] / new_item_features['week_no'].nunique()
    item_features = item_features.merge(item_qnt, on='item_id', how='left')

    ##### 2 Среднее количество продаж товара в категории в неделю
    items_in_department = new_item_features.groupby('department')['item_id'].count().reset_index().sort_values(
        'item_id', ascending=False
    )
    items_in_department.rename(columns={'item_id': 'items_in_department'}, inplace=True)

    qnt_of_sales_per_dep = new_item_features.groupby(['department'])['quantity'].count().reset_index().sort_values(
        'quantity', ascending=False
    )
    qnt_of_sales_per_dep.rename(columns={'quantity': 'qnt_of_sales_per_dep'}, inplace=True)

    items_in_department = items_in_department.merge(qnt_of_sales_per_dep, on='department')
    items_in_department['qnt_of_sales_per_item_per_dep_per_week'] = (
            items_in_department['qnt_of_sales_per_dep'] /
            items_in_department['items_in_department'] /
            new_item_features['week_no'].nunique()
    )
    items_in_department = items_in_department.drop(['items_in_department'], axis=1)
    item_features = item_features.merge(items_in_department, on=['department'], how='left')

    ##### sub_commodity_desc
    items_in_department = new_item_features.groupby('sub_commodity_desc')['item_id'].count().reset_index().sort_values(
        'item_id', ascending=False
    )
    items_in_department.rename(columns={'item_id': 'items_in_sub_commodity_desc'}, inplace=True)

    qnt_of_sales_per_dep = new_item_features.groupby(['sub_commodity_desc'])[
        'quantity'].count().reset_index().sort_values(
        'quantity', ascending=False
    )
    qnt_of_sales_per_dep.rename(columns={'quantity': 'qnt_of_sales_per_sub_commodity_desc'}, inplace=True)

    items_in_department = items_in_department.merge(qnt_of_sales_per_dep, on='sub_commodity_desc')
    items_in_department['qnt_of_sales_per_item_per_sub_commodity_desc_per_week'] = (
            items_in_department['qnt_of_sales_per_sub_commodity_desc'] /
            items_in_department['items_in_sub_commodity_desc'] /
            new_item_features['week_no'].nunique()
    )
    items_in_department = items_in_department.drop(['items_in_sub_commodity_desc'], axis=1)
    item_features = item_features.merge(items_in_department, on=['sub_commodity_desc'], how='left')
    item_features.fillna(0.0, inplace=True)
    return item_features 



def get_important_features(model, X_train, y_train):
    """Список важных признаков"""
    model.fit(X_train, y_train)
    feature_imp = list(zip(X_train.columns.tolist(), model.feature_importances_))
    feature_imp = pd.DataFrame(feature_imp, columns=['feature', 'value'])
    basic_feats = feature_imp.loc[feature_imp.value > 0, 'feature'].tolist()
    return basic_feats


def postfilter_items(items, items_info, bought, most_popular_items , department_price, department_quantity, N=5):
    def get_department(i):
        department = items_info[items_info['item_id'] == i]['department'].values[0]
        return department

#     not_cheap_items = items_info[items_info['price'] > 1.0]
    not_cheap_items = items_info[(items_info['price'] > 1.0) & (items_info['price']  < 5) & (items_info['day_avg']  > 22.0)]
    item_ids = pd.DataFrame(items, columns=['item_id'])
    never_bought_items = item_ids[~item_ids['item_id'].isin(bought)]['item_id'].values.tolist()
#     never_bought_items= never_bought_items(never_bought_items['price'] > 1.0) & (never_bought_items['price']  < 1.7))
    expensive_items =  item_ids.merge(items_info[(items_info['price']>7) & (items_info['price']<15)], on='item_id', how='right').head(5)['item_id'].values.tolist()
   
    categories_used = []
    final_recommendations = []
   
    expensive_item_id = expensive_items[0]
    final_recommendations.append(expensive_item_id)
    categories_used.append(get_department(expensive_item_id))

   
    for i in items:
        if any(not_cheap_items[not_cheap_items['item_id'] == i]['price']):
            if  get_department(i) not in categories_used:
                vals = department_price[department_price['department'] == get_department(i)].values
                quantity = department_quantity[department_quantity['department'] == get_department(i)].values
                if vals.shape[0] == 1 and quantity.shape[0] ==1:
                    average_price = vals[0,1]
                    average_quantity = quantity[0,1]
#                     print('average_quantity:i ', average_quantity, i)
                    if average_price <= float(not_cheap_items[not_cheap_items['item_id'] == i]['price']) and average_quantity >= 25:
                        final_recommendations.append(i)
                        categories_used.append( get_department(i))
        if len(final_recommendations) == 3:
            break
            ### and average_quantity >=float(not_cheap_items[not_cheap_items['item_id'] == i]['day'])
# average_quantity <=float(not_cheap_items.groupby([not_cheap_items['item_id']==i, 'department'])['day'].mean().reset_index()) \
#                                              and 
    for i in never_bought_items:
        if any(not_cheap_items[not_cheap_items['item_id'] == i]['price']):
            if  get_department(i) not in categories_used:
                final_recommendations.append(i)
                categories_used.append( get_department(i))
        if len(final_recommendations) == 5:
            break
    

    
    if len(final_recommendations) < 5:      
        for i in most_popular_items:
            if True:
                if  get_department(i) not in categories_used:
                    final_recommendations.append(i)
                    categories_used.append( get_department(i))
            if len(final_recommendations) == 5:
                break            
       
    assert len(final_recommendations) == N, 'Количество рекомендаций = {}, должно быть {}'.format(len(final_recommendations), N)
    assert len(categories_used) == len(set(categories_used)), '{} уникальных категорий'.format(len(set(categories_used)))
    return final_recommendations


def add_feat_itm(data, item_features):    
    data_1 = data.merge(item_features, on='item_id', how='left')

    data_1 = data_1.rename(columns={'day_x': 'day'}) 
    data_1.columns

    ## Количество продаж товара 

    df_5 = data_1.groupby(['item_id', 'sub_commodity_desc']).agg({'quantity': 'sum'}) \
    .reset_index().rename(columns={'quantity': 'item_quantity_for_category'}) 

    df_5=df_5.drop('sub_commodity_desc' , axis=1).sort_values('item_quantity_for_category', ascending = False)

    # Сумма продаж по производителю 
    df_6 = data_1.groupby(['item_id', 'manufacturer']).agg({'sales_value': 'sum'}) \
    .reset_index().rename(columns={'sales_value': 'item_sales_for_dep'}) 
    df_6=df_6.drop('manufacturer' , axis=1).sort_values('item_sales_for_dep', ascending = False)

    item_features = item_features.merge(df_6, on='item_id', how='left')

    # Средняя частота покупки товара в неделю 
    freq_itm = data.groupby('item_id')['day'].unique()
    freq_itm = pd.DataFrame(freq_itm)
    freq_itm['diff_itm']=freq_itm['day'].apply(lambda x: np.diff(x, axis=0))
    freq_itm['average_freq_itm'] = freq_itm['diff_itm'].apply(lambda x: np.mean(x, axis=0))
    freq_itm['nd_from_la_pur_itm'] = freq_itm['day'].apply(lambda x: 666 - x[-1:][0])
    freq_itm
    item_features.shape
    item_features=item_features.merge(freq_itm, on='item_id', how = 'left')
    item_features.shape
    item_features
    item_features= item_features.fillna(0)
    item_features.columns
    item_features = item_features.drop(['day_y', 'diff_itm'], axis=1)
    return item_features


def add_feat_user(data, user_features):   
    ### Средняя частота покупок в неделю
    freq_my = data.groupby('user_id')['day'].unique()
    freq_my = pd.DataFrame(freq_my)
    freq_my['day'].apply(lambda x: np.diff(x, axis=0))
    freq_my['diff'] = freq_my['day'].apply(lambda x: np.diff(x, axis=0))
    freq_my
    freq_my['nd_from_la_pur'] = freq_my['day'].apply(lambda x: 666 - x[-1:][0])
    freq_my['average_freq_user'] = freq_my['diff'].apply(lambda x: np.mean(x, axis=0))
    user_features=user_features.merge(freq_my, on='user_id', how = 'left')
    user_features.shape
    user_features= user_features.fillna(0)
    user_features = user_features.drop(['day_x', 'day_y', 'diff'], axis=1)
    
    #1 Средний купон дискаунт юзера
    df_1 = data.groupby(['user_id']).agg({'coupon_disc': 'mean'}) \
        .reset_index().rename(columns={'coupon_disc': 'user_avg_coupon_disc'})

    user_features = user_features.merge(df_1, on='user_id', how='left')
    #2 Средений чек юзера
    df_2 = data.groupby(['user_id']).agg({'sales_value': 'mean'}) \
        .reset_index().rename(columns={'sales_value': 'user_avg_chek'})

    user_features = user_features.merge(df_2, on='user_id', how='left')

    ## Cредняя частота покупок юзером 
    df_3 = data.groupby(['user_id']).agg({'basket_id': 'count'}) \
        .reset_index().rename(columns={'basket_id': 'user_purch_week'}) 
    df_3['user_avg_day_for_purch'] = df_3['user_purch_week']/666
    df_3.drop('user_purch_week', axis=1)

    user_features = user_features.merge(df_3, on='user_id', how='left')
    return user_features