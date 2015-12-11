# encoding: utf-8

from datasys import dbhelper, timeHelper, crawler_helper
import time
import datamining_config
import logging


def calculate_min_max_price():
    logging.debug('Reading item_dynamic history and calculate min/max/avg/median price for skus...')
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

        -- update_time > '2015-11-14 0:00:00' and  -- 双十一期间价格不能算啊...
        price > 0

        group by sku_id
        having max(update_time) >= '%s'
    ''' %(dt)

    logging.debug(sql1)
    retrows = dbhelper.executeSqlRead2(sql1, is_dirty=True)
    logging.debug("Done, rows to insert: %s" %len(retrows) )
    t2 = time.time()
    logging.debug('using seconds: %0.1f' %(t2-t1) )

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


if __name__ == "__main__":
    t1 = time.time()
    print calculate_min_max_price()
    t2 = time.time()
    print(int(t2-t1))
