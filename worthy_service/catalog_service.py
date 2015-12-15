# encoding: utf-8

import dbhelper_read
import sku_index_access,sku_service, service_config
from datasys.memcachedHelper import memcachedStatic
from worthy_analytics import common_analytics

mc = memcachedStatic.getMemCache()

P_VALUE_BLACK_LIST = [
    u'其他', u'其它',
    u'不支持',
    u'无',
]

def getCatalogs():

    sql = 'select catalog_id, catalog_name as category_name from jd_catalog order by order_weight DESC'
    retrows = dbhelper_read.executeSqlRead(sql)
    for row in retrows:
        row['category_id'] = '%s' %(row['catalog_id'])
        row.pop('catalog_id')
    return retrows


def get_indicator_given_part_of_query(query):
    mckey = memcachedStatic.getKey("GET_INDICATOR2::%s" %query)

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

    retlist = []

    for row in retrows:
        category_id = row['category_id']
        # if category_id in ['670-677-5009','670-677-683','670-677-687','670-671-672']:
        #     continue
        category_name = row['category_name']
        catalog_id = row['catalog_id']
        catalog_name = row['catalog_name']
        sql0 = '''
            select
            p_value,
            count(1) as count_hits,
            p_key

            from

            jd_analytic_property_latest

            where sku_id in (%s)
            and category_id = "%s"
            and p_value like "%%%s%%"
            group by p_value
            -- having count(1) > 1
            order by count_hits DESC
            limit %s
        ''' %(in_clause, category_id,  query, service_config.PROPERTY_INDICATOR_MAX_NUM)

        sql1 = '''
            select
            p_value,
            count(1) as count_hits,
            p_key

            from

            jd_analytic_property_latest

            where sku_id in (%s)
            and category_id = "%s"
            and p_key = '品牌'
            group by p_value
            -- having count(1) > 1
            order by count_hits DESC
            limit %s
        ''' %(in_clause, category_id, service_config.PROPERTY_INDICATOR_MAX_NUM)

        sql2 = '''
            select
            p_value,
            count(1) as count_hits,
            p_key

            from

            jd_analytic_property_latest

            where sku_id in (%s)
            and category_id = "%s"
            and p_key <> '品牌'
            group by p_value
            -- having count(1) > 1
            order by count_hits DESC
            limit %s
        ''' %(in_clause, category_id, service_config.PROPERTY_INDICATOR_MAX_NUM)

        retrows0 = dbhelper_read.executeSqlRead(sql0)
        retrows1 = dbhelper_read.executeSqlRead(sql1)
        retrows2 = dbhelper_read.executeSqlRead(sql2)
        plist = common_analytics.dedup_leave_max(_retrows_to_list(retrows0+retrows1+retrows2, 'p_value'))
        query2 = common_analytics.dedup_inline(query)
        if query2 not in plist:
            if query2 not in category_name:
                plist = [query2] + plist
        plist = common_analytics.remove_string_from_list(category_name,plist)
        qlist = []
        for item in plist:
            if item not in P_VALUE_BLACK_LIST:
                qlist.append(item)
        retlist.append({
            'category': [category_id,category_name],
            'property': qlist,
        })

    mc.set(mckey,retlist)
    return retlist
#
# def _check_black_list(item, blacklist):
#     for b in blacklist:
#         if item == b:
#             return True
#     return False

def _retrows_to_list(retrows, colname):
    rlist = []
    for row in retrows:
        rlist.append(row[colname])
    return rlist


if __name__ == '__main__':
    print get_indicator_given_part_of_query('软壳衣裤 软壳衣裤')