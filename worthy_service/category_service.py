# encoding: utf-8

import dbhelper_read
from datasys.memcachedHelper import memcachedStatic

SERVICE_CATEGORY_CACHE_TIMEOUT = 86400
mc = memcachedStatic.getMemCache()

def get_sub_categories(category_id):
    sql = 'select id as category_id, name as category_name from jd_category where id like "%s-%%" and id not like "%s-%%-%%"' %(category_id, category_id)
    retrows = dbhelper_read.executeSqlRead(sql)

    if len(retrows) == 0:
        sql = 'select id as category_id, name as category_name from jd_category where id like "%s-%%" and id not like "%s-%%-%%-%%"' %(category_id, category_id)
        retrows = dbhelper_read.executeSqlRead(sql)

    # for row in retrows:
    #     row['sub_categories'] = _expand_to_sub_categories(row['category_id'])
    #     print row['category_id']
    return retrows

def getServiceCategoryList():
    mckey = 'category_service.py::getServiceCategoryList'
    #mv  = mc.get(mckey)
    mv = None
    if mv is not None:
        return mv
    sql = 'select * from jd_category_white_list where is_service=1 order by id ASC'
    retrows = dbhelper_read.executeSqlRead(sql)
    # for row in retrows:
    #     sub_rows = get_sub_categories(row['category_id'])
    #     row['sub_categories'] = sub_rows

    #mc.set(mckey,retrows,SERVICE_CATEGORY_CACHE_TIMEOUT)
    return retrows

def _get_sub_categories_all(category_id):
    sql = 'select id as category_id, name as category_name from jd_category where id like "%s-%%"' %(category_id)
    retrows = dbhelper_read.executeSqlRead(sql)
    return retrows

def getServiceCategoryListAll(level = 1):
    mckey = 'category_service.py::getServiceCategoryListAll_%s' %level
    #mv  = mc.get(mckey)
    mv = None
    if mv is not None:
        return mv

    white_list = []
    sql = 'select * from jd_category_white_list where is_service=1'
    retrows = dbhelper_read.executeSqlRead(sql)
    for row in retrows:
        white_list.append(row['category_id'])

    retlist = []

    for catid in white_list:
        sql2 = '''
          select * from jd_category where (id='%s' or id like '%s-%%')
          and (LENGTH(id) - LENGTH(REPLACE(id,"-", ""))) / LENGTH("-") <= %s
          order by id ASC
        ''' %(catid, catid, level)
        #print sql2
        retrows2 = dbhelper_read.executeSqlRead(sql2)
        #print len(retrows2)
        retlist += retrows2

    #mc.set(mckey,retlist,SERVICE_CATEGORY_CACHE_TIMEOUT)
    return retlist

# def getServiceCategoryListAll(level = 0):
#     mckey = 'category_service.py::getServiceCategoryListAll'
#     #mv  = mc.get(mckey)
#     mv = None
#     if mv is not None:
#         return mv
#
#     sql = 'select * from jd_category_white_list where is_service=1'
#     retrows = dbhelper_read.executeSqlRead(sql)
#     for row in retrows:
#         sub_rows = _get_sub_categories_all(row['category_id'])
#         row['sub_categories'] = sub_rows
#     #mc.set(mckey,retrows,SERVICE_CATEGORY_CACHE_TIMEOUT)
#     return retrows


if __name__ == '__main__':
    ret = getServiceCategoryListAll(1)
    print len(ret)

    # for item in ret:
    #     print '-'*60
    #     print item['category_id']
    #     print json.dumps(get_sub_categories(item['category_id']))