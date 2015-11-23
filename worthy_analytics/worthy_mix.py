# encoding: utf-8

from datasys import dbhelper,crawler_helper
import math
import rows_helper
import time
from worthy_analytics import datamining_config

IS_SKU_LEVEL_DEBUGGING = False
DEBUG_SKU_ID = 188029

col_worthyvalue_weight_dict_deduct_even = {
    'discount_rate': 1,
    # 'max_deduction_ratio': 1,
    # 'deduction_score': 1,
    'deduction_final_score': 1.0,
    'discount': 1,
    'rf_ratio': 1,
    'gift_ratio': 1,
}

col_worthyvalue_weight_dict_acitivity = {
    'discount_rate': 0.0,
    # 'max_deduction_ratio': 1.0,
    # 'deduction_score': 0.8,
    'deduction_final_score': 1.0,
    'discount': 0.75,
    'rf_ratio': 0.6,
    'gift_ratio': 0.3,
}

worthy_columns = [
    'sku_id',
    'this_update_time',
    'category_id',
    'category_name',
    'current_price',
    'average_price',
    'median_price',
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
    'reach_2',
    'deduction_2',
    'max_dr_ratio',
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
    'sample_count',
    'catalog_id',   # added 1123
    'catalog_name',  # added 1123
]

def _get_merged_tables():
    sql = '''
    select
    a.sku_id as sku_id,
    CURRENT_TIMESTAMP() as this_update_time,
    j.category_id as category_id,
    h.name as category_name,
    b.price as current_price,
    a.average_price as average_price,
    a.median_price,
    a.min_price,
    a.max_price,
    b.price/a.median_price as discount_rate,
    k.a,
    k.b,
    k.c,
    k.j,
    k.l,
    b.title,
    b.thumbnail_url,
    b.icon_url,
    c.content as content_deduction,
    c.adurl as adurl_deduction,
    c.is_repeat,
    c.reach,
    c.deduction,
    c.max_deduction,
    c.dr_ratio,
    c.maxp_ratio,
    c.max_deduction_ratio,
    c.reach_2,
    c.deduction_2,
    c.max_dr_ratio,
    c.discount_score_2 as deduction_score,
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
    g.first_seen_date,
    a.sample_count

    from

    jd_analytic_price_stat_latest a
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

    left join jd_item_stock_latest k
    on a.sku_id = k.sku_id

    left join jd_item_category j
    on a.sku_id = j.sku_id

    left join jd_category h
    on j.category_id = h.id

    where b.price > 0
    '''

    if IS_SKU_LEVEL_DEBUGGING:
        sql += '\n and a.sku_id = %s' %DEBUG_SKU_ID

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
        cata_info = _get_catalogy_info_by_category_id(sku['category_id'])
        sku['catalog_id'] = cata_info['catalog_id'] if cata_info is not None else None
        sku['catalog_name'] = cata_info['catalog_name'] if cata_info is not None else None

        col_name_list = [
            'discount_rate',
            # 'max_deduction_ratio',
            # 'deduction_score',
            'deduction_final_score',
            'discount',
            'rf_ratio',
            'gift_ratio',
        ]

        deduction_score = 1.0
        d1 = sku['max_deduction_ratio']
        d2 = sku['deduction_score']
        if d1 is None:
            deduction_score = 1.0 - d2
        elif d2 is None:
            deduction_score = 1.0 - d1
        elif float(d1) > float(d2):
            deduction_score = 1.0 - d1
        else:
            deduction_score = 1.0 - (float(d1)+float(d2))/2.0

        param_dict = {}
        param_dict['deduction_final_score'] = deduction_score
        for item in col_name_list:
            param_dict[item] = 1.0
            if item not in sku:
                continue
            if sku[item] is not None:
                val  = float(sku[item])
                if val > 0.0:
                    param_dict[item] = val
                    # if item in ['deduction_score']:
                    #     param_dict[item] = 1.0 - val
                    # # max_deduction should be 1 - X
                    # also, max_deduction and deduction_score has overlap, need only one of them...
                    # if item in ['max_deduction_ratio']:
                    #     param_dict[item] = 1.0 - val
                        # if abs(float(sku['deduction_score']) - val) < 0.001:
                        #     param_dict['deduction_score'] = 1.0
                    # discount should be divided by 10
                    if item in ['discount']:
                        param_dict[item] = val / 10.0
                    # there are cases where gift price is None, in db it's -1.
                    # generally these are not valuable, so make it 1.0 here.
                    if item in ['gift_ratio']:
                        val2 = 1.0 - val
                        if val2 < datamining_config.MAX_GIFT_DISCOUNT:
                            val2 = datamining_config.MAX_GIFT_DISCOUNT
                        param_dict[item] = val2
                    # For reach-free, the larger the value of reach_num, the less valuable the deal is.
                    # so make the score less when reach_num goes higher.
                    if item in ['rf_ratio']:
                        reach_num = float(sku['reach_num'])
                        score = float(param_dict[item])
                        param_dict[item] = 1 - (1.0-score)/math.pow((reach_num-1.0),datamining_config.DISCOUNT_REACH_NUM_POWER_BASE)




        # The most easy algorithm to calculate final worthy score
        value1 = _calculate_weighted_score(param_dict, datamining_config.col_worthyvalue_weight_dict_1)
        sku['worthy_value1'] = value1

        value2 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_acitivity)
        sku['activity_discount_rate'] = value2

        value3 = _calculate_weighted_score(param_dict, col_worthyvalue_weight_dict_deduct_even)
        sku['total_discount_rate'] = value3

    return 0

global g_catalog_map
g_catalog_map = {}

def _load_catalog_map_as_dict_key_category_id_prefix():
    global g_catalog_map
    if len(g_catalog_map) > 0:
        return g_catalog_map

    sql = 'select * from jd_catalog_map'
    retrows = dbhelper.executeSqlRead(sql)
    cdict = rows_helper.transform_retrows_to_dict(retrows,'category_id')
    g_catalog_map = cdict
    return g_catalog_map

def _get_catalogy_info_by_category_id(category_id):
    cdict = _load_catalog_map_as_dict_key_category_id_prefix()
    for prefix in cdict:
        if prefix in category_id:
            return cdict[prefix]
    return None

def generate_worthy_mix_main():

    t1 = time.time()
    print '1/4 >>> Join all related tables: price_temp, dynamic, deduction, discount, gift, rating, last-seen, etc...'
    worthy_rows = _get_merged_tables()
    t2 = time.time()
    print 'Done, rows read: %s, using seconds: %s\n' %(len(worthy_rows), (t2-t1))

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