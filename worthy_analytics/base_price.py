# encoding: utf-8

from datasys import dbhelper, timeHelper
import time

def calculate_price_table():
    """
    sql = '''
    replace into
    jd_price
    select sku_id,
    price as current_price,
    AVG(price) as average_price,
    min(price) as min_price,
    max(price) as max_price,
    max(price_m) as price_m,
    price/max(price) as discount_rate
    from jd_item_dynamic
    where update_date > '2015-10-20'
    group by sku_id

    '''
    """

    dt4 = timeHelper.getTimeAheadOfNowDays(4)
    dt2 = timeHelper.getTimeAheadOfNowDays(2)
    sql = '''

    replace into jd_price_temp

    select
    h.sku_id as sku_id,
    h.current_price as current_price,
    h.average_price as average_price,
    h.min_price as min_price,
    h.max_price as max_price,
    h.price_m  as price_m,
    h.discount_rate as discount_rate,
    h.update_date as update_date,
    b.a as a,
    b.b as b,
    b.c as c,
    b.j as j,
    b.l as l,
    b.stock_json as stock_json,
    b.update_time as stock_update_time,
    c.category_id as category_id,
    -- d.ads_json as ads_json,
    -- d.promo_json as promo_json,
    -- d.quan_json as quan_json,
    -- d.dt as promo_dt,
    -- f.ads_json as cat_ads_json,
    -- f.promo_json as cat_promo_json,
    -- f.quan_json as cat_quan_json,
    -- f.dt as cat_promo_dt
    "","","",""

    from

    (
        select sku_id,
        price as current_price,
        AVG(price) as average_price,
        min(price) as min_price,
        max(price) as max_price,
        max(price_m) as price_m,
        price/max(price) as discount_rate,
        max(update_date) as update_date

        from
        jd_item_dynamic
        where
        update_date > '2015-10-20'

        group by sku_id
        having max(update_date) > '%s'
    ) h
    left join
    jd_item_stock_latest b
    on h.sku_id = b.sku_id and b.sku_id is not NULL
    left join
    jd_item_category c
    on h.sku_id = c.sku_id
    -- left join
    -- jd_promo_item_latest d
    -- on h.sku_id = d.sku_id
    -- left join
    -- jd_promo_category_latest f
    -- on f.category_id = c.category_id

    WHERE

    b.sku_id is not NULL
    and b.update_time>'%s'
    and c.sku_id is not NULL
    -- and (d.dt is NULL or d.dt > '2015-11-4')
    -- and (f.dt is NULL or f.dt > '%s')

    ''' %(dt2,dt2,dt4)

    # print sql

    affected_rows = dbhelper.executeSqlWrite1(sql)
    return affected_rows


if __name__ == "__main__":


    while True:
        t1 = time.time()
        affected_rows = calculate_price_table()
        t2 = time.time()
        print "Completed. Rows affected: %s" %affected_rows
        print "using time in seconds: %s" %(t2-t1)

        remaining = timeHelper.getTimeLeftTillTomorrow()

        print "Now sleep to tomorrow, hours left = %s" %(remaining/3600)
        time.sleep(remaining)
