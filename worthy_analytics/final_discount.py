# encoding: utf-8
from datasys import dbhelper,timeHelper
import rows_helper


def _get_deduction_dict():
    hours_ahead = timeHelper.getTimeAheadOfNowHours(36,format='%Y-%m-%d %H:%M:%S')

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

    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True)
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction


def _get_discount_dict():
    hours_ahead = timeHelper.getTimeAheadOfNowHours(36,format='%Y-%m-%d %H:%M:%S')

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
    # print sql_deduction

    retrows_deduction = dbhelper.executeSqlRead(sql_deduction, is_dirty=True)
    dict_deduction = rows_helper.transform_retrows_to_dict(retrows_deduction, 'sku_id')
    return dict_deduction


def _memory_left_join(tbl_left_as_rows, tbl_right_as_dict, col_name_list_left, col_name_list_right, key_col_name='sku_id'):
    vlist = []
    for row in tbl_left_as_rows:
        skuid = "%s" %row[key_col_name]
        if skuid in tbl_right_as_dict:
            vlist.append(dict(row,**tbl_right_as_dict[skuid]))
        else:
            vlist.append(row)

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

def match_discounts():

    sql_price = 'select * from jd_price_temp_latest'
    retrows_price = dbhelper.executeSqlRead(sql_price, is_dirty=True)
    print 'here1111111'
    deduction_dict = _get_deduction_dict()
    print 'here222222'
    cols = [
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
        'single_discount_rate',
        'category_id',
        'category_name',
        'content',
        'adurl',

    ]
    tlist = _memory_left_join(retrows_price,deduction_dict,
                              col_name_list_left=cols,
                              col_name_list_right=cols_deduction
                              )
    print 'here333333'
    print len(tlist)
    discount_dict = _get_discount_dict()
    print 'here44444'



    # write


import time
t1 = time.time()
match_discounts()
t2 = time.time()
print int(t2-t1)