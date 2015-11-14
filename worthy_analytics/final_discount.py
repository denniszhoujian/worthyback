# encoding: utf-8
from datasys import dbhelper,timeHelper,crawler_helper
import rows_helper
import math

FINAL_DISCOUNT_RECENCY_HOURS = 36

col_worthyvalue_weight_dict_1 = {
            'discount_rate': 1,
            'max_deduction_ratio': 1.3,
            'discount': 1,
            'rf_ratio': 1,
            'gift_ratio': 0.5,
        }

col_worthyvalue_weight_dict_deduct_even = {
    'discount_rate': 1,
    'max_deduction_ratio': 1,
    'discount': 1,
    'rf_ratio': 1,
    'gift_ratio': 1,
}

col_worthyvalue_weight_dict_acitivity = {
    'discount_rate': 0,
    'max_deduction_ratio': 1.3,
    'discount': 1,
    'rf_ratio': 1,
    'gift_ratio': 0.7,
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
        'content',
        'adurl',
        'title',
        'price',
        'is_repeat',
        'reach',
        'deduction',
        'max_deduction',
        'dr_ratio',
        'maxp_ratio',
        'max_deduction_ratio',
        'category_name',


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

        'first_seen_date',

        'comment_count',
        'rating_score',
        'category_rating_score',
        'rating_score_diff',
        'rate_1',
        'category_rate_1',
        'rate_1_diff',
        'rate_good',
        'category_rate_good',
        'rate_good_diff',

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

def _get_item_firstseen_dict():
    sql_deduction = '''
        select sku_id,first_seen_date from jd_item_firstseen
    '''
    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True)
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction

def _get_rating_dict():
    sql_deduction = '''
        select * from jd_analytic_item_rating_diff
    '''
    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True)
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
        i = 0
        for name in col_name_list_left:
            tp.append(rdict[name])
            # print "%s\t%s" %(i,name)
            i+=1
        for name in col_name_list_right:
            # print "%s\t%s" %(i,name)
            i+=1
            if name in rdict:
                tp.append(rdict[name])
            else:
                tp.append(None)
        tlist.append(tp)
        # print tp
        # print len(tp)
        # exit()
    return tlist

def _merge_dict_under_key(dict_change, copy_dict_list):
    for key in dict_change:
        for dict_copy in copy_dict_list:
            if key in dict_copy:
                cdict = dict_change[key]
                for kk in dict_copy[key]:
                    cdict[kk] = dict_copy[key][kk]
    return 0

def _get_column_index(col_name):
    col_list = cols_left + cols_deduction
    offset = col_list.index(col_name)
    return offset

def _calculate_weighted_score(param_dict, weight_dict):
    value = float(1.0)
    for param in param_dict:
        score = param_dict[param]
        weight = weight_dict[param]
        value = value * math.pow(score,weight)
    return value

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

    print('>>> 1/8 >>> Reading jd_price_temp_latest...')
    sql_price = 'select * from jd_price_temp_latest'
    retrows_price = dbhelper.executeSqlRead(sql_price, is_dirty=True)
    print('rows read: %s' %len(retrows_price))

    print('>>> 2/8 >>> Reading strongest deductions of each sku...')
    deduction_dict = _get_deduction_dict()
    print('rows read: %s' %len(deduction_dict))

    print('>>> 3/8 >>> Reading discounts of each sku...')
    discount_dict = _get_discount_dict()
    print('rows read: %s' %len(discount_dict))

    print('>>> 4/8 >>> Reading gifts of each sku...')
    gift_dict = _get_gift_dict()
    print('rows read: %s' %len(gift_dict))

    print('>>> 5/8 >>> Reading first seen date of each sku...')
    first_seen_dict = _get_item_firstseen_dict()
    print('rows read: %s' %len(first_seen_dict))

    print('>>> 6/8 >>> Reading ratings of each sku...')
    rating_dict = _get_rating_dict()
    print('rows read: %s' %len(rating_dict))

    print('>>> 7/8 >>> Joining results in memory...')

    _merge_dict_under_key(
        deduction_dict,
        [
            discount_dict,
            gift_dict,
            first_seen_dict,
            rating_dict,
        ]
    )

    tlist = _memory_left_join(retrows_price,deduction_dict,
                              col_name_list_left=cols_left,
                              col_name_list_right=cols_deduction
                              )
    print('rows generated: %s' %len(tlist))

    print '>>> 8/8 >>> Calculating worhty_values...'
    _calculate_worthy_values(tlist)
    print 'num cols = %s ' %len(tlist[0])

    print '>>> 9/9 >>> Saving to DB...'
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