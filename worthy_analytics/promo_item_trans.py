# encoding: utf-8

from datasys import dbhelper,timeHelper, crawler_helper
import time
import json
from datasys import jd_API
import MySQLdb
import re

MAX_DEDUCTION_CONSTANT = 99999999

# def read_Promo_Items_Quan() :
#
#     sql = '''
#         select * from jd_promo_item_latest where quan_json is not NULL
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#
#     adict = {}
#
#     for row in retrows:
#         obj = json.loads(row['quan_json'])
#         url = "http://item.jd.com/%s.html" %row['sku_id']
#         # print "%s\t\t%s" %(obj['title'],url)
#         # print ("\n")
#         adict[obj['title']] = url
#     pass
#
#     for item in adict:
#         print item
#         print adict[item]
#
# def read_Promo_Items_Ads():
#     sql = '''
#     select sku_id, ads_json from jd_promo_item_latest limit 1000
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#     for row in retrows:
#         js = row['ads_json']
#         obj = json.loads(js)
#         for item in obj:
#             if len(item['ad'])>0:
#                 print item['ad']
#                 print row['sku_id']
#
#
# def read_Promo_Items_Promo() :
#
#     sql = '''
#         select sku_id, promo_json from jd_promo_item_latest
#         where promo_json is not NULL
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#
#     adict = {}
#     for row in retrows:
#         json_str = row['promo_json'].strip()
#         if json_str not in adict:
#             adict[json_str] = []
#         vlist = adict[json_str]
#         vlist.append(row['sku_id'])
#
#     for key in adict:
#         obj = json.loads(key)
#         pots = obj['pickOneTag']
#         for pot in pots:
#             if pot['code'] == '19':
#                 name = pot['name']
#                 content = pot['content']
#                 adurl = pot['adurl']
#                 print "name"
#                 print name
#                 print content
#                 print adurl
#
#         ending = obj['ending']
#         tags = obj['tags']
#         skus = adict[key]
#
#         print "ending = %s" %ending
#         print "tags"
#         for tag in tags:
#             for k in tag:
#                 print "%s :: %s" %(k,tag[k])
#         print skus
#         print '-'*60
#
#     # print json.dumps(adict)
#     print "ok"

PROCESS_RAW_PROMO_RECENCY_HOURS = 24
PROCESS_PROMO_DETAIL_RECENCY_HOURS = 24

def processItemPromo():
    vlist = []
    glist = []
    update_date = timeHelper.getNowLong()
    recent = timeHelper.getTimeAheadOfNowHours(PROCESS_RAW_PROMO_RECENCY_HOURS,'%Y-%m-%d %H:%M:%S')
    print 'A long query will be running now, need wait...'
    sql = '''
        select sku_id, dt, promo_json from jd_promo_item_latest
        where promo_json is not NULL and LENGTH(promo_json)>100
        and dt>="%s"
    ''' %recent
    retrows = dbhelper.executeSqlRead(sql,is_dirty=True)
    # total_rows = len(retrows)
    num_error = 0
    num17 = 0
    print 'completed!'
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
        ret1 = crawler_helper.persist_db_history_and_lastest_empty_first(
            table_name='jd_analytic_promo_item',
            num_cols=len(vlist[0]),
            value_list=vlist,
            is_many=True
        )
    print "ret1 for promo = %s" %ret1
    if len(glist)>0:
        ret2 = crawler_helper.persist_db_history_and_lastest_empty_first(
            table_name='jd_analytic_promo_gift',
            num_cols=len(glist[0]),
            value_list=glist,
            is_many=True
        )
    print "ret2 for gift = %s" %ret2
    return _generate_mixed_ret([ret1,ret2])


def _generate_mixed_ret(ret_list):
    ret_obj = {
        'status': 0,
        'data': []
    }
    for ret in ret_list:
        ret_obj['status'] += ret['status']
        ret_obj['data'].append(ret)
    return ret_obj

## 下面方法必须在当天处理完promo_item的gift数据之后运行
def process_gift_value(for_date = None):
    # today = timeHelper.getNowLong()
    today = timeHelper.getTimeAheadOfNowHours(24,format='%Y-%m-%d %H:%M:%S')

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
    a.update_date >= '%s'
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
        'max': MAX_DEDUCTION_CONSTANT
    }
    plist = content.split(repeat_text)
    if len(plist) <= 1:
        return ret
    max_deduction_amount = MAX_DEDUCTION_CONSTANT
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
        tp = (reach_amount,deduction_amount,1 if repeated_deduction else 0)
        retlist.append(tp)
        # print tp
    return ret

def _extract_reach_deduction_array(content):
    ret1 = _extract_reach_deduction_array_of_type(content, True)
    ret2 = _extract_reach_deduction_array_of_type(content, False)
    ret = {
        'data':ret1['promo'] + ret2['promo'],
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
    today = timeHelper.getTimeAheadOfNowHours(PROCESS_PROMO_DETAIL_RECENCY_HOURS,'%Y-%m-%d %H:%M:%S')
    # today = timeHelper.getTimeAheadOfNowDays(1)
    sql = '''
        select a.*, b.title, b.price, d.id as category_id, d.name as category_name from

        jd_analytic_promo_item_latest a
        left join
        jd_item_dynamic_latest b
        on a.sku_id = b.sku_id

        left JOIN
        jd_item_category c
        on a.sku_id = c.sku_id

        left join
        jd_category d
        on c.category_id = d.id

        where a.dt >= "%s"
        and b.sku_id is not NULL
        and b.price is not NULL
    ''' %today
    # print sql
    retrows = dbhelper.executeSqlRead(sql, is_dirty=True)

    vlist = []
    vlist19 = []

    dt = timeHelper.getNowLong()

    print 'num total promo_item rows: %s' %len(retrows)
    # exit()

    num_15 = 0
    num_19 = 0
    num_15_repeated = 0

    for row in retrows:
        sku_id = row['sku_id']
        code = int(row['code'])
        content = row['content'] if 'content' in row else ""
        adurl = row['adurl'] if 'adurl' in row else ""
        origin_dt = row['dt']
        pid = row['pid']
        name = row['name'] if 'name' in row else ""
        price = float("%s" %row['price'])
        category_id = row['category_id']
        category_name = row['category_name']
        title = row['title']
        if code == 15:
            num_15 += 1
            ret = _extract_reach_deduction_array(content)

            # print content
            # print ret
            # print '-'*60
            stat_has_repeat = False
            max_deduction = float(ret['max'])
            for item in ret['data']:
                try:
                    reach = float(item[0])
                    deduction = float(item[1])

                    is_repeat = item[2]
                    if is_repeat==1:
                        stat_has_repeat = True
                    dr_ratio = deduction*1.0/reach
                    maxp_ratio = max_deduction*1.0/price if max_deduction > 0 else 1.0
                    could_deduct = 0
                except Exception as e:
                    print "reach:%s, deduction:%s" %(reach,deduction)
                    print e
                    continue

                if price >= reach and reach>0:
                    if is_repeat:
                        times = price // reach
                    else:
                        times = 1
                    could_deduct = times * deduction
                    if could_deduct > max_deduction:
                        could_deduct = max_deduction
                single_discount_rate = could_deduct/price
                tp =[sku_id, dt, title, price, is_repeat, reach, deduction, max_deduction, dr_ratio, maxp_ratio, single_discount_rate, category_id, category_name, pid, code, name, content, adurl, origin_dt]
                vlist.append(tp)

            if stat_has_repeat:
                num_15_repeated += 1

        elif code == 19:
            num_19 += 1
            # 满几件打折或者降低多少
            type_word_list = ["总价打","商品价格"]
            # 0: 直接打折
            # 1: 减商品价格
            # 2: 其他
            deduct_type = 2
            for type_word in type_word_list:
                if content.find(type_word) >= 0:
                    deduct_type = 0
                    break
            if deduct_type==2:
                print "NEW TYPE OF DISCOUNT FOUND!!!"
                print content
                print "NEW TYPE OF DISCOUNT FOUND!!!"

            pt = re.compile(u'[\d.]+',re.U)
            pts = pt.findall(content)
            if len(pts) != 2:
                if '可购买热销商品' not in content:
                    print content
                    print "NEW PATTERN ABOVE"
            reach_num = discount = free_num = rf_ratio = None
            reach_num = pts[0]
            if deduct_type==0:
                discount = pts[1]
            elif deduct_type==1:
                free_num = pts[1]
                rf_ratio = float(free_num*1.0/reach_num)

            tp19 =[sku_id, dt, title, price, deduct_type, reach_num, discount, free_num, rf_ratio, category_id, category_name, pid, code, name, content, adurl, origin_dt]
            vlist19.append(tp19)


        else:
            pass

    print "code = 15, cases = %s" %num_15
    print "code = 15, repeated = %s" %num_15_repeated
    print "rows to insert = %s" %len(vlist)

    pret15 = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_promo_deduction',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True
    )

    print "code = 19, cases = %s" %num_19
    print "rows to insert = %s" %len(vlist19)

    pret19 = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_promo_discount',
        num_cols=len(vlist19[0]),
        value_list=vlist19,
        is_many=True
    )

    return _generate_mixed_ret([pret15, pret19])

# def _transform_retrow_to_list(retrows, col_name):
#     list2 = []
#     for row2 in retrows:
#         list2.append(row2[col_name])
#     return list2

# def _delete_skus_from_tables(sku_list,table_list):
#     if len(sku_list)==0 or len(table_list)==0:
#         return 0
#     sku_str = ','.join(sku_list)
#     total_afr = 0
#     for table in table_list:
#         sql = 'delete from %s where sku_id in (%s)' %(table, sku_str)
#         afr = dbhelper.executeSqlWrite1(sql)
#         total_afr += afr
#     return total_afr
#
# def _transform_retrows_to_dict(retrows, col1_name, col2_name):
#     ret = {}
#     for row in retrows:
#         id = row[col1_name]
#         if id in ret:
#             ret[id].append(row[col2_name])
#         else:
#             ret[id] = [row[col2_name],]
#     return ret
#
# def _find_time_mismatch(retrows1,retrows2,col1_name,col2_name):
#     list1_dict = _transform_retrows_to_dict(retrows1,'sku_id',col1_name)
#     vlist = []
#     for row in retrows2:
#         if row[col2_name] not in list1_dict[row['sku_id']]:
#             vlist.append(row['sku_id'])
#     return vlist

# def update_promo_results():
#     print 'Set of long query'
#     sql_all = '''
#     select sku_id,dt,promo_json
#     from jd_promo_item_latest
#     -- where
#     -- length(promo_json)<100
#     '''
#     # retrows = dbhelper.executeSqlRead(sql)
#     # non_list = _transform_retrow_to_list(retrows, 'sku_id')
#     # print 'Finished 1 of 6'
#
#     # sql_all = 'select sku_id, dt from jd_promo_item_latest'
#     retrows_all = dbhelper.executeSqlRead(sql_all, is_dirty=True)
#     print 'Finished 2 of 6'
#     non_list = []
#     for row in retrows_all:
#         if len(row['promo_json']) < 100:
#             non_list.append(row['sku_id'])
#
#     sql5 = 'select sku_id,dt from jd_analytic_promo_item_latest'
#     retrows5 = dbhelper.executeSqlRead(sql5, is_dirty=True)
#     item_list = _transform_retrow_to_list(retrows5, 'sku_id')
#     list5 = list(set(non_list).intersection(set(item_list)))
#     list55 = _find_time_mismatch(retrows_all,retrows5,'dt','dt')
#     list5 = list(set(list5) + set(list55))
#     print 'Finished 3 of 6'
#
#     sql2 = 'select sku_id,origin_time from jd_analytic_promo_deduction_latest'
#     retrows2 = dbhelper.executeSqlRead(sql2, is_dirty=True)
#     deduction_list = _transform_retrow_to_list(retrows2, 'sku_id')
#     list2 = list(set(non_list).intersection(set(deduction_list)))
#     list22 = _find_time_mismatch(retrows_all,retrows2,'dt','origin_time')
#     list2 = list(set(list2) + set(list22))
#     print 'Finished 4 of 6'
#
#     sql3 = 'select sku_id,origin_time from jd_analytic_promo_discount_latest'
#     retrows3 = dbhelper.executeSqlRead(sql3, is_dirty=True)
#     discount_list = _transform_retrow_to_list(retrows3, 'sku_id')
#     list3 = list(set(non_list).intersection(set(discount_list)))
#     list33 = _find_time_mismatch(retrows_all,retrows3,'dt','origin_time')
#     list3 = list(set(list3) + set(list33))
#     print 'Finished 5 of 6'
#
#     sql4 = 'select sku_id,origin_time  from jd_analytic_promo_gift_latest'
#     retrows4 = dbhelper.executeSqlRead(sql4, is_dirty=True)
#     gift_list = _transform_retrow_to_list(retrows4, 'sku_id')
#     list4 = list(set(non_list).intersection(set(gift_list)))
#     list44 = _find_time_mismatch(retrows_all,retrows4,'dt','origin_time')
#     list4 = list(set(list4) + set(list44))
#     print 'Finished 6 of 6\n'
#     print "removing invalid promotions now..."
#     print "item_promo: %s\ndeduction: %s\ndiscount: %s\ngift: %s" %(len(list5),len(list2),len(list3),len(list4))
#
#     print list5,list2,list3,list4
#     exit()
#
#     afr5 = _delete_skus_from_tables(list5,['jd_analytic_promo_item_latest'])
#     afr2 = _delete_skus_from_tables(list2,['jd_analytic_promo_deduction_latest'])
#     afr3 = _delete_skus_from_tables(list3,['jd_analytic_promo_discount_latest'])
#     afr4 = _delete_skus_from_tables(list4,['jd_analytic_promo_gift_latest', 'jd_analytic_promo_gift_valued'])
#
#     print "Removed: "
#     print "item_promo: %s\ndeduction: %s\ndiscount: %s\ngift: %s" %(afr5,afr2,afr3,afr4)
#     return 0


if __name__ == "__main__":
    print processItemPromo()
    print process_gift_value()
    print process_promo_detail()
    # update_promo_results()

    pass