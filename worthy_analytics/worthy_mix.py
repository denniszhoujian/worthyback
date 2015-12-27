# encoding: utf-8

from datasys import dbhelper,crawler_helper
import time
import math
import rows_helper
from worthy_analytics import datamining_config
import logging

IS_SKU_LEVEL_DEBUGGING = False
DEBUG_SKU_ID = 617166

col_worthyvalue_weight_dict_deduct_even = {
    'discount_rate': 1,
    'deduction_final_score': 1.0,
    'discount': 1,
    'rf_ratio': 1,
    'gift_ratio': 1,
    'rating_score_diff': 0.0,
    'min_price_reached': 0.0,
}

col_worthyvalue_weight_dict_acitivity = {
    'discount_rate': 0.0,
    'deduction_final_score': 1.0,
    'discount': 0.75,
    'rf_ratio': 0.6,
    'gift_ratio': 0.3,
    'rating_score_diff': 0.0,
    'min_price_reached': 1.0,
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
    'min_price_reached',    # added 1130
    'this_update_date',     # added 1130
    'min_ratio',    # added 1220
    'LPDR',         # added 1220
]

def _get_merged_tables():
    sql = '''
    select
    a.sku_id as sku_id,
    CURRENT_TIMESTAMP() as this_update_time,
    j.category_id as category_id,
    h.name as category_name,
    pp.price as current_price,
    a.average_price as average_price,
    a.median_price,
    a.min_price,
    a.max_price,
    a.min_ratio,
    a.LPDR,
    pp.price/a.median_price as discount_rate,
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
    f.rating_sample_num as category_rating_score,
    f.percentile_rating_score as rating_score_diff,
    g.first_seen_date,
    a.sample_count,
    CURRENT_DATE() as this_update_date

    from

    jd_analytic_price_stat_latest a
    left join jd_item_price_latest pp
    on a.sku_id = pp.sku_id

    left join jd_item_dynamic_latest b
    on a.sku_id = b.sku_id

    left join jd_analytic_promo_deduction_max c
    on a.sku_id = c.sku_id

    left join jd_analytic_promo_discount_latest d
    on a.sku_id = d.sku_id

    left join jd_analytic_promo_gift_valued e
    on a.sku_id = e.sku_id

    left join jd_analytic_rating_percentile_latest f
    on a.sku_id = f.sku_id

    left join jd_item_firstseen g
    on a.sku_id = g.sku_id

    left join jd_item_stock_latest k
    on a.sku_id = k.sku_id

    left join jd_item_category j
    on a.sku_id = j.sku_id

    left join jd_category h
    on j.category_id = h.id

    where

    pp.price > 0
    and a.sku_id not in (select sku_id from jd_analytic_sku_gift)
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
            logging.error("Error in _calculate_weighted_score:")
            logging.error(param)
            logging.error(param_dict)
            logging.error(weight_dict)
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
        logging.error(e)
        logging.error("price = %s" %price)
        logging.error("sku_id = %s" %worthy_row['sku_id'])
        logging.error("could_deduct = %s" %could_deduct)

    # discount
    dr = 1.0
    reach_num = worthy_row['reach_num']
    if reach_num is not None:
        if reach_num == 1:
            dr = float(worthy_row['discount'])/10  # MUST DIVIDE BY 10
    final_dr = deduct_discount_rate if deduct_discount_rate <= dr else dr
    return final_dr * price


def _calculate_ladder_score(value, matrix):
    ret = None
    for key in matrix:
        ret = matrix[key]
        break
    for key in matrix:
        if value>=key:
            ret = matrix[key]
    return ret


def _calculate_worthy_values(worthy_rows):
    for sku in worthy_rows:
        sku['final_price'] = caculate_final_price(sku,price=None)
        sku['final_discount'] = float(sku['final_price'])/float(sku['current_price'])
        cata_info = _get_catalogy_info_by_category_id(sku['category_id'])
        sku['catalog_id'] = cata_info['catalog_id'] if cata_info is not None else None
        sku['catalog_name'] = cata_info['catalog_name'] if cata_info is not None else None
        # history lowest
        cur_price = int(sku['current_price'])
        min_price = int(sku['min_price'])
        max_price = int(sku['max_price'])
        median_price = int(sku['median_price'])
        LPDR = float(sku['LPDR'])
        min_ratio = float(sku['min_ratio'])
        sample_count = int(sku['sample_count'])
        sku['min_price_reached'] = 1
        if cur_price==min_price and min_price!=max_price and LPDR > datamining_config.SKU_MIN_PRICE_REACHED_MINIMUM_REQUIRED_DISCOUNT_RATE and min_ratio<0.1 and sample_count >= 14:
            sku['min_price_reached'] = 2

        # col_name_list = [
        #     'discount_rate',
        #     # 'max_deduction_ratio',
        #     # 'deduction_score',
        #     'deduction_final_score',
        #     'discount',
        #     'rf_ratio',
        #     'gift_ratio',
        #     'rating_score_diff',
        # ]
        col_name_list = []
        for param_key in datamining_config.col_worthyvalue_weight_dict_1:
            col_name_list.append(param_key)

        deduction_score = 1.0
        d1 = sku['max_deduction_ratio']
        d2 = sku['deduction_score']
        if d1 is None:
            d1 = 0
        if d2 is None:
            d2 = 0

        if float(d1) >= float(d2):
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
                if val > 0.0:   ###################### NOTE THIS ###################
                    param_dict[item] = val
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
                    if item in ['rating_score_diff']:
                        param_dict[item] = _calculate_ladder_score(val,datamining_config.RATING_PERCENTILE_SCORE_MATRIX)
                    if item in ['min_price_reached']:
                        param_dict[item] = _calculate_ladder_score(val,datamining_config.MIN_PRICE_REACHED_SCORE_MATRIX)


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
    logging.debug('1/4 >>> Join all related tables: price_temp, dynamic, deduction, discount, gift, rating, last-seen, etc...')
    worthy_rows = _get_merged_tables()
    t2 = time.time()
    logging.debug('Done, rows read: %s, using seconds: %s\n' %(len(worthy_rows), (t2-t1)) )

    logging.debug('2/4 >>> Calculating worthy scores and final price')
    _calculate_worthy_values(worthy_rows)
    t3 = time.time()
    logging.debug('Done, using seconds: %0.1f\n' %(t3-t2) )

    logging.debug('3/4 >>> Generating data for db insert')
    insert_list = rows_helper.generate_list_for_db_write(worthy_rows, worthy_columns)
    t4 = time.time()
    logging.debug('Done, using seconds: %0.1f\n' %(t4-t3) )

    logging.debug('4/4 >>> Now writing to db, rows = %s' %len(insert_list) )

    tbl_name = 'jd_worthy'
    # tbl_name = 'zz_worthy_%s' %int(time.time())
    # tbl_name_latest = "%s_latest" %tbl_name

    # ret = crawler_helper.persist_db_history_and_lastest_empty_first(
    ret = crawler_helper.persist_db_history_and_latest(
        table_name=tbl_name,
        num_cols=len(insert_list[0]),
        value_list=insert_list,
        is_many=True,
        need_history=False,  ##### WAS TRUE, why we need it?
        # sql_create_table=getWorthySqlCreateTable(tbl_name_latest),
    )

    # logging.debug('Now altering table name...')
    # afr = dbhelper.rename_table(tbl_name_latest, 'jd_worthy_latest', if_delete_duplicate=True)

    t5 = time.time()
    logging.debug('Done, using seconds: %0.1f\n' %(t5-t4))

    return ret

def getWorthySqlCreateTable(tbl_name):
    sqlcb = '''
    CREATE TABLE %s (
      sku_id bigint(20) NOT NULL,
      this_update_time datetime NOT NULL,
      category_id varchar(255) NOT NULL,
      category_name varchar(255) DEFAULT NULL,
      current_price float NOT NULL,
      average_price float NOT NULL,
      median_price float NOT NULL,
      min_price float NOT NULL,
      max_price float NOT NULL,
      discount_rate float DEFAULT NULL,
      a int(11) DEFAULT NULL,
      b int(11) DEFAULT NULL,
      c int(11) DEFAULT NULL,
      j int(11) DEFAULT NULL,
      l int(11) DEFAULT NULL,
      title varchar(255) DEFAULT NULL,
      thumbnail_url varchar(255) DEFAULT NULL,
      icon_url varchar(255) DEFAULT NULL,
      content_deduction varchar(255) DEFAULT NULL,
      adurl_deduction varchar(255) DEFAULT NULL,
      is_repeat tinyint(255) DEFAULT NULL,
      reach float DEFAULT NULL,
      deduction float DEFAULT NULL,
      max_deduction float DEFAULT NULL,
      dr_ratio float DEFAULT NULL,
      maxp_ratio float DEFAULT NULL,
      max_deduction_ratio float DEFAULT NULL,
      reach_2 float DEFAULT NULL,
      deduction_2 float DEFAULT NULL,
      max_dr_ratio float DEFAULT NULL,
      deduction_score float DEFAULT NULL,
      content_discount varchar(255) DEFAULT NULL,
      adurl_discount varchar(255) DEFAULT NULL,
      deduct_type smallint(6) DEFAULT NULL,
      reach_num smallint(6) DEFAULT NULL,
      discount float DEFAULT NULL,
      free_num smallint(6) DEFAULT NULL,
      rf_ratio float DEFAULT NULL,
      gift_name varchar(255) DEFAULT NULL,
      gift_num int(11) DEFAULT NULL,
      gift_image varchar(255) DEFAULT NULL,
      gift_sku_id bigint(20) DEFAULT NULL,
      gift_price float DEFAULT NULL,
      gift_value float DEFAULT NULL,
      gift_ratio float DEFAULT NULL,
      comment_count int(11) DEFAULT NULL,
      rating_score float DEFAULT NULL,
      category_rating_score float DEFAULT NULL,
      rating_score_diff float DEFAULT NULL,
      first_seen_date date DEFAULT NULL,
      final_price float DEFAULT NULL,
      final_discount float DEFAULT NULL,
      total_discount_rate float DEFAULT NULL,
      activity_discount_rate float DEFAULT NULL,
      worthy_value1 float DEFAULT NULL,
      sample_count int(11) DEFAULT NULL,
      catalog_id bigint(20) DEFAULT NULL,
      catalog_name varchar(255) DEFAULT NULL,
      min_price_reached tinyint(4) NOT NULL,
      this_update_date date NOT NULL,
      min_ratio float NOT NULL,
      LPDR float NOT NULL,
      PRIMARY KEY (sku_id),
      KEY sku (sku_id),
      KEY worthy1 (worthy_value1),
      KEY cur_price (current_price),
      KEY cataid (catalog_id),
      KEY stock_a (a)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ''' %tbl_name
    return sqlcb


if __name__ == "__main__":
    from tasks import task_logging
    task_logging.configLogging('worthy_mix')
    print generate_worthy_mix_main()
    print int(time.time())