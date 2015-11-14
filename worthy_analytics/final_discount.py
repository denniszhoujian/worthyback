# encoding: utf-8
from datasys import dbhelper,timeHelper,crawler_helper
import rows_helper

FINAL_DISCOUNT_RECENCY_HOURS = 36

col_worthyvalue_weight_dict_1 = {
            'discount_rate': 100,
            'max_deduction_ratio': 130,
            'discount': 100,
            'rf_ratio': 100,
            'gift_ratio': 30,
        }

col_worthyvalue_weight_dict_deduct_even = {
    'discount_rate': 100,
    'max_deduction_ratio': 100,
    'discount': 100,
    'rf_ratio': 100,
    'gift_ratio': 100,
}

col_worthyvalue_weight_dict_acitivity = {
    'discount_rate': 0,
    'max_deduction_ratio': 130,
    'discount': 100,
    'rf_ratio': 100,
    'gift_ratio': 30,
}

cols_left = [
        'sku_id',
        'current_price',
        'average_price',
        'min_price',
        'max_price',
        'price_m',
        'discount_rate',
        'update_date',
        'a',
        'b',
        'c',
        'j',
        'l',
        'stock_update_time',
        'category_id'
    ]
cols_deduction = [
        'pid',
        'code',
        'name',
        'title',
        'price',
        'is_repeat',
        'reach',
        'deduction',
        'max_deduction',
        'dr_ratio',
        'maxp_ratio',
        'max_deduction_ratio',
        'category_id',
        'category_name',
        'code',
        'content',
        'adurl',

        'deduct_type',
        'reach_num',
        'discount',
        'free_num',
        'rf_ratio',

        'gift_name',
        'gift_num',
        'gift_image',
        'gift_sku_id',
        'gift_price',
        'gift_value',
        'gift_ratio',

        'total_discount_rate',
        'activity_discount_rate',
        'worthy_value1',
        'worthy_value2', #reserved
        'price1', # reserved
        'price2', # reserved
    ]

def _get_deduction_dict():
    hours_ahead = timeHelper.getTimeAheadOfNowHours(FINAL_DISCOUNT_RECENCY_HOURS,format='%Y-%m-%d %H:%M:%S')

    sql_deduction = '''
        select * from
        (
        select
        sku_id,
        max(single_discount_rate) as max_deduction_ratio
        FROM
        jd_analytic_promo_deduction_latest
        group by sku_id
        -- having max(single_discount_rate)>0
        ) a

        left join

        jd_analytic_promo_deduction_latest b

        on
        a.sku_id = b.sku_id
        and ABS(a.max_deduction_ratio-b.single_discount_rate)<0.001

        where origin_time>'%s'
    ''' %hours_ahead

    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True, isolation_type='read-committed')
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction


def _get_discount_dict():
    hours_ahead = timeHelper.getTimeAheadOfNowHours(FINAL_DISCOUNT_RECENCY_HOURS,format='%Y-%m-%d %H:%M:%S')

    sql_deduction = '''
        select * from
        jd_analytic_promo_discount_latest
        where origin_dt>'%s'
    ''' %hours_ahead
    # print sql_deduction

    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True, isolation_type='read-committed')
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction


def _get_gift_dict():
    hours_ahead = timeHelper.getTimeAheadOfNowHours(FINAL_DISCOUNT_RECENCY_HOURS,format='%Y-%m-%d %H:%M:%S')
    # gift_valued表中, dt是原始爬取时间(其他表是origin_time)
    sql_deduction = '''
        select * from
        jd_analytic_promo_gift_valued
        where dt>'%s'
    ''' %hours_ahead
    # print sql_deduction

    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True, isolation_type='read-committed')
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction

def _memory_left_join(tbl_left_as_rows, tbl_right_as_dict, col_name_list_left, col_name_list_right, key_col_name='sku_id'):
    # first, join left retrows with right as dict using dict-key, returning a dict
    vlist = []
    for row in tbl_left_as_rows:
        skuid = "%s" %row[key_col_name]
        if skuid in tbl_right_as_dict:
            vlist.append(dict(row,**tbl_right_as_dict[skuid]))
        else:
            vlist.append(row)

    # second, turn the dict into a db-insert-able list
    tlist = []
    for rdict in vlist:
        tp = []
        for name in col_name_list_left:
            tp.append(rdict[name])
        for name in col_name_list_right:
            if name in rdict:
                tp.append(rdict[name])
            else:
                tp.append(None)
        tlist.append(tp)

    return tlist

def _get_column_index(col_name):
    col_list = cols_left + cols_deduction
    offset = col_list.index(col_name)
    return offset

def _calculate_weighted_score(param_dict, weight_dict):
    value = float(1.0)
    sum_weight = float(0.0)
    sum_score = float(0.0)
    for param in param_dict:
        score = param_dict[param]
        weight = weight_dict[param]
        sum_weight += weight
        sum_score += score*weight
    weighted_score = sum_score/sum_weight
    return weighted_score

# sku_info_list: format [(cols)]
def _calculate_worthy_values(sku_info_list):
    for sku in sku_info_list:

        col_name_list = [
            'discount_rate',
            'max_deduction_ratio',
            'discount',
            'rf_ratio',
            'gift_ratio',
        ]

        param_dict = {}
        for item in col_name_list:
            param_dict[item] = 1.0
            index = _get_column_index(item)
            if sku[index] is not None:
                param_dict[item] = float(sku[index])
                if item=='max_deduction_ratio':
                    param_dict[item] = 1.0 - float(sku[index])

        # The most easy algorithm to calculate final worthy score
        value1 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_1)
        sku[_get_column_index('worthy_value1')] = value1

        value2 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_acitivity)
        sku[_get_column_index('activity_discount_rate')] = value2

        value3 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_deduct_even)
        sku[_get_column_index('total_discount_rate')] = value3

        # if value1<1:
        #     print
    return 0


def match_discounts():

    print('>>> 1/6 >>> Reading jd_price_temp_latest...')
    sql_price = 'select * from jd_price_temp_latest'
    retrows_price = dbhelper.executeSqlRead(sql_price, is_dirty=True)
    print('rows read: %s' %len(retrows_price))

    print('>>> 2/6 >>> Reading strongest deductions of each sku...')
    deduction_dict = _get_deduction_dict()
    print('rows read: %s' %len(deduction_dict))

    print('>>> 3/6 >>> Reading discounts of each sku...')
    discount_dict = _get_discount_dict()
    print('rows read: %s' %len(discount_dict))

    print('>>> 4/6 >>> Reading gifts of each sku...')
    gift_dict = _get_gift_dict()
    print('rows read: %s' %len(gift_dict))

    print('>>> 5/6 >>> Joining results in memory...')

    tlist = _memory_left_join(retrows_price,deduction_dict,
                              col_name_list_left=cols_left,
                              col_name_list_right=cols_deduction
                              )
    print('rows generated: %s' %len(tlist))

    print '>>> 6/6 >>> Calculating worhty_values...'
    _calculate_worthy_values(tlist)

    print 'Saving to DB...'
    ret = crawler_helper.persist_db_history_and_latest(
        table_name='jd_worthy',
        num_cols=len(tlist[0]),
        value_list=tlist,
        is_many=True,
        need_history=False
    )
    return ret


    # write

if __name__ == '__main__':
    import time
    t1 = time.time()
    match_discounts()
    t2 = time.time()
    print "time used: %s" %int(t2-t1)