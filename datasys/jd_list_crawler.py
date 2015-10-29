# encoding: utf-8

import sys
import time
import logging
import timeHelper
import url_utils
import jd_list_resolver
import jd_API
import dbhelper


reload(sys)
sys.setdefaultencoding('utf8')

# set to 0.1 has problem, try 0.5
SLEEP_TIME = 0.5


def __get_category_page_url__(category_id, page_num=1):
    # http://list.jd.com/list.html?cat=9987%2C830%2C863&delivery=1&page=1
    category_id = '%s' %category_id
    page_url = "http://list.jd.com/list.html?cat=%s&delivery=1&page=%s" % (category_id.replace('-','%2C'),page_num)
    return page_url


#def __add_price_to_list__(product_list):


def crawl_category(category_id):

    logging.info('category_id = %s -- page 1' %(category_id))
    html = url_utils.getWebResponse(__get_category_page_url__(category_id,1),'utf-8')
    total_pages = jd_list_resolver.resolveTotalPageNum(html)

    product_list = jd_list_resolver.resolveProductListFromPage(html)

    for page_iter in range(2,total_pages+1):
        logging.info('category_id = %s -- page %s' %(category_id,page_iter))
        url = __get_category_page_url__(category_id,page_iter)
        html = url_utils.getWebResponse(url,'utf-8')
        product_list = product_list + jd_list_resolver.resolveProductListFromPage(html)
        time.sleep(SLEEP_TIME)

    sku_list = []
    for product_tp in product_list:
        sku_id = product_tp[0]
        sku_list.append(sku_id)

    # Get price of all products
    price_obj = jd_API.getPrices_JD(sku_list)

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
    nowtime = timeHelper.getNowLong()
    nowdate = timeHelper.getNow()
    for i in xrange(total_goods_num):
        product_id = product_list[i][0]
        pkey = '%s' %product_id
        if pkey in price_obj:
            product_list[i] = product_list[i] + (price_obj[pkey][0],price_obj[pkey][1],price_obj[pkey][2],nowdate,nowtime,category_id,)
        else:
            logging.error('Error: product_id=%s cannot get result' %(product_id,price_id))
            continue

    # persist in database
    # (sku_id,sku_title,sku_url,sku_thumnail_url,sku_stock,comment_count,is_global,is_pay_on_delivery,is_free_gift,sku_icon_url, price, price_m, update_date,update_time, category_id)
    sql = '''
      replace into jd_item_dynamic (sku_id,title,url,thumbnail_url,stock_status,comment_count,is_global,is_pay_on_delivery,
      has_free_gift,icon_url,price,price_m,price_pcp,update_date,update_time,category_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
      '''
    affected_rows = dbhelper.executeSqlWriteMany(sql,product_list)
    logging.info('Saved to DB -- category_id = %s -- sku_count=%s -- affected_rows=%s' %(category_id,total_goods_num,affected_rows))

    ret_obj = {
        'status': 0,
        'affected_rows': affected_rows,
        'sku_count': total_goods_num
    }

    return ret_obj


if __name__ == '__main__':

    print crawl_category('737-738-748')