# encoding: utf-8

from datasys import dbhelper, timeHelper, crawler_helper
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

    dt2 = timeHelper.getTimeAheadOfNowDays(2)
    sql = '''

    select
    h.sku_id as sku_id,
    r.price as current_price,
    h.average_price as average_price,
    h.min_price as min_price,
    h.max_price as max_price,
    h.price_m  as price_m,
    r.price/h.max_price as discount_rate,
--    h.update_date as update_date,
--    h.thumbnail_url,
--    h.icon_url,
    b.a as a,
    b.b as b,
    b.c as c,
    b.j as j,
    b.l as l,
--    b.update_time as stock_update_time,
    c.category_id as category_id

    from

    (
        select sku_id,
        AVG(price) as average_price,
        min(price) as min_price,
        max(price) as max_price,
        max(price_m) as price_m,
        max(update_date) as update_date
--        thumbnail_url,
--        icon_url

        from
        jd_item_dynamic

        group by sku_id
        having max(update_date) > '%s'
    ) h

    left join jd_item_dynamic_latest r
    on h.sku_id = r.sku_id


    left join
    jd_item_stock_latest b
    on h.sku_id = b.sku_id and b.sku_id is not NULL
    left join
    jd_item_category c
    on h.sku_id = c.sku_id

    WHERE

    b.sku_id is not NULL
    and c.sku_id is not NULL

    ''' %(dt2)

#    print sql

    print 'Reading item_dynamic database, calculating min/max price, etc...'
    retrows = dbhelper.executeSqlRead2(sql,is_dirty=True)
    if len(retrows)<=0:
        error_msg = 'error: reading database returned 0 rows'
        print error_msg
        return {'status':-1, 'msg':error_msg}
    print 'Completed. Rows read: %s' %len(retrows)
    # print len(retrows[0])

    print 'Writing to jd_price_temp db...'
    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_price_temp',
        num_cols=len(retrows[0]),
        value_list=retrows,
        is_many=True,
        need_history=False
    )


if __name__ == "__main__":
    t1 = time.time()
    print calculate_price_table()
    t2 = time.time()
    print int(t2-t1)
