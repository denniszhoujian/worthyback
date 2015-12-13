# encoding: utf-8

import dbhelper_read
import sku_index_access,sku_service, service_config
from datasys.memcachedHelper import memcachedStatic

mc = memcachedStatic.getMemCache()

def getCatalogs():

    sql = 'select catalog_id, catalog_name as category_name from jd_catalog order by order_weight DESC'
    retrows = dbhelper_read.executeSqlRead(sql)
    for row in retrows:
        row['category_id'] = '%s' %(row['catalog_id'])
        row.pop('catalog_id')
    return retrows


def get_indicator_given_part_of_query(query):
    mckey = memcachedStatic.getKey("GET_INDICATOR::%s" %query)

    mcv = mc.get(mckey)
    if mcv is not None:
        return mcv

    retlist = sku_index_access.getSearchResult(query)
    sku_id_list = []
    i = 0
    for sku_id in retlist:
        sku_id_list.append("%s" %sku_id)
        i += 1
        if i >= 30:
            break

    in_clause = ','.join(sku_id_list)
    sql = '''
        select
            category_id,
            count(1) as count_hits,
            catalog_id,
            catalog_name,
            category_name
        from
        jd_worthy_latest
        where sku_id in (%s) and catalog_name is not NULL
        group by category_id
        order by count_hits DESC
        limit %s
    ''' %(in_clause,service_config.CATEGORY_INDICATOR_MAX_NUM)
    retrows = dbhelper_read.executeSqlRead(sql, is_dirty=True)

    black_list_clause = '","'.join(service_config.PROPERTY_KEY_BLACK_WORD_LIST)
    black_list_clause = '"%s"' %black_list_clause
    sql2 = '''
        select
            p_value,
            LENGTH(p_value) as ll,
            count(1) as count_hits,
            p_key
        from jd_item_property_latest
        where sku_id in (%s)
        and LENGTH(p_value)>3 and LENGTH(p_value)<=30 and p_key<>'__DEFAULT__' and LENGTH(p_key)>=6 and LENGTH(p_key)<=21 and p_key NOT IN (%s) and p_value NOT LIKE '%%%s%%'
        group by p_value
        order by count_hits DESC
        limit %s
    ''' %(in_clause, black_list_clause, query, service_config.PROPERTY_INDICATOR_MAX_NUM)
    # print sql2
    retrows2 = dbhelper_read.executeSqlRead(sql2)
    ret = {
        'category': retrows,
        'property': retrows2,
    }

    mc.set(mckey,ret)

    return ret


if __name__ == '__main__':
    print get_indicator_given_part_of_query('雅诗兰黛')