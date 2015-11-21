# encoding: utf-8

from datasys import dbhelper, timeHelper, crawler_helper
import time
import datamining_config


def calculate_min_max_price():
    print 'Reading item_dynamic history and calculate min/max/avg/median price for skus...'
    t1 = time.time()
    dt = timeHelper.getTimeAheadOfNowHours(datamining_config.PRICE_RECENCY_HOURS, timeHelper.FORMAT_LONG)
    sql1 = '''
        select
            sku_id,
            AVG(price) as average_price,
            min(price) as min_price,
            median(price) as median_price,
            max(price) as max_price,
            max(update_time) as origin_time,
            count(1) as sample_count

        from
        jd_item_dynamic

        where

        update_time > '2015-11-14 0:00:00'  -- 双十一期间价格不能算啊...
        and price > 0

        group by sku_id
        having max(update_time) >= '%s'
    ''' %(dt)

    print sql1
    retrows = dbhelper.executeSqlRead2(sql1, is_dirty=True)
    print "Done, rows to insert: %s" %len(retrows)
    t2 = time.time()
    print 'using seconds: %s' %(t2-t1)

    sql_cb = '''

        CREATE TABLE jd_analytic_price_stat_latest (
          sku_id bigint(20) NOT NULL,
          average_price float NOT NULL,
          min_price float NOT NULL,
          median_price float NOT NULL,
          max_price float NOT NULL,
          origin_time datetime NOT NULL,
          sample_count int(11) NOT NULL,
          PRIMARY KEY (sku_id),
          KEY skuid (sku_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8

    '''

    ret = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_price_stat',
        num_cols=len(retrows[0]),
        value_list=retrows,
        is_many=True,
        need_history=False,
        sql_create_table= sql_cb,
    )
    return ret


# def calculate_price_table():
#
#     print 'Reading item_dynamic history and calculate min/max/avg/median price for skus...'
#     # ret1 = _calculate_min_max_price()
#     # print ret1
#
#     sql = '''
#     select
#     h.sku_id as sku_id,
#     r.price as current_price,
#     h.average_price as average_price,
#     h.min_price as min_price,
#     h.median_price as median_price,
#     h.max_price as max_price,
#     r.price/h.max_price as discount_rate,
#     b.a as a,
#     b.b as b,
#     b.c as c,
#     b.j as j,
#     b.l as l,
#     c.category_id as category_id
#
#     from
#
#     jd_analytic_price_stat_latest h
#     left join jd_item_dynamic_latest r
#     on h.sku_id = r.sku_id
#
#     left join
#     jd_item_stock_latest b
#     on h.sku_id = b.sku_id and b.sku_id is not NULL
#     left join
#     jd_item_category c
#     on h.sku_id = c.sku_id
#
#     WHERE
#
#     b.sku_id is not NULL
#     and c.sku_id is not NULL
#
#     '''
#
# #    print sql
#
#     print 'Reading item_dynamic database, calculating min/max price, etc...'
#     retrows = dbhelper.executeSqlRead2(sql,is_dirty=True)
#     if len(retrows)<=0:
#         error_msg = 'error: reading database returned 0 rows'
#         print error_msg
#         return {'status':-1, 'msg':error_msg}
#     print 'Completed. Rows read: %s' %len(retrows)
#     # print len(retrows[0])
#
#     sql_cb = '''
#         CREATE TABLE jd_price_temp_latest (
#           sku_id bigint(20) NOT NULL,
#           current_price float NOT NULL,
#           average_price float NOT NULL,
#           min_price float NOT NULL,
#           median_price float DEFAULT NULL,
#           max_price float NOT NULL,
#           discount_rate float NOT NULL,
#           a int(11) DEFAULT NULL,
#           b int(11) DEFAULT NULL,
#           c int(11) DEFAULT NULL,
#           j int(11) DEFAULT NULL,
#           l int(11) DEFAULT NULL,
#           category_id varchar(255) NOT NULL,
#           PRIMARY KEY (sku_id),
#           KEY sku (sku_id)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8
#     '''
#
#     print 'Writing to jd_price_temp db...'
#     return crawler_helper.persist_db_history_and_lastest_empty_first(
#         table_name='jd_price_temp',
#         num_cols=len(retrows[0]),
#         value_list=retrows,
#         is_many=True,
#         need_history=False,
#         sql_create_table=sql_cb,
#     )


if __name__ == "__main__":
    t1 = time.time()
    # print calculate_price_table()
    print calculate_min_max_price()
    t2 = time.time()
    print int(t2-t1)
