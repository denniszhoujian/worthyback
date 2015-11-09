# encoding: utf-8

import sys
import jd_detail_resolver
import url_utils
from memcachedHelper import memcachedStatic
import timeHelper
import dbhelper
import logging

mc = memcachedStatic.getMemCache()

MEMCACHE_DETAIL_HTML_TIMEOUT = 7200  # in seconds

def __get_detail_page_url__(sku_id):
    url = 'http://item.jd.com/%s.html' %sku_id
    return url

def __get_detail_page_content__(sku_id):
    mc_key = 'JD_DETAIL_HTML9_%s' %sku_id
    mcv = mc.get(mc_key)
    if mcv is not None:
        return mcv
    html = ""
    try:
        url = __get_detail_page_url__(sku_id)
        html = url_utils.getWebResponse(url)
        html = html.decode('gbk')
    except Exception as e:
        try:
            html = html.decode('gb18030')
        except:
            logging.warning('url=%s, failed decoding using GBK or GB18030, using utf-8 now... may cause problems' %url)
    if len(html) > 0:
        mc.set(mc_key,html,MEMCACHE_DETAIL_HTML_TIMEOUT)
    return html


def crawl_detail_property(sku_id):
    html = __get_detail_page_content__(sku_id)
    prop_map = jd_detail_resolver.resolve_Properties(html)
    update_time = timeHelper.getNow()
    vlist = []
    if len(prop_map) == 0:
        return {'status':0}
    for p_key in prop_map:
        p_value = prop_map[p_key]
        tp = (sku_id, update_time, p_key, p_value)
        vlist.append(tp)
    sql = 'replace into jd_item_property values(%s,%s,%s,%s)'
    affected_rows = dbhelper.executeSqlWriteMany(sql,vlist)
    sql2 = 'replace into jd_item_property_latest values(%s,%s,%s,%s)'
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,vlist)
    ret = {
        'status': -1,
        'affected_rows': affected_rows,
        'affected_rows2': affected_rows2
    }
    if affected_rows>0 and affected_rows2>0:
        ret['status'] = 0
    return ret

def crawl_detail_images(sku_id):
    html = __get_detail_page_content__(sku_id)
    img_list = jd_detail_resolver.resolve_Images(html)
    logging.debug(img_list)
    if len(img_list)==0:
        return {'status':-1}
    vlist = []
    update_time = timeHelper.getNow()
    for img in img_list:
        tp = (sku_id, update_time, img)
        vlist.append(tp)
    sql = 'replace into jd_item_images values(%s,%s,%s)'
    affected_rows = dbhelper.executeSqlWriteMany(sql,vlist)
    sql2 = 'replace into jd_item_images_latest values(%s,%s,%s)'
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,vlist)
    ret = {
        'status': -1,
        'affected_rows': affected_rows,
        'affected_rows2': affected_rows2
    }
    if affected_rows>0 and affected_rows2>0:
        ret['status'] = 0
    return ret

def crawl_detail_all(sku_id):
    ret1 = crawl_detail_property(sku_id)
    ret2 = crawl_detail_images(sku_id)
    status = ret1['status'] # + ret2['status']
    ret = {
        'status':status,
        'msg':[ret1,ret2]
    }
    return ret



if __name__ == '__main__':
    print crawl_detail_property(1688360)