# encoding: utf-8
import dbhelper_read
from datasys import timeHelper
from datasys.memcachedHelper import memcachedStatic
import service_config

# mc = memcachedStatic.getMemCache()
#
# def getMemcacheKeyForCatalogIndex(catalog_id):
#     mckey_prefix = service_config.MEMCACHE_KEY_FOR_CATALOG_INDEX
#     mc_key = "%s::%s" %(mckey_prefix,catalog_id)
#     return mc_key
#
# def generateIndexOnCatalog():
#     sql = 'select catalog_id from jd_catalog'
#     catrows = dbhelper_read.executeSqlRead(sql)
#     catlist = ['_EXPENSIVE_','_ALL_']
#     for row in catrows:
#         catlist.append(row['catalog_id'])
#     for item in catlist:
#         catalog_dict = {}
#         rows = get_catalog_Rows(item)
#         catalog_dict['data'] = rows
#         catalog_dict['num'] = len(rows)
#         mc_key = getMemcacheKeyForCatalogIndex(item)
#         mcret = mc.set(mc_key,catalog_dict)
#         print len(rows)
#         print mcret
#
# def testGetIndexOnCatalog():
#     sql = 'select catalog_id from jd_catalog'
#     catrows = dbhelper_read.executeSqlRead(sql)
#     catlist = ['_EXPENSIVE_','_ALL_']
#     for row in catrows:
#         catlist.append(row['catalog_id'])
#     tdict = {}
#     for item in catlist:
#         mc_key = getMemcacheKeyForCatalogIndex(item)
#         cat_dict = mc.get(mc_key)
#         tdict[item] = cat_dict
#     pass
#
# def get_catalog_Rows(catalog_name):
#     startpos = 1
#
#     catalog_sql_part = " catalog_id is not null and "
#     if catalog_name == "_ALL_":
#         pass
#     elif catalog_name == "_EXPENSIVE_":
#         catalog_sql_part += ' catalog_id<>1000 and catalog_id<>2000 and catalog_id<>3000 and '
#         min_allowed_price = service_config.SKU_LIST_MIN_PRICE_FOR_EXPENSIVE
#     else:
#         catalog_sql_part = 'catalog_id = %s and ' %int(catalog_name)
#
#     dt = timeHelper.getTimeAheadOfNowHours(service_config.SKU_LIST_APP_WORTHY_RECENCY_HOURS, timeHelper.FORMAT_LONG)
#     sql = '''
#         select
#         *
#         -- ,if(a=34,0,1) as stock_bit
#         from
#         jd_worthy_latest
#         where
#         %s
#         worthy_value1 < %s
#         and current_price >= %s
#         and current_price < %s
#         and this_update_time > '%s'
#         -- and a <> 34 -- 有货,无货标志34
#         order by
#         -- stock_bit DESC,
#         worthy_value1 ASC
#         -- limit %s, %s
#         limit %s
#     ''' %( catalog_sql_part,
#            service_config.SKU_LIST_MIN_ALLOWED_WORTHY_VALUE,
#            service_config.SKU_LIST_MIN_ALLOWED_PRICE,
#            service_config.SKU_LIST_MAX_ALLOWED_PRICE,
#            dt,
#            startpos,
#            service_config.SKU_LIST_FRAME_SIZE,
#            service_config.SKU_LIST_MAX_RECALL_NUM
#         )
#     print sql
#     retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
#     return retrows
#
#
# if __name__ == "__main__":
#
#     generateIndexOnCatalog()
#     testGetIndexOnCatalog()
#     pass