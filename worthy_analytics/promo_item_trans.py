# encoding: utf-8

from datasys import dbhelper,timeHelper
import time
import json

def read_Promo_Items() :

    sql = '''
        select * from jd_promo_item_latest where quan_json is not NULL
    '''
    retrows = dbhelper.executeSqlRead(sql)

    adict = {}

    for row in retrows:
        obj = json.loads(row['quan_json'])
        url = "http://item.jd.com/%s.html" %row['sku_id']
        # print "%s\t\t%s" %(obj['title'],url)
        # print ("\n")
        adict[obj['title']] = url
    pass

    for item in adict:
        print item
        print adict[item]


if __name__ == "__main__":
    read_Promo_Items()