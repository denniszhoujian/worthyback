# encoding: utf-8

import dbhelper_read
from datasys.memcachedHelper import memcachedStatic

mc = memcachedStatic.getMemCache()

FRAME_SIZE = 30
CACHE_TIME_OUT = 3600

def getSkuInfoForList(sku_list):

    vlist = []
    for sku in sku_list:
        sql1 = 'select * from jd_item_dynamic_latest where sku_id=%s limit 1' %sku
        retrows1 = dbhelper_read.executeSqlRead(sql1)
        if len(retrows1) > 0:
            vlist = vlist + retrows1

    return vlist


def getDiscountItemsAll(category_id = "_ALL_", startpos = 0, min_allowed_price=20, min_allowed_discount_rate=0.9):

    kstr = memcachedStatic.getKey(category_id)
    mckey = "getDiscountItemsAll4_%s_%s_%s_%s" %(kstr, startpos, min_allowed_price,min_allowed_discount_rate)
    print "memcache key = %s" %mckey
    # mcv = mc.get(mckey)
    mcv = None
    if mcv is not None:
        print "ok cached"
        return mcv

    if category_id == "_ALL_":
        category_id = ""
    elif category_id == "_EXPENSIVE_":
        category_id = ""
        min_allowed_price = 2000

    sql = '''
        select * from
        (select * from jd_price_temp where discount_rate<%s and max_price>=%s) a
        left join
        jd_item_dynamic_latest c
        on a.sku_id = c.sku_id
        where c.sku_id is not NULL and current_price>0 and category_id like '%s%%'
        order by discount_rate*power(max_price,0.2) ASC
        limit %s, %s

    ''' %(min_allowed_discount_rate, min_allowed_price, category_id, startpos+1, FRAME_SIZE)
    # print sql
    retrows = dbhelper_read.executeSqlRead(sql)
    # mc.set(mckey, retrows, CACHE_TIME_OUT)
    print "rows returned: %s" %len(retrows)
    return retrows


if __name__ == "__main__":

    getDiscountItemsAll(0)

