# encoding: utf-8

import dbhelper_read
from datasys.memcachedHelper import memcachedStatic
from datasys import jd_API,timeHelper
import time

mc = memcachedStatic.getMemCache()

FRAME_SIZE = 30
CACHE_TIME_OUT = 3600
MIN_PRICE_FOR_EXPENSIVE = 800
MAX_ALLOWED_PRICE = 30000
IF_USE_REAL_TIME_PRICE = False

DEFAULT_MIN_ALLOWED_PRICE = 20
DEFAULT_MIN_ALLOWED_WORTHY_VALUE = 0.85

APP_WORTHY_RECENCY_HOURS = 12

def getSkuInfoForList(sku_list):

    vlist = []
    for sku in sku_list:
        sql1 = 'select * from jd_item_dynamic_latest where sku_id=%s limit 1' %sku
        retrows1 = dbhelper_read.executeSqlRead(sql1)
        if len(retrows1) > 0:
            vlist = vlist + retrows1

    return vlist


def getDiscountItemsAll(category_id = "_EXPENSIVE_", startpos = 0, min_allowed_price=DEFAULT_MIN_ALLOWED_PRICE, min_allowed_discount_rate=DEFAULT_MIN_ALLOWED_WORTHY_VALUE):

    kstr = memcachedStatic.getKey(category_id)
    mckey = "getDiscountItemsAll15_%s_%s_%s_%s" %(kstr, startpos, min_allowed_price,min_allowed_discount_rate)
    print "memcache key = %s" %mckey
    mcv = None
    mcv = mc.get(mckey)
    retrows = None
    t1 = time.time()
    if mcv is not None:
        print "ok cached"
        retrows = mcv
    else:
        catalog_sql_part = " catalog_id is not null and "
        if category_id == "_ALL_":
            pass
        elif category_id == "_EXPENSIVE_":
            min_allowed_price = MIN_PRICE_FOR_EXPENSIVE
        else:
            catalog_sql_part = 'catalog_id = %s and ' %category_id

        dt = timeHelper.getTimeAheadOfNowHours(APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
        sql = '''
            select *, if(a=34,0,1) as stock_bit from
            jd_worthy_latest
            where
            %s
            worthy_value1 < %s
            and current_price >= %s
            and current_price < %s
            and this_update_time > '%s'
            -- and a <> 34 -- 有货,无货标志34
            order by stock_bit DESC, worthy_value1 ASC
            limit %s, %s
        ''' %(catalog_sql_part, min_allowed_discount_rate, min_allowed_price, MAX_ALLOWED_PRICE, dt, startpos, FRAME_SIZE)
        print sql
        retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)

    t2 = time.time()
    # get realtime_price, just try, fail is ok
    if IF_USE_REAL_TIME_PRICE:
        try:
            skulist = []
            for row in retrows:
                skulist.append(row['sku_id'])
            price_map = jd_API.getSkuListPrice_Mob_Realtime(skulist)
            for row in retrows:
                sku_id = row['sku_id']
                row['price'] = float(price_map["%s" %sku_id])
        except Exception as e:
            print "ERROR in real-time-price retreaval in jd_API"
            print e

    # calculate final_price, final_discount
    for row in retrows:
        # price = float(row['price'])
        # row['price'] = price
        # final_price = price
        # if row['reach'] is not None:
        #     final_price *= (1.0 - float(row['max_deduction_ratio']))
        # row['final_price'] = final_price

        diff_stars = None
        if row['rating_score_diff'] is not None:
            #print "okokshit: %s" %row['rating_score_diff']
            rating_score_diff = float() + 10.0
            diff_stars = 0
            if rating_score_diff > 10:
                rating_score_diff = 10.0
            if rating_score_diff < 0:
                rating_score_diff = 0.0
            diff_stars = rating_score_diff/2
        row['diff_stars'] = diff_stars
        if row['max_deduction'] is not None:
            if float(row['max_deduction']) > 90000000:
                row['max_deduction'] = -1.0


    mc.set(mckey, retrows, CACHE_TIME_OUT)
    print "rows returned: %s" %len(retrows)
    t3 = time.time()
    print "t2-t1 = %0.1f" %(t2-t1)
    print "t3-t2 = %0.1f" %(t3-t2)
    return retrows


if __name__ == "__main__":

    getDiscountItemsAll()

