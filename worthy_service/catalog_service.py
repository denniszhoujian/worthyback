# encoding: utf-8

import dbhelper_read
import sku_index_access,sku_service, service_config
from datasys.memcachedHelper import memcachedStatic
from worthy_analytics import common_analytics
from utils import regex_dict_helper, collection_utils

mc = memcachedStatic.getMemCache()

P_VALUE_BLACK_LIST = [
    u'其他', u'其它',
    u'不支持',u'支持',
    u'无',
]

P_VALUE_BLACK_LIST_REGEX = [
    r'[\\/]+[\w\W]*-',
    r'[a-z]+\d{2,}[ ]?-',
    r'\d[.]\d{3,}',
    r'2[1234]0[ ]?v',
    r'1[01]0[ ]v',
    r'\d{5,}',
    u'℃',
    u'°[ ]?c',
    u'\d(摄氏|华氏| )?度',
    r'[\w\W]+-[\w\W]*-',
    u'\d+[种个]',
    r'[a-z0-9]{2,}[ ]?-[ ]?[a-z0-9]{2,}',
    u'不含',
    u'的所有',
    u'年\d月',
    r'\d[ ]?hz',
]

P_VALUE_SPLIT_LIST = [
     ',', ';', u'，',u'；',u'、',
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
        plist = collection_utils.expand_list(plist, P_VALUE_SPLIT_LIST)
        qlist = []
        for item in plist:
            if item not in P_VALUE_BLACK_LIST:
                item = item.lower()
                if not regex_dict_helper.is_regex_match_list(item, P_VALUE_BLACK_LIST_REGEX):
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

    print regex_dict_helper.is_regex_match_list('en-el15',P_VALUE_BLACK_LIST_REGEX)
    # exit()

    ret = get_indicator_given_part_of_query('硬盘')
    for item in ret:
        print item['category'][1]
        for item2 in item['property']:
            print '%s\t%s' %(item2,len(item2))
        print '-'*60
