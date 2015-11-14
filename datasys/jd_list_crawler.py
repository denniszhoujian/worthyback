# encoding: utf-8

import sys
import time
import logging
import timeHelper
import url_utils
import jd_list_resolver
import jd_API
import dbhelper
import crawler_helper

reload(sys)
sys.setdefaultencoding('utf8')

# set to 0.1 has problem, try 0.5
SLEEP_TIME = 0.3
SLEEP_PRICE_API = 0.1

def __get_category_page_url__(category_id, page_num=1):
    # http://list.jd.com/list.html?cat=9987%2C653%2C655&delivery=1&page=1&stock=0
    category_id = '%s' %category_id
    page_url = "http://list.jd.com/list.html?cat=%s&delivery=1&page=%s&stock=0" % (category_id.replace('-','%2C'),page_num)
    # print page_url
    return page_url

def __up_roll_category_id__(category_id):
    cat_reverse = category_id[::-1]
    idx = cat_reverse.find('-')
    if idx < 0:
        return None
    cat_trunc = cat_reverse[idx+1:len(cat_reverse)]
    ret = cat_trunc[::-1]
    return ret

#def __add_price_to_list__(product_list):


def crawl_category(category_id):

    logging.debug('category_id = %s -- page 1' %(category_id))
    url = __get_category_page_url__(category_id,1)
    # print url
    html = url_utils.getWebResponse(url,'utf-8')
    if html == "":
        html = url_utils.getWebResponse(url,'gb18030')
    if html == "":
        html = url_utils.getWebResponse(url, 'gbk')
    total_pages = jd_list_resolver.resolveTotalPageNum(html)

    product_list = jd_list_resolver.resolveProductListFromPage(html)

    while len(product_list) == 0 and category_id is not None:
        category_id = __up_roll_category_id__(category_id)
        return crawl_category(category_id)

    if category_id is None or len(product_list)==0:
        return {'status':-1, 'msg': 'No item in category product list'}

    for page_iter in range(2,total_pages+1):
        logging.debug('category_id = %s -- page %s' %(category_id,page_iter))
        url = __get_category_page_url__(category_id,page_iter)
        html = url_utils.getWebResponse(url,'utf-8')
        product_list = product_list + jd_list_resolver.resolveProductListFromPage(html)
        time.sleep(SLEEP_TIME)

    sku_list = []
    for product_tp in product_list:
        sku_id = product_tp[0]
        sku_list.append(sku_id)

    # Get price of all products
    price_obj = jd_API.getPrices_JD(sku_list,sleep_time=SLEEP_PRICE_API)

    ret_obj = {
        'status': -1,
        'affected_rows': -1,
        'sku_count': -1
    }
    total_goods_num = len(product_list)

    # for item in product_list:
    #     print item[0]
    # print '='*80

    # combine product list and price list, timestamp, category_id
    for i in xrange(total_goods_num):
        product_id = product_list[i][0]
        pkey = '%s' %product_id
        if pkey in price_obj:
            product_list[i] = product_list[i] + (price_obj[pkey][0],price_obj[pkey][1],price_obj[pkey][2],) #nowdate,nowtime,)
        else:
            logging.error('Error: product_id=%s cannot get result' %(product_id,price_id))
            continue

    # persist in database
    # (sku_id,sku_title,sku_url,sku_thumnail_url,sku_stock,comment_count,is_global,is_pay_on_delivery,is_free_gift,sku_icon_url, price, price_m, update_date,update_time, category_id)
    # sql = '''
    #   replace into jd_item_dynamic (sku_id,title,url,thumbnail_url,stock_status,comment_count,is_global,is_pay_on_delivery,
    #   has_free_gift,icon_url,price,price_m,price_pcp,update_date,update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #   '''
    # affected_rows = dbhelper.executeSqlWriteMany(sql,product_list)

    ret = crawler_helper.persist_db_history_and_latest(
        table_name='jd_item_dynamic',
        num_cols=len(product_list[0]),
        value_list=product_list,
        is_many=True,
        need_history=True
    )

    logging.debug('Saved to DB -- category_id = %s -- sku_count=%s' %(category_id,total_goods_num))
    logging.debug('%s' %ret)

    # HANDLE JD_ITEM_CATEGORY
    item_cat_list = []
    for prod in product_list:
        item_cat_list.append((prod[0],category_id,))
    sql2 = 'replace into jd_item_category values (%s,%s)'
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,item_cat_list)
    logging.debug('Saved to DB - item_category - affected rows = %s' %affected_rows2)
    if affected_rows2<=0:
        logging.error('Saving to item_category error, category_id = %s' %category_id)


    # HANDLE JD_ITEM_FIRSTSEEN
    nowtime = timeHelper.getNowLong()
    nowdate = timeHelper.getNow()
    sql3 = 'insert ignore into jd_item_firstseen values(%s,"%s","%s")'
    ftlist = []
    for item in product_list:
        ftlist.append([item[0],nowtime,nowdate])
    affected_rows3 = dbhelper.executeSqlWriteMany(sql3,ftlist)

    ret_obj = {
        'status': 0 if ret['status']==0 and affected_rows2>0 else -1,
        'item_dynamic': ret,
        'item_category': affected_rows2,
        'item_first_seen': affected_rows3,
    }

    return ret_obj


if __name__ == '__main__':
    import mylog
    mylog.configLogging('test_list_crawler')
    cat_id = '12218-12219'
    print crawl_category(cat_id)
    # print __up_roll_category_id__('652')
