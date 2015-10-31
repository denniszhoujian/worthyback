# encoding: utf-8

import sys
import url_utils
import json
import time
import dbhelper
import logging

reload(sys)
sys.setdefaultencoding('utf8')

# 0.1 : got refused after crawling 90000 products... Now set to 0.5

SLEEP_TIME = 0.5

# COMMON

def __accumulative_call__(param_list,threshold,func_pointer):
    sku_list = param_list
    iters = len(sku_list)//threshold+1
    price_list = []
    for i in xrange(iters):
        remaining = len(sku_list) - i*threshold
        end = threshold
        if remaining < threshold:
            end = remaining
        list2 = sku_list[i*threshold:i*threshold+end]
        list3 = func_pointer(list2)
        price_list = price_list + list3

        if i>0:
            time.sleep(SLEEP_TIME)

    return price_list

# PRICE

def __get_price_call_url___(sku_list):
    # http://p.3.cn/prices/mgets?skuIds=J_854074,J_1772186 -- deprecated
    # http://pm.3.cn/prices/pcpmgets?skuids=1279171,595936,1279827&origin=2
    api_url = "http://pm.3.cn/prices/pcpmgets?origin=2&skuids="
    tlist = []
    for sku_id in sku_list:
        mark = "%s" %sku_id
        tlist.append(mark)
    return api_url + ','.join(tlist)

def __transform_price_list_to_map__(price_list):
    ret_map = {}
    for price_item in price_list:
        id = price_item['id']
        price = price_item['p']
        price_m = price_item['m']
        price_pcp = None
        if 'pcp' in price_item:
            price_pcp = price_item['pcp']
        ret_map['%s'%id] = (price,price_m,price_pcp)
    return ret_map

def __getPrices_JD_100__(sku_list):
    if len(sku_list) == 0:
        return []
    api_url = __get_price_call_url___(sku_list)
    obj =  json.loads(url_utils.getWebResponse(api_url))
    # print 'obj len: %s' %len(obj)
    for item in obj:
        item['id'] = int(item['id'])
        item['p'] = float(item['p'])
        item['m'] = float(item['m'])
        if 'pcp' in item:
            item['pcp'] = float(item['pcp'])
        else:
            item['pcp'] = None
    return obj

def getPrices_JD(sku_list):
    logging.debug('sku_list len: %s' %len(sku_list))
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

    return __transform_price_list_to_map__(price_list)


# COMMENT-COUNT
# {
#     "CommentsCount": [
#         {
#             "SkuId": 1279827,
#             "ProductId": 1279827,
#             "Score1Count": 261,
#             "Score2Count": 80,
#             "Score3Count": 299,
#             "Score4Count": 1211,
#             "Score5Count": 21239,
#             "ShowCount": 1541,
#             "CommentCount": 23090,
#             "AverageScore": 5,
#             "GoodCount": 22450,
#             "GoodRate": 0.973,
#             "GoodRateShow": 97,
#             "GoodRateStyle": 146,
#             "GeneralCount": 379,
#             "GeneralRate": 0.016,
#             "GeneralRateShow": 2,
#             "GeneralRateStyle": 2,
#             "PoorCount": 261,
#             "PoorRate": 0.011,
#             "PoorRateShow": 1,
#             "PoorRateStyle": 2
#         },
#         {
#             "SkuId": 1279171,
#             "ProductId": 1279171,
#             "Score1Count": 2394,
#             "Score2Count": 947,
#             "Score3Count": 2839,
#             "Score4Count": 6622,
#             "Score5Count": 103301,
#             "ShowCount": 8178,
#             "CommentCount": 116103,
#             "AverageScore": 5,
#             "GoodCount": 109923,
#             "GoodRate": 0.948,
#             "GoodRateShow": 95,
#             "GoodRateStyle": 142,
#             "GeneralCount": 3786,
#             "GeneralRate": 0.032,
#             "GeneralRateShow": 3,
#             "GeneralRateStyle": 5,
#             "PoorCount": 2394,
#             "PoorRate": 0.02,
#             "PoorRateShow": 2,
#             "PoorRateStyle": 3
#         }
#     ]
# }

def __getCommentCount_JD__(sku_list):
    # http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=1279827
    sku_list2 = []
    for item in sku_list:
        sku_list2.append('%s' %item)
    sku_str = ','.join(sku_list2)
    api_url = 'http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=%s' %sku_str
    json_str = url_utils.getWebResponse(api_url)
    ret_list = []
    try:
        ret_map = json.loads(json_str)
        ret_list = ret_map['CommentsCount']
    except:
        logging.error('JD_API::getCommentCount_JD() failed, sku_id = %s' %sku_id)
    return ret_list

def getCommentCount_JD(sku_list):
    return __accumulative_call__(sku_list,50,__getCommentCount_JD__)


# PROMO - CATEGORY

# {
#     "quan": {
#         "title": "买平板电视满1000就送3000元飞利浦XS1音响指定优惠东券",
#         "actUrl": "http://sale.jd.com/act/hO6i4F3cmPTUQEL.html"
#     },
#     "adsStatus": 200,
#     "ads": [ ],
#     "quanStatus": 200,
#     "promStatus": 200,
#     "prom": [ ]
# }

def get_Promo_Category(category_id):
    # http://cd.jd.com/promotion/v2?skuId=1&area=1_72_2799_123&cat=737%2C794%2C798
    cat_id = category_id.replace('-','%2C')
    api_url = 'http://cd.jd.com/promotion/v2?skuId=1&area=1_72_2799_123&cat=%s' %cat_id
    json_str = url_utils.getWebResponse(api_url,'gbk')
    ret_map = {}
    #print json_str
    try:
        obj = json.loads(json_str)
        if obj['quanStatus']==200:
            ret_map['quan'] = obj['quan']
        if obj['adsStatus']==200:
            ret_map['ads'] = obj['ads']
        if obj['promStatus']==200:
            ret_map['prom'] = obj['prom']
    except:
        logging.error('JD_API::get_Promo_Category() failed, category_id = %s' %category_id)
    return ret_map

# PROMO - SKU
def get_Promo_Sku(sku_id):
    # http://cd.jd.com/promotion/v2?skuId=1279827&area=1_72_2799_123&cat=670,729,7311199999
    api_url = 'http://cd.jd.com/promotion/v2?skuId=%s&area=1_72_2799_123&cat=670,729,7311199999' %sku_id
    json_str = url_utils.getWebResponse(api_url,'gbk')
    ret_map = {}
    #print json_str
    try:
        obj = json.loads(json_str)
        if obj['quanStatus']==200:
            ret_map['quan'] = obj['quan']
        if obj['adsStatus']==200:
            ret_map['ads'] = obj['ads']
        if obj['promStatus']==200:
            ret_map['prom'] = obj['prom']
    except:
        logging.error('JD_API::get_Promo_Sku() failed, sku_id = %s' %sku_id)
    return ret_map


if __name__ == "__main__":
    #print getPrices_JD([1279171,595936,1279827,1279171,595936,1279827])
    # sql = 'select distinct sku_id from jd_item_dynamic limit 183'
    # retrows = dbhelper.executeSqlRead2(sql)
    # alist = []
    # for row in retrows:
    #     alist.append(row[0])
    print get_Promo_Sku(1279171)
    print getCommentCount_JD([1279171])


