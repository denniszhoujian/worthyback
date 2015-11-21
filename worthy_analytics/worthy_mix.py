# encoding: utf-8

from datasys import dbhelper,crawler_helper
import math
import rows_helper
import time

col_worthyvalue_weight_dict_1 = {
            'discount_rate': 2.0,
            'max_deduction_ratio': 2.0,
            'deduction_score': 1.0,
            'discount': 1.0,
            'rf_ratio': 1.0,
            'gift_ratio': 0.3,
        }

col_worthyvalue_weight_dict_deduct_even = {
    'discount_rate': 1,
    'max_deduction_ratio': 1,
    'deduction_score': 1,
    'discount': 1,
    'rf_ratio': 1,
    'gift_ratio': 1,
}

col_worthyvalue_weight_dict_acitivity = {
    'discount_rate': 0,
    'max_deduction_ratio': 2.0,
    'deduction_score': 1.0,
    'discount': 1.0,
    'rf_ratio': 1.0,
    'gift_ratio': 0.3,
}

worthy_columns = [
    'sku_id',
    'this_update_time',
    'category_id',
    'category_name',
    'current_price',
    'average_price',
    'min_price',
    'max_price',
    'discount_rate',
    'a',
    'b',
    'c',
    'j',
    'l',
    'title',
    'thumbnail_url',
    'icon_url',
    'content_deduction',
    'adurl_deduction',
    'is_repeat',
    'reach',
    'deduction',
    'max_deduction',
    'dr_ratio',
    'maxp_ratio',
    'max_deduction_ratio',
    'deduction_score', # added 1121
    'content_discount',
    'adurl_discount',
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
    'comment_count',
    'rating_score',
    'category_rating_score',
    'rating_score_diff',
    'first_seen_date',

    'final_price',
    'final_discount', # added 1121

    'total_discount_rate',
    'activity_discount_rate',
    'worthy_value1',
]

def _get_merged_tables():
    sql = '''
    select
    a.sku_id as sku_id,
    CURRENT_TIMESTAMP() as this_update_time,
    a.category_id,
    h.name as category_name,
    a.current_price as current_price,
    a.average_price as average_price,
    a.min_price,
    a.max_price,
    a.discount_rate,
    a.a,
    a.b,
    a.c,
    a.j,
    a.l,

    b.title,
    b.thumbnail_url,
    b.icon_url,

    c.content as content_deduction,
    c.adurl as adurl_deduction,
    c.is_repeat,
    c.reach,
    c.deduction,
    c.max_deduction_ratio,
    c.dr_ratio,
    c.maxp_ratio,
    c.max_deduction,

    d.content as content_discount,
    d.adurl as adurl_discount,
    d.deduct_type,
    d.reach_num,
    d.discount,
    d.free_num,
    d.rf_ratio,

    e.gift_name,
    e.gift_num,
    e.gift_image,
    e.gift_sku_id,
    e.gift_price,
    e.gift_value,
    e.gift_ratio,

    f.comment_count,
    f.rating_score,
    f.category_rating_score,
    f.rating_score_diff,

    g.first_seen_date


    from

    jd_price_temp_latest a
    left join jd_item_dynamic_latest b
    on a.sku_id = b.sku_id

    left join jd_analytic_promo_deduction_max c
    on a.sku_id = c.sku_id

    left join jd_analytic_promo_discount_latest d
    on a.sku_id = d.sku_id

    left join jd_analytic_promo_gift_valued e
    on a.sku_id = e.sku_id

    left join jd_analytic_item_rating_diff f
    on a.sku_id = f.sku_id

    left join jd_item_firstseen g
    on a.sku_id = g.sku_id

    left join jd_category h
    on a.category_id = h.id

    where a.current_price > 0
    '''

    retrows = dbhelper.executeSqlRead(sql, is_dirty=True)
    return retrows


def _calculate_weighted_score(param_dict, weight_dict):
    value = float(1.0)
    for param in param_dict:
        score = float(param_dict[param])
        weight = float(weight_dict[param])
        try:
            value = value * math.pow(score,weight)
        except:
            print param
            print param_dict
            print weight_dict
    return value

def caculate_final_price(worthy_row, price=None):
    if price is None:
        val = worthy_row['current_price']
        price = float(val)

    # deduction
    could_deduct = 0
    reach  = worthy_row['reach']
    if reach is not None:
        if price >= reach and reach>0:
            is_repeat = worthy_row['is_repeat']
            deduction = worthy_row['deduction']
            max_deduction = worthy_row['max_deduction']

            if is_repeat:
                times = price // reach
            else:
                times = 1

            could_deduct = times * deduction
            if could_deduct > max_deduction:
                could_deduct = max_deduction

    deduct_discount_rate = 1.0
    try:
        deduct_discount_rate = (price*1.0-could_deduct*1.0)/price
    except Exception as e:
        print e
        print "price = %s" %price
        print "sku_id = %s" %worthy_row['sku_id']
        print "could_deduct = %s" %could_deduct

    # discount
    dr = 1.0
    reach_num = worthy_row['reach_num']
    if reach_num is not None:
        if reach_num == 1:
            dr = float(worthy_row['discount'])/10  # MUST DIVIDE BY 10
    final_dr = deduct_discount_rate if deduct_discount_rate <= dr else dr
    return final_dr * price


def _calculate_worthy_values(worthy_rows):
    for sku in worthy_rows:
        sku['final_price'] = caculate_final_price(sku,price=None)
        sku['final_discount'] = float(sku['final_price'])/float(sku['current_price'])
        if sku['is_repeat'] is not None:
            ds = float(sku['max_deduction_ratio'])
            if math.fabs(ds-0.000)<0.0001:
                ds1 = float(sku['maxp_ratio'])
                ds2 = float(sku['dr_ratio'])
                ds = ds1 * ds2
            sku['deduction_score'] = 1.000 - ds

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
            if sku[item] is not None:
                val  = float(sku[item])
                if val > 0.0:
                    param_dict[item] = val
                    # max_deduction should be 1 - X
                    if item in ['max_deduction_ratio']:
                        param_dict[item] = 1.0 - val
                    # there are cases where gift price is None, in db it's -1.
                    # generally these are not valuable, so make it 1.0 here.
                    if item in ['gift_ratio']:
                        val2 = 1.0 - val
                        if val2 < 0.2:
                            val2 = 0.2
                        param_dict[item] = val2


        # The most easy algorithm to calculate final worthy score
        value1 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_1)
        sku['worthy_value1'] = value1

        value2 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_acitivity)
        sku['activity_discount_rate'] = value2

        value3 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_deduct_even)
        sku['total_discount_rate'] = value3

    return 0


def generate_worthy_mix_main():

    t1 = time.time()
    print '1/4 >>> Join all related tables: price_temp, dynamic, deduction, discount, gift, rating, last-seen, etc...'
    worthy_rows = _get_merged_tables()
    t2 = time.time()
    print 'Done, using seconds: %s\n' %(t2-t1)

    print '2/4 >>> Calculating worthy scores and final price'
    _calculate_worthy_values(worthy_rows)
    t3 = time.time()
    print 'Done, using seconds: %s\n' %(t3-t2)

    print '3/4 >>> Generating data for db insert'
    insert_list = rows_helper.generate_list_for_db_write(worthy_rows, worthy_columns)
    t4 = time.time()
    print 'Done, using seconds: %s\n' %(t4-t3)

    print '4/4 >>> Now writing to db, rows = %s' %len(insert_list)
    ret = crawler_helper.persist_db_history_and_latest(
        table_name='jd_worthy',
        num_cols=len(insert_list[0]),
        value_list=insert_list,
        is_many=True,
        need_history=False,
    )
    t5 = time.time()
    print 'Done, using seconds: %s\n' %(t5-t4)

    return ret


if __name__ == "__main__":
    print generate_worthy_mix_main()