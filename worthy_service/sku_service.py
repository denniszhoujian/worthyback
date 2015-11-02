# encoding: utf-8

from datasys import dbhelper

def getSkuInfoForList(sku_list):

    vlist = []
    for sku in sku_list:
        sql1 = 'select * from jd_item_dynamic_latest where sku_id=%s limit 1' %sku
        retrows1 = dbhelper.executeSqlRead(sql1)
        if len(retrows1) > 0:
            vlist = vlist + retrows1

    return vlist

