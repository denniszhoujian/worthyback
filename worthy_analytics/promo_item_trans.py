# encoding: utf-8

from datasys import dbhelper,timeHelper, crawler_helper
import time
import json
from datasys import jd_API

def read_Promo_Items_Quan() :

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



def read_Promo_Items_Promo() :

    sql = '''
        select sku_id, promo_json from jd_promo_item_latest
        where promo_json is not NULL
    '''
    retrows = dbhelper.executeSqlRead(sql)

    adict = {}
    for row in retrows:
        json_str = row['promo_json'].strip()
        if json_str not in adict:
            adict[json_str] = []
        vlist = adict[json_str]
        vlist.append(row['sku_id'])

    for key in adict:
        obj = json.loads(key)
        pots = obj['pickOneTag']
        for pot in pots:
            if pot['code'] == '19':
                name = pot['name']
                content = pot['content']
                adurl = pot['adurl']
                print "name"
                print name
                print content
                print adurl

        ending = obj['ending']
        tags = obj['tags']
        skus = adict[key]

        print "ending = %s" %ending
        print "tags"
        for tag in tags:
            for k in tag:
                print "%s :: %s" %(k,tag[k])
        print skus
        print '-'*60

    # print json.dumps(adict)
    print "ok"

def processItemPromo():
    vlist = []
    glist = []
    update_date = timeHelper.getNow()
    recent = timeHelper.getTimeAheadOfNowDays(2)
    sql = '''
        select sku_id, dt, promo_json from jd_promo_item_latest
        where promo_json is not NULL and LENGTH(promo_json)>100
        and dt>="%s"
    ''' %recent
    retrows = dbhelper.executeSqlRead(sql)
    num_error = 0
    num17 = 0
    print "Total rows with promo_json: %s" %len(retrows)
    for row in retrows:
        sku_id = row['sku_id']
        dt = row['dt']
        obj = None
        try:
            obj = json.loads(row['promo_json'])
        except:
            num_error += 1
            print 'ERROR: json.loads()'
            print row['promo_json']
            continue
        rtags = obj['pickOneTag']
        for tag in rtags:
            pid = tag['pid']
            code = tag['code']
            # 不记录加价购
            if code == "17":
                num17 += 1
                continue
            name = tag['name']
            content = tag['content']
            adurl = tag['adurl'] if 'adurl' in tag else ""
            tp = [sku_id, dt, pid, code, name, content, adurl, update_date]
            vlist.append(tp)
        tags = obj['tags']
        for tag in tags:
            pid = tag['pid']
            code = tag['code']
            name = tag['name']
            if code == "10":
                # gift
                gifts = tag['gifts']
                for gift in gifts:
                    gift_name = gift['nm']
                    gift_num = gift['num'] if 'num' in gift else 1
                    gift_image = gift['mp'] if 'mp' in gift else ""
                    gift_sku_id = gift['sid'] if 'sid' in gift else ""
                    gift_gt = gift['gt'] if 'gt' in gift else ""
                    gift_gs = gift['gs'] if 'gs' in gift else ""
                    tp_gift = [sku_id,dt,pid,code, name, gift_name, gift_num, gift_image, gift_sku_id, gift_gt, gift_gs, update_date]
                    glist.append(tp_gift)
            else:
                content = tag['content']
                adurl = tag['adurl'] if 'adurl' in tag else ""
                tp = [sku_id, dt, pid, code, name, content, adurl, update_date]
                vlist.append(tp)

    # print num of errors
    print "num of errors: %s" %num_error
    print 'num17: %s' %num17
    print 'vlist len: %s' %len(vlist)
    print 'glist len: %s' %len(glist)

    # persist in DB
    ret1 = ret2 = None
    if len(vlist)>0:
        ret1 = crawler_helper.persist_db_history_and_latest(
            table_name='jd_analytic_promo_item',
            num_cols=len(vlist[0]),
            value_list=vlist,
            is_many=True
        )
    print "ret1 for promo = %s" %ret1
    if len(glist)>0:
        ret2 = crawler_helper.persist_db_history_and_latest(
            table_name='jd_analytic_promo_gift',
            num_cols=len(glist[0]),
            value_list=glist,
            is_many=True
        )
    print "ret2 for gift = %s" %ret2


def process_gift_value(for_date = None):
    if for_date is None:
        for_date = timeHelper.getNow()
    sql = 'select * from jd_analytic_promo_gift where update_date = "%s"' %for_date
    retrows = dbhelper.executeSqlRead(sql)
    sku_list = []
    for row in retrows:
        sku_list.append(row['gift_sku_id'])
    price_map = {}
    for row in retrows:
        gift_sku_id = row['gift_sku_id']
        gift_num = 1
        try:
            gift_num = int(row['gift_num'])
        except:
            pass

    pass


def read_Promo_Items_Ads():
    sql = '''
    select sku_id, ads_json from jd_promo_item_latest limit 1000
    '''
    retrows = dbhelper.executeSqlRead(sql)
    for row in retrows:
        js = row['ads_json']
        obj = json.loads(js)
        for item in obj:
            if len(item['ad'])>0:
                print item['ad']
                print row['sku_id']


if __name__ == "__main__":
    # read_Promo_Items_Quan()
    # read_Promo_Items_Promo()
    # read_Promo_Items_Ads()
    processItemPromo()
    pass