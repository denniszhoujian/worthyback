# encoding: utf-8

from datasys import dbhelper,timeHelper, crawler_helper
import time
import json
from datasys import jd_API
import MySQLdb
import re
import datamining_config
import logging

MAX_DEDUCTION_CONSTANT = 99999999


def processItemPromo():
    vlist = []
    glist = []
    update_date = timeHelper.getNowLong()
    recent = timeHelper.getTimeAheadOfNowHours(datamining_config.PROMO_ITEM_RECENCY_HOURS,timeHelper.FORMAT_LONG)
    logging.debug('Reading jd_promo_item_latest...' )
    sql = '''
        select sku_id, dt, promo_json from jd_promo_item_latest
        where promo_json is not NULL and LENGTH(promo_json)>100
        and dt>="%s"
    ''' %recent
    retrows = dbhelper.executeSqlRead(sql,is_dirty=True)
    # total_rows = len(retrows)
    num_error = 0
    num17 = 0
    logging.debug('completed!')
    logging.debug("Total rows with promo_json: %s" %len(retrows))
    for row in retrows:
        sku_id = row['sku_id']
        dt = row['dt']
        obj = None
        try:
            obj = json.loads(row['promo_json'])
        except:
            num_error += 1
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
            name = tag['name'] if 'name' in tag else ""
            if code == "10":
                # gift
                gifts = tag['gifts']
                for gift in gifts:
                    gift_name = "赠品"
                    try:
                        gift_name = gift['nm']
                        gift_num = gift['num'] if 'num' in gift else 1
                        gift_image = gift['mp'] if 'mp' in gift else ""
                        gift_sku_id = gift['sid'] if 'sid' in gift else ""
                        gift_gt = gift['gt'] if 'gt' in gift else ""
                        gift_gs = gift['gs'] if 'gs' in gift else ""
                        tp_gift = [sku_id,dt,pid,code, name, gift_name, gift_num, gift_image, gift_sku_id, gift_gt, gift_gs, update_date]
                        glist.append(tp_gift)
                    except Exception as e:
                        logging.debug("error in extracting gift info for sku_id = %s"%sku_id)
                        logging.debug("%s" %e)
            else:
                content = tag['content']
                adurl = tag['adurl'] if 'adurl' in tag else ""
                tp = [sku_id, dt, pid, code, name, content, adurl, update_date]
                vlist.append(tp)

    logging.error("IGNOR-ABLE: num of errors: %s (like json.loads error)" %num_error)
    logging.debug('num17: %s' %num17 )
    logging.debug('vlist len: %s' %len(vlist) )
    logging.debug('glist len: %s' %len(glist) )

    sql_cb_promo_item = '''
        CREATE TABLE jd_analytic_promo_item_latest (
          sku_id bigint(20) NOT NULL,
          dt datetime NOT NULL,
          pid varchar(255) NOT NULL,
          code varchar(255) NOT NULL,
          name varchar(255) NOT NULL,
          content varchar(255) NOT NULL,
          adurl varchar(255) DEFAULT NULL,
          update_date datetime NOT NULL,
          PRIMARY KEY (sku_id,pid)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    sql_cb_promo_gift = '''
        CREATE TABLE jd_analytic_promo_gift_latest (
          sku_id bigint(20) NOT NULL,
          dt datetime NOT NULL,
          pid varchar(255) NOT NULL,
          code varchar(255) NOT NULL,
          name varchar(255) NOT NULL,
          gift_name varchar(255) NOT NULL,
          gift_num int(11) NOT NULL,
          gift_image varchar(255) DEFAULT NULL,
          gift_sku_id bigint(20) NOT NULL,
          gift_gt varchar(255) DEFAULT NULL,
          gift_gs varchar(255) DEFAULT NULL,
          update_date datetime NOT NULL,
          PRIMARY KEY (sku_id,pid)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    # persist in DB
    ret1 = ret2 = None
    if len(vlist)>0:
        ret1 = crawler_helper.persist_db_history_and_lastest_empty_first(
            table_name='jd_analytic_promo_item',
            num_cols=len(vlist[0]),
            value_list=vlist,
            is_many=True,
            need_history=False,
            sql_create_table=sql_cb_promo_item,
        )
    if len(glist)>0:
        ret2 = crawler_helper.persist_db_history_and_lastest_empty_first(
            table_name='jd_analytic_promo_gift',
            num_cols=len(glist[0]),
            value_list=glist,
            is_many=True,
            need_history=False,
            sql_create_table=sql_cb_promo_gift,
        )

        # record gift
        sglist = []
        cur_time = timeHelper.getNowLong()
        for gg in glist:
            sglist.append([gg[0],cur_time])
        sql_gg = 'insert ignore into jd_analytic_sku_gift values(%s,%s)'
        afr = dbhelper.executeSqlWriteMany(sql_gg,sglist)
        ret3 = {
            'status': 0 if afr > 0 else -1,
            'msg': "",
        }

    return _generate_mixed_ret([ret1,ret2, ret3])


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
    today = timeHelper.getTimeAheadOfNowHours(datamining_config.PROMO_ITEM_RECENCY_HOURS,format='%Y-%m-%d %H:%M:%S')

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
    and b.price>0

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
        logging.error(e)
    finally:
        conn.close()

    logging.debug("affected rows: %s" %afr )
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
        repeat_text = "满"
        content = content.replace("每满","")

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
            continue
        reach_amount = pts[0]
        deduction_amount = pts[1]

        if len(pts)>2:
            ret['max'] = pts[2]
        tp = (reach_amount,deduction_amount,1 if repeated_deduction else 0)
        retlist.append(tp)
    return ret

def _extract_reach_deduction_array(content):
    ret1 = _extract_reach_deduction_array_of_type(content, True)
    ret2 = _extract_reach_deduction_array_of_type(content, False)
    ret = {
        'data':ret1['promo'] + ret2['promo'],
        'max': ret1['max']
    }
    return ret


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
    today = timeHelper.getTimeAheadOfNowHours(datamining_config.PROMO_ITEM_RECENCY_HOURS,'%Y-%m-%d %H:%M:%S')
    # today = timeHelper.getTimeAheadOfNowDays(1)
    sql = '''
        select a.*, b.price, d.id as category_id, d.name as category_name from

        jd_analytic_promo_item_latest a
        left join
        jd_item_price_latest b
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
    logging.debug(sql)
    retrows = dbhelper.executeSqlRead(sql, is_dirty=True)

    vlist = []
    vlist19 = []

    dt = timeHelper.getNowLong()

    logging.debug('num total promo_item rows: %s' %len(retrows) )
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
        # title = row['title']
        if code == 15:
            num_15 += 1
            ret = _extract_reach_deduction_array(content)

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
                    logging.error("reach:%s, deduction:%s" %(reach,deduction) )
                    logging.error(e)
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
                tp =[sku_id, dt, price, is_repeat, reach, deduction, max_deduction, dr_ratio, maxp_ratio, single_discount_rate, category_id, category_name, pid, code, name, content, adurl, origin_dt]
                vlist.append(tp)

            if stat_has_repeat:
                num_15_repeated += 1

        elif code == 19:

            sku_str = "%s" %sku_id

            num_19 += 1
            # 满几件打折或者降低多少
            type_word_list = ["总价打","商品价格"]
            # 0: 直接打折
            # 1: 减商品价格
            # 2: 其他
            deduct_type = 0
            for type_word in type_word_list:
                if content.find(type_word) >= 0:
                    # deduct_type = 0
                    break
                deduct_type += 1

            if deduct_type==2:
                logging.error("NEW TYPE OF DISCOUNT FOUND!!!")
                logging.error(content)
                logging.error("NEW TYPE OF DISCOUNT FOUND!!!")

            pt = re.compile(u'[\d.]+',re.U)
            pts = pt.findall(content)
            if len(pts) != 2:
                if '可购买热销商品' not in content:
                    logging.error(content)
                    logging.error("NEW PATTERN ABOVE")
            reach_num = discount = free_num = rf_ratio = None
            reach_num = float(pts[0])
            if deduct_type==0:
                discount = pts[1]
            elif deduct_type==1:
                free_num = float(pts[1])
                rf_ratio = float(free_num*1.0/reach_num)

            # tp19 =[sku_id, dt, title, price, deduct_type, reach_num, discount, free_num, rf_ratio, category_id, category_name, pid, code, name, content, adurl, origin_dt]
            tp19 =[sku_id, dt, price, deduct_type, reach_num, discount, free_num, rf_ratio, category_id, category_name, pid, code, name, content, adurl, origin_dt]
            vlist19.append(tp19)


        else:
            pass

    logging.debug("code = 15, cases = %s" %num_15)
    logging.debug("code = 15, repeated = %s" %num_15_repeated)
    logging.debug("rows to insert = %s" %len(vlist) )

    sql_cb_deduction = '''
        CREATE TABLE jd_analytic_promo_deduction_latest (
          sku_id bigint(20) NOT NULL,
          add_time datetime NOT NULL,
          -- title varchar(255) NOT NULL,
          price float NOT NULL,
          is_repeat tinyint(4) NOT NULL,
          reach float NOT NULL,
          deduction float NOT NULL,
          max_deduction float NOT NULL,
          dr_ratio float NOT NULL,
          maxp_ratio float NOT NULL,
          single_discount_rate float NOT NULL,
          category_id varchar(255) NOT NULL,
          category_name varchar(255) DEFAULT NULL,
          pid varchar(255) NOT NULL,
          code varchar(255) NOT NULL,
          name varchar(255) NOT NULL,
          content varchar(255) NOT NULL,
          adurl varchar(255) DEFAULT NULL,
          origin_time datetime NOT NULL,
          KEY skuid (sku_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    sql_cb_discount = '''
        CREATE TABLE jd_analytic_promo_discount_latest (
          sku_id bigint(20) NOT NULL,
          add_time datetime NOT NULL,
          -- title varchar(255) DEFAULT NULL,
          price float DEFAULT NULL,
          deduct_type smallint(6) DEFAULT NULL,
          reach_num smallint(6) DEFAULT NULL,
          discount float DEFAULT NULL,
          free_num smallint(6) DEFAULT NULL,
          rf_ratio float DEFAULT NULL,
          category_id varchar(255) DEFAULT NULL,
          category_name varchar(255) DEFAULT NULL,
          pid varchar(255) NOT NULL,
          code varchar(255) NOT NULL,
          name varchar(255) NOT NULL,
          content varchar(255) NOT NULL,
          adurl varchar(255) DEFAULT NULL,
          origin_dt datetime DEFAULT NULL,
          PRIMARY KEY (sku_id,pid),
          KEY skuid (sku_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    pret15 = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_promo_deduction',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=False,
        sql_create_table=sql_cb_deduction,
    )

    logging.debug("code = 19, cases = %s" %num_19 )
    logging.debug("rows to insert = %s" %len(vlist19) )

    pret19 = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_promo_discount',
        num_cols=len(vlist19[0]),
        value_list=vlist19,
        is_many=True,
        need_history=False,
        sql_create_table=sql_cb_discount,
    )

    return _generate_mixed_ret([pret15, pret19])


if __name__ == "__main__":
    from tasks import task_logging
    task_logging.configLogging('debug_promo_item_trans')
    # print(processItemPromo())
    # print(process_gift_value())
    print(process_promo_detail())

    pass