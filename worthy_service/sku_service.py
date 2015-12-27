# encoding: utf-8

import time

import dbhelper_read
import service_config
from datasys import jd_API,timeHelper
from datasys.memcachedHelper import memcachedStatic
import rerank_service

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

        deduction_list = []

        if row['max_deduction'] is not None:
            if float(row['max_deduction']) > 90000000:
                row['max_deduction'] = -1.0
            tp = {
                'name': '满减',
                'content': '满%0.0f,减%0.0f现金' %(row['reach'],row['deduction'])
            }
            deduction_list.append(tp)


        if row['reach_2'] is not None:
            if row['reach'] is not None:
                # judge for duplicate entry on deductions
                if abs(float(row['reach_2'])-float(row['reach'])) < 0.001:
                    row['reach_2'] = None
                    row['deduction_2'] = None
                else:
                    tp = {
                        'name': '满减',
                        'content': '满%0.0f,减%0.0f现金' %(row['reach_2'],row['deduction_2'])
                    }
                    deduction_list.append(tp)

        if row['reach_num'] is not None:
            tp = {
                'name': '打折',
                'content': row['content_discount']
            }
            deduction_list.append(tp)

        row['deducts'] = deduction_list

    pass

MEMCACHE_KEY_PREFIX_CATALOGID = "MEMCACHE_KEY_PREFIX_CATALOGID"
MEMCACHE_KEY_PREFIX_QUERY = "MEMCACHE_KEY_PREFIX_QUERY"

def getSkuListByCatalogID(catalog_id = '_HISTORY_LOWEST_',startpos=0,is_update_cache=False):
    # print "catalog_id = %s" %catalog_id
    keystr = memcachedStatic.getKey("%s" %catalog_id)
    mckey = "%s::%s" %(MEMCACHE_KEY_PREFIX_CATALOGID, keystr)
    #mcv is reranked result of all returned skus
    mcv = None
    if not is_update_cache:
        mcv = mc.get(mckey)
    if mcv is None or len(mcv)==0:
        idlist = getSku_ID_ListByCatalogID(category_id=catalog_id, startpos=startpos)
        mcv = rerank_service.rerank_list(idlist,apply_category_mixer=True)
        mc.set(mckey,mcv,service_config.SKU_LIST_CACHE_TIME_OUT)
    else:
        print "OK cached"

    partlist = _get_frame_from_list(mcv,startpos)
    retlist = getWorthyInfo_of_skuid_list(partlist)
    _processSkuThumbInfo(retlist)
    return retlist


def getSkuListByQuery(query,startpos=0):
    keystr = memcachedStatic.getKey(query)
    mckey = "%s::%s" %(MEMCACHE_KEY_PREFIX_CATALOGID, keystr)
    #mcv is reranked result of all returned skus
    mcv = mc.get(mckey)
    if mcv is None or len(mcv)==0:
        mcv = rerank_service.rerank_list_query(query)
        mc.set(mckey,mcv,service_config.SKU_LIST_CACHE_TIME_OUT)
    # print "ok"
    # mc.flush_all()
    # pp = mc.get(mckey)
    # print 'ok2'
    partlist = _get_frame_from_list(mcv,startpos)
    retlist = getWorthyInfo_of_skuid_list(partlist)
    _processSkuThumbInfo(retlist)
    return retlist


def _get_frame_from_list(thumb_list,startpos):
    if startpos >= len(thumb_list):
        return []
    maxpos = len(thumb_list)
    endpos = startpos + service_config.SKU_LIST_FRAME_SIZE #- 1
    if endpos > maxpos:
        endpos = maxpos

    return thumb_list[startpos:endpos]


def getSku_ID_ListByCatalogID(category_id = "_ALL_", startpos = 0, min_allowed_price=service_config.SKU_LIST_MIN_ALLOWED_PRICE, min_allowed_discount_rate=service_config.SKU_LIST_MIN_ALLOWED_WORTHY_VALUE):

    retrows = None
    t1 = time.time()

    catalog_constraint = " catalog_id is not null and catalog_id<>1000 and catalog_id<>2000 and catalog_id<>3000 and category_name not like '%%保护套%%' AND "

    if category_id == "_ALL_":
        catalog_sql_part = catalog_constraint
    elif category_id == "_EXPENSIVE_":
        min_allowed_price = service_config.SKU_LIST_MIN_PRICE_FOR_EXPENSIVE
        catalog_sql_part = catalog_constraint
    else:
        catalog_sql_part = 'catalog_id = %s and ' %category_id

    dt = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
    sql = '''
        select
        sku_id
        -- ,if(a=34,0,1) as stock_bit
        from
        jd_worthy_latest
        where
        %s
        worthy_value1 < %s
        and median_price >= %s
        and median_price < %s
        and this_update_time > '%s'
        -- and a <> 34 -- 有货,无货标志34
        order by
        -- stock_bit DESC,
        worthy_value1 ASC
        -- limit %s, %s
    ''' %(catalog_sql_part, min_allowed_discount_rate, min_allowed_price, service_config.SKU_LIST_MAX_ALLOWED_PRICE, dt, startpos, service_config.SKU_LIST_FRAME_SIZE)

    if category_id == '_HISTORY_LOWEST_':
        sql = '''
        select
        sku_id
        from
        jd_worthy_latest
        where
        %s
        min_price_reached = 2
        and this_update_time > '%s'
        and a<>34
        order by
        worthy_value1 ASC
        ''' %(catalog_constraint, dt)

    elif category_id == 'HOT':
        dt_hot = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_DISCOVERY_RECENCY_HOURS,format=timeHelper.FORMAT_LONG)
        sql = '''
        select

        distinct a.sku_id

        from

        jd_notification_history_lowest a
        left join
        jd_worthy_latest b
        using(sku_id)

        where
        %s
        a.update_time > '%s'
        and b.a<>34

        order by
        a.update_time DESC, worthy_value1 ASC
        ''' %(catalog_constraint, dt_hot)

    print sql
    retrows = dbhelper_read.executeSqlRead(sql)
    vlist = []
    for row in retrows:
        vlist.append(row['sku_id'])
    return vlist


# def getDiscountItemsAll(category_id = "_EXPENSIVE_", startpos = 0, min_allowed_price=service_config.SKU_LIST_MIN_ALLOWED_PRICE, min_allowed_discount_rate=service_config.SKU_LIST_MIN_ALLOWED_WORTHY_VALUE):
#
#     kstr = memcachedStatic.getKey(category_id)
#     mckey = "getDiscountItemsAll_17_%s_%s_%s_%s" %(kstr, startpos, min_allowed_price,min_allowed_discount_rate)
#     print "memcache key = %s" %mckey
#     mcv = None
#     # mcv = mc.get(mckey)
#     retrows = None
#     t1 = time.time()
#     if mcv is not None:
#         print "ok cached"
#         retrows = mcv
#     else:
#         catalog_sql_part = " catalog_id is not null and catalog_id<>1000 and catalog_id<>2000 and catalog_id<>3000 and "
#         if category_id == "_ALL_":
#             pass
#         elif category_id == "_EXPENSIVE_":
#             min_allowed_price = service_config.SKU_LIST_MIN_PRICE_FOR_EXPENSIVE
#         else:
#             catalog_sql_part = 'catalog_id = %s and ' %int(category_id)
#
#         dt = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
#         sql = '''
#             select
#             *
#             -- ,if(a=34,0,1) as stock_bit
#             from
#             jd_worthy_latest
#             where
#             %s
#             worthy_value1 < %s
#             and current_price >= %s
#             and current_price < %s
#             and this_update_time > '%s'
#             -- and a <> 34 -- 有货,无货标志34
#             order by
#             -- stock_bit DESC,
#             worthy_value1 ASC
#             limit %s, %s
#         ''' %(catalog_sql_part, min_allowed_discount_rate, min_allowed_price, service_config.SKU_LIST_MAX_ALLOWED_PRICE, dt, startpos, service_config.SKU_LIST_FRAME_SIZE)
#         print sql
#         retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
#
#     t2 = time.time()
#     # get realtime_price, just try, fail is ok
#     _processSkuThumbInfo(retrows)
#
#     mc.set(mckey, retrows, service_config.SKU_LIST_CACHE_TIME_OUT)
#     print "rows returned: %s" %len(retrows)
#     t3 = time.time()
#     print "t2-t1 = %0.1f" %(t2-t1)
#     print "t3-t2 = %0.1f" %(t3-t2)
#     return retrows



def getWorthyInfo_of_skuid_list(sku_id_list):
    if len(sku_id_list) == 0:
        return []
    sku_id_list2 = []
    for item in sku_id_list:
        sku_id_list2.append("%s" %item)
    dt = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
    id_clause = ','.join(sku_id_list2)

    sql = '''
            select
            *, instr('%s',sku_id) as dd
            from
            jd_worthy_latest
            where
            this_update_time > '%s'
            and sku_id in (%s)
            order by dd ASC
        ''' %(id_clause,dt,id_clause)
    # print sql
    retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
    return retrows


def getWorthyInfo_of_skuid(sku_id):
    sql = 'select * from jd_worthy_latest where sku_id=%s limit 1' %sku_id
    retrows = dbhelper_read.executeSqlRead(sql, is_dirty=True)
    _processSkuThumbInfo(retrows)
    return retrows


def _getPriceHistory(sku_id):
    sql = '''
    select a.update_date, a.price from

    (select * from jd_item_price
    where sku_id = %s
    order by price ASC) a

    -- group by a.update_date
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
    order by dt DESC
    ''' %(sku_id,sku_id,sku_id)
    retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
    for row in retrows:
        types = row['type']
        if types == 'gift':
            row['content'] = u'赠送礼物,价值￥%0.0f'%row['content']
        score = 0
        try:
            score = float(row['score'])
        except:
            pass
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
    try:
        ret['worthy'] = getWorthyInfo_of_skuid(sku_id)[0]
    except:
        pass
    try:
        ret['price_chart'] = getPriceHistory_forChart(sku_id)
    except:
        pass
    try:
        ret['discount_history_list'] = getDiscountHistory_of_Sku_for_table(sku_id)
    except:
        pass
    try:
        ret['images'] = getImages_of_sku_as_list(sku_id)
    except:
        pass
    try:
        ret['discount_list'] = getDiscounts_of_sku_as_list(sku_id)
    except Exception as e:
        print e
    return ret


if __name__ == "__main__":
    # test case
    # getDiscountItemsAll()

    # print getSingleSku_Mixed_Info(2136882)
    # print getSkuListByCatalogID("_EXPENSIVE_",30)
    # print getSkuListByQuery('键盘',30)
    print getSku_ID_ListByCatalogID(category_id="_HISTORY_LOWEST_")
    pass
