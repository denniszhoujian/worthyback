# encoding: utf-8

import dbhelper_read

def getCatalogs():

    sql = 'select catalog_id, catalog_name as category_name from jd_catalog order by order_weight DESC'
    retrows = dbhelper_read.executeSqlRead(sql)
    for row in retrows:
        row['category_id'] = '%s' %(row['catalog_id'])
        row.pop('catalog_id')
    return retrows