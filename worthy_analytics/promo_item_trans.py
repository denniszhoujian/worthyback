# encoding: utf-8

from datasys import dbhelper,timeHelper, crawler_helper
import time
import json
from datasys import jd_API
import MySQLdb
import re

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
            # print 'ERROR: json.loads()'
            # print row['promo_json']
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
    print "num of errors: %s (like json.loads error)" %num_error
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


## 下面方法必须在当天处理完promo_item的gift数据之后运行
def process_gift_value(for_date = None):
    today = timeHelper.getNow()

    sql1 = 'delete from jd_analytic_promo_gift_valued'

    sql2 = '''
    insert into jd_analytic_promo_gift_valued

    select

    a.*,
    b.price as price,
    c.price as gift_price,
    c.price*a.gift_num as gift_value,
    (c.price*a.gift_num)/b.price as gift_ratio

    from

    jd_analytic_promo_gift_latest a
    left join
    jd_item_dynamic_latest b
    on a.sku_id = b.sku_id

    left join
    jd_item_dynamic_latest c
    on a.gift_sku_id = c.sku_id

    where
    a.update_date = '%s'
    and b.price is not NULL
    and c.price is not NULL

    order by gift_value DESC

    ''' %today

    afr = -1

    # AS TRANSACTION
    conn = dbhelper.getConnection()
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        retrows = cursor1.execute(sql1)
        retrows2 = cursor1.execute(sql2)
        if retrows2 <= 0:
            raise Exception("process_gift_value: nothing to insert")
        conn.commit()
        afr = cursor1.rowcount
    except Exception as e:
        conn.rollback()
        print e
    finally:
        conn.close()


    #afr = dbhelper.executeSqlWrite1(sql)
    print "affected rows: %s" %afr
    ret = {
        'status': 0 if afr > 0 else -1,
        'affected_rows': afr,
        'rows deleted': retrows,
        'rows_inserted': retrows2
    }
    return ret


def _extract_reach_deduction_array_of_type(content, repeated_deduction=True):
    repeat_text = "每满"
    if not repeated_deduction:
        # print "not"
        repeat_text = "满"
        content = content.replace("每满","")
        # print content

    retlist = []
    ret = {
        'promo':retlist,
        'max': -1
    }
    plist = content.split(repeat_text)
    if len(plist) <= 1:
        return ret
    max_deduction_amount = -1
    for item in plist:
        pt = re.compile(u'[\d.]+',re.U)
        pts = pt.findall(item)
        if len(pts)<2:
            # print '#1 : %s' %pts
            continue
        reach_amount = pts[0]
        deduction_amount = pts[1]

        if len(pts)>2:
            ret['max'] = pts[2]
        tp = (reach_amount,deduction_amount)
        retlist.append(tp)
        # print tp
    return ret

def _extract_reach_deduction_array(content):
    ret1 = _extract_reach_deduction_array_of_type(content, True)
    ret2 = _extract_reach_deduction_array_of_type(content, False)
    ret = {
        'repeated':ret1['promo'],
        'non_repated':ret2['promo'],
        'max': ret1['max']
    }
    return ret




    # index = 999
    # index1 = -1
    # while index > 0:
    #     index = content.find(repeat_text)
    #     if index>0:
    #         index1 = content.find(deduction_text, index+1)



# 15	121244	100295	每满999.00元，可减150.00元现金
# 19	28288	100284	满2件，总价打8.80折
# 3	6243	101709	购买1-200件时享受优惠
# 9	3505	100306	此价格不与套装优惠同时享受
# 18	1959	182341	满499.00元即赠热销商品，赠完即止
# 7	1855	164468	赠100京豆
# 20	745	103666	购买1-99件时享受优惠
# 1	271	101709	企业用户及以上会员可享受会员价：￥568.00
# 16	46	105129	满500.00元另加85.00元即赠热销商品，赠完即止
# 4	17	497412	使用20.00京豆可享受优惠价215.80元
# 6	3	1308514	赠300.00元京券（仅限仅限购买1464854使用使用）


def process_promo_detail():
    # today = timeHelper.getNow()
    today = timeHelper.getTimeAheadOfNowDays(1)
    sql = '''
        select a.*, b.title, b.price, d.id as category_id, d.name as category_name from

        jd_analytic_promo_item_latest a
        left join
        jd_item_dynamic_latest b
        on a.sku_id = b.sku_id and b.sku_id is not NULL

        left JOIN
        jd_item_category c
        on a.sku_id = c.sku_id

        left join
        jd_category d
        on c.category_id = d.id

        where a.update_date = "%s"
    ''' %today
    retrows = dbhelper.executeSqlRead(sql)
    vlist = []
    dt = timeHelper.getNow()
    for row in retrows:
        sku_id = row['sku_id']
        code = int(row['code'])
        content = row['content'] if 'content' in row else ""
        adurl = row['adurl'] if 'adurl' in row else ""
        origin_dt = row['dt']
        pid = row['pid']
        name = row['name'] if 'name' in row else ""
        price = row['price']
        category_id = row['category_id']
        category_name = row['category_name']
        title = row['title']
        if code == 15:
            ret = _extract_reach_deduction_array(content)

            # print content
            # print ret
            # print '-'*60
            max_deduction = ret['max']
            for item in ret['repeated']:
                reach = item[0]
                deduction = [1]
                dr_ratio = deduction*1.0/reach
                maxp_ratio = max_deduction*1.0/price if max_deduction > 0 else 1.0
                
                single_discount_rate = 0
                tp =[sku_id, dt, title, price, 1, reach, deduction, max_deduction, dr_ratio, maxp_ratio, category_id, category_name, pid, code, name, content, adurl, origin_dt]

        elif code == 19:
            pass
        else:
            pass


if __name__ == "__main__":
    # read_Promo_Items_Quan()
    # read_Promo_Items_Promo()
    # read_Promo_Items_Ads()
    #processItemPromo()
    # process_gift_value()

    ret = process_promo_detail()

    pass