# encoding: utf-8

import jd_API
import dbhelper
import timeHelper
import crawler_helper
import json

def crawl_sku_comment_count(sku_list):
    clist = jd_API.getCommentCount_JD(sku_list)
    if len(clist)==0:
        return {'status':-1,'msg':'jd api returned no result for sku_list'}
    if len(clist)!=len(set(sku_list)):
        return {'status':-1,'msg':'jd api return size mismatch, size of sku:%s, size of api:%s' %(len(set(sku_list)),len(clist))}
    vlist = []
    dt = timeHelper.getNow()
    for cdict in clist:
        tp = []
        cdict['dt'] = dt
        for key in cdict:
            tp.append(cdict[key])
        vlist.append(tp)

    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_item_comment_count',
        num_cols=len(clist[0]),
        value_list=vlist,
        is_many=True
    )

def crawl_sku_stock_status(sku_list):
    clist = jd_API.get_Stock_Status(sku_list)
    if len(clist)==0:
        return {'status':-1,'msg':'jd api returned no result for sku_list'}
    if len(clist)!=len(set(sku_list)):
        return {'status':-1,'msg':'jd api return size mismatch, size of sku:%s, size of api:%s' %(len(set(sku_list)),len(clist))}
    vlist = []
    dt = timeHelper.getNowLong()
    key_list = ['sku_id','dt','a','b','c','l','j','stock_json']
    for cdict in clist:
        cdict['stock_json'] = json.dumps(cdict)
        cdict['dt'] = dt
        tp = []
        for key in key_list:
            # print 'key=%s\tvalue=%s' %(key,cdict[key])
            if key in cdict.keys():
                tp.append(cdict[key])
            else:
                tp.append(None)
        vlist.append(tp)
        # print '-'*60

    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_item_stock',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True
    )

def crawl_category_promo(category_id):
    rdict = jd_API.get_Promo_Category(category_id)
    dt = timeHelper.getNow()
    if len(rdict)==0:
        return {
            'status':0,
            'msg':'empty in return, category_id=%s' %category_id
        }
    quan = json.dumps(rdict['quan'])
    ads = json.dumps(rdict['ads'])
    prom = json.dumps(rdict['prom'])
    vlist = [[
        category_id,
        dt,
        quan if quan!='[]' else None,
        ads if ads!='[]' else None,
        prom if prom!='[]' else None
    ]]
    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_promo_category',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True
    )


def crawl_item_promo(sku_id):
    rdict = jd_API.get_Promo_Sku(sku_id)
    dt = timeHelper.getNow()
    quan = json.dumps(rdict['quan'])
    ads = json.dumps(rdict['ads'])
    prom = json.dumps(rdict['prom'])
    vlist = [[
        sku_id,
        dt,
        quan if quan!='[]' else None,
        ads if ads!='[]' else None,
        prom if prom!='[]' else None
    ]]
    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_promo_item',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True
    )


if __name__ == '__main__':

    #print crawl_sku_comment_count([1279171,595936,1279827,1279171,595936,1279827])
    #print crawl_category_promo('737-794-798')
    # print crawl_item_promo(1510479)
    sql = 'select distinct sku_id from jd_item_dynamic limit 120'
    retrows = dbhelper.executeSqlRead2(sql)
    alist = []
    for row in retrows:
        alist.append(row[0])

    print crawl_sku_stock_status(alist)