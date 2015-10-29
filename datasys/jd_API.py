# encoding: utf-8

import sys
import url_utils
import json
import time

reload(sys)
sys.setdefaultencoding('utf8')

# 0.1 : got refused after crawling 90000 products... Now set to 0.5

SLEEP_TIME = 0.5

def __get_price_call_url___(sku_list):
    # http://p.3.cn/prices/mgets?skuIds=J_854074,J_1772186
    api_url = "http://p.3.cn/prices/mgets?skuIds="
    tlist = []
    for sku_id in sku_list:
        mark = "J_%s" %sku_id
        tlist.append(mark)
    return api_url + ','.join(tlist)

def __transform_price_list_to_map__(price_list):
    ret_map = {}
    for price_item in price_list:
        id = price_item['id']
        price = price_item['p']
        price_m = price_item['m']
        ret_map['%s'%id] = (price,price_m)
    return ret_map

def getPrices_JD(sku_list):
    print 'sku_list len: %s' %len(sku_list)
    iters = len(sku_list)//100+1
    price_list = []
    for i in xrange(iters):
        remaining = len(sku_list) - i*100
        end = 100
        if remaining < 100:
            end = remaining
        list2 = sku_list[i*100:i*100+end]
        list3 = __getPrices_JD_100__(list2)
        price_list = price_list + list3

        if i>0:
            time.sleep(SLEEP_TIME)

        # DEBUG INFO BEGEIN
        # print 'list2 len: %s' %len(list2)
        # print 'pricelist len: %s' %len(list3)
        # if len(list2)!=len(list3):
        #     print list2
        #     print list3
        # DEBUG INFO END
    return __transform_price_list_to_map__(price_list)


def __getPrices_JD_100__(sku_list):
    if len(sku_list) == 0:
        return []
    api_url = __get_price_call_url___(sku_list)
    obj =  json.loads(url_utils.getWebResponse(api_url))
    # print 'obj len: %s' %len(obj)
    for item in obj:
        item['id'] = int(item['id'].replace('J_',''))
        item['p'] = float(item['p'])
        item['m'] = float(item['m'])
    return obj



if __name__ == "__main__":
    print getPrices_JD([854074,1772186])