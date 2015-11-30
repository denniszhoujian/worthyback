# encoding: utf-8

import dbhelper_read
from datasys.memcachedHelper import memcachedStatic
from datasys import jd_API,timeHelper
import time
#import rating_service
import service_config
import service_helper

mc = memcachedStatic.getMemCache()

def _processSkuThumbInfo(retrows):
    if service_config.SKU_LIST_IF_USE_REAL_TIME_PRICE:
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

    for row in retrows:
        # diff_stars = 3
        # if row['rating_score_diff'] is not None:
        #     diff_stars = rating_service.getRatingDiffScore(row['rating_score_diff'])
        # row['diff_stars'] = diff_stars
        if row['max_deduction'] is not None:
            if float(row['max_deduction']) > 90000000:
                row['max_deduction'] = -1.0
        if row['reach_2'] is not None:
            if row['reach'] is not None:
                if abs(float(row['reach_2'])-float(row['reach'])) < 0.001:
                    print('<0.001')
                    row['reach_2'] = None
                    row['deduction_2'] = None

    pass



def getDiscountItemsAll(category_id = "_EXPENSIVE_", startpos = 0, min_allowed_price=service_config.SKU_LIST_MIN_ALLOWED_PRICE, min_allowed_discount_rate=service_config.SKU_LIST_MIN_ALLOWED_WORTHY_VALUE):

    kstr = memcachedStatic.getKey(category_id)
    mckey = "getDiscountItemsAll_17_%s_%s_%s_%s" %(kstr, startpos, min_allowed_price,min_allowed_discount_rate)
    print "memcache key = %s" %mckey
    mcv = None
    # mcv = mc.get(mckey)
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
            min_allowed_price = service_config.SKU_LIST_MIN_PRICE_FOR_EXPENSIVE
        else:
            catalog_sql_part = 'catalog_id = %s and ' %category_id

        dt = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
        sql = '''
            select
            *
            -- ,if(a=34,0,1) as stock_bit
            from
            jd_worthy_latest
            where
            %s
            worthy_value1 < %s
            and current_price >= %s
            and current_price < %s
            and this_update_time > '%s'
            -- and a <> 34 -- 有货,无货标志34
            order by
            -- stock_bit DESC,
            worthy_value1 ASC
            limit %s, %s
        ''' %(catalog_sql_part, min_allowed_discount_rate, min_allowed_price, service_config.SKU_LIST_MAX_ALLOWED_PRICE, dt, startpos, service_config.SKU_LIST_FRAME_SIZE)
        print sql
        retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)

    t2 = time.time()
    # get realtime_price, just try, fail is ok
    _processSkuThumbInfo(retrows)


    mc.set(mckey, retrows, service_config.SKU_LIST_CACHE_TIME_OUT)
    print "rows returned: %s" %len(retrows)
    t3 = time.time()
    print "t2-t1 = %0.1f" %(t2-t1)
    print "t3-t2 = %0.1f" %(t3-t2)
    return retrows


def getWorthyInfo_of_skuid(sku_id):
    sql = 'select * from jd_worthy_latest where sku_id=%s limit 1' %sku_id
    retrows = dbhelper_read.executeSqlRead(sql, is_dirty=True)
    _processSkuThumbInfo(retrows)
    return retrows


def _getPriceHistory(sku_id):
    sql = '''
    select a.update_date, a.price from

    (select * from jd_item_dynamic_flow
    where sku_id = %s
    order by price ASC) a

    group by a.update_date
    order by a.update_date ASC
    ''' %sku_id
    retrows = dbhelper_read.executeSqlRead(sql, is_dirty=True)
    return retrows


def getPriceHistory_forChart(sku_id):
    retrows = _getPriceHistory(sku_id)
    datelist = []
    pricelist = []

    min_dt = retrows[0]['update_date']
    max_dt = retrows[len(retrows)-1]['update_date']

    i = 0
    dt = min_dt
    last_val = int(retrows[0]['price'])
    while True:

        datelist.append("%s" %timeHelper.getDateRemovedYear(dt))
        if "%s" %retrows[i]['update_date'] == "%s" %dt:
            last_val = int(retrows[i]['price'])
            i += 1

        pricelist.append(last_val)

        dt = timeHelper.getDateAheadOfTargetDate("%s"%dt,-1)
        if timeHelper.compareTime("%s" %dt,"%s"%max_dt,timeHelper.FORMAT_SHORT):
            break

    return {
        'dates': datelist,
        'prices': pricelist,
    }

# def getPriceHistory_forChart(sku_id):
#     retrows = _getPriceHistory(sku_id)
#     datelist = []
#     pricelist = []
#
#     min_dt = retrows[0]['update_date']
#     max_dt = retrows[len(retrows)-1]['update_date']
#
#     i = 0
#     dt = min_dt
#     last_val = int(retrows[0]['price'])
#     datelist.append("%s" %timeHelper.getDateRemovedYear(dt))
#     pricelist.append(last_val)
#     while True:
#
#         if "%s" %retrows[i]['update_date'] == "%s" %dt:
#             this_price = int(retrows[i]['price'])
#             if this_price != last_val:
#                 datelist.append("%s" %timeHelper.getDateRemovedYear(timeHelper.getDateAheadOfTargetDate(dt,1)))
#                 pricelist.append(last_val)
#                 datelist.append("%s" %timeHelper.getDateRemovedYear(dt))
#                 pricelist.append(this_price)
#                 last_val = this_price
#
#             i += 1
#
#         dt = timeHelper.getDateAheadOfTargetDate("%s"%dt,-1)
#         if timeHelper.compareTime("%s" %dt,"%s"%max_dt,timeHelper.FORMAT_SHORT):
#             break
#
#     return {
#         'dates': datelist,
#         'prices': pricelist,
#     }

def getImages_of_sku_as_list(sku_id):
    sql = 'select image_url from jd_item_images_latest where sku_id=%s'%sku_id
    return dbhelper_read.executeSqlRead(sql,is_dirty=True)

def getDiscounts_of_sku_as_list(sku_id):
    sql = 'select name, content from jd_analytic_promo_item_latest where (code=15 or code=19) and sku_id=%s order by code ASC, content DESC'%sku_id
    return dbhelper_read.executeSqlRead(sql,is_dirty=True)


def _getDiscountHistory_of_Sku_as_list(sku_id):
    sql = '''
    select dt, type, content, score from
        (select this_update_date as dt, 'deduction' as type, content_deduction as content, deduction_score as score from jd_worthy where sku_id=%s and content_deduction is not NULL
        UNION
        select this_update_date as dt, 'discount' as type, content_discount as content, 1.0-rf_ratio as score from jd_worthy where sku_id=%s and content_discount is not NULL
        UNION
        select this_update_date as dt, 'gift' as type, gift_price*gift_num as content, 0 as score from jd_worthy where sku_id=%s and gift_price is not NULL
        ) a
    order by dt ASC
    ''' %(sku_id,sku_id,sku_id)
    retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
    for row in retrows:
        types = row['type']
        if types == 'gift':
            row['content'] = u'赠送礼物,价值￥%0.0f'%row['content']

        score = float(row['score'])
        row['score'] = int(min(int(score*10),int(5)))

    return retrows


def getDiscountHistory_of_Sku_for_table(sku_id):
    retrows = _getDiscountHistory_of_Sku_as_list(sku_id)
    #ret = service_helper.fill_missing_dates_output_double_lists(retrows,col_name_dt='dt',col_name_val='content',mandatory_min_total_days=60)
    ret = retrows
    return ret

def getSingleSku_Mixed_Info(sku_id):
    ret = {}
    if sku_id is None:
        return ret
    # try:
    if True:
        ret['worthy'] = getWorthyInfo_of_skuid(sku_id)[0]
        ret['price_chart'] = getPriceHistory_forChart(sku_id)
        ret['discount_history_list'] = getDiscountHistory_of_Sku_for_table(sku_id)
        ret['images'] = getImages_of_sku_as_list(sku_id)
        ret['discount_list'] = getDiscounts_of_sku_as_list(sku_id)
    # except Exception as e:
    #     print e
    return ret


if __name__ == "__main__":
    # test case
    # getDiscountItemsAll()

    print getSingleSku_Mixed_Info(1066246)

    pass
