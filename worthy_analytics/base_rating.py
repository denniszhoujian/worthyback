# encoding: utf-8

from datasys import dbhelper
import time
from datasys import timeHelper
from datasys import crawler_helper

def calculate_base_rating_for_categories():

    today = timeHelper.getNow()
    sql = getSqlCatRating()
    retrows = dbhelper.executeSqlRead(sql)
    print sql
    print "rows of data selected for insert: %s" %len(retrows)
    print len(retrows[0])
    # print retrows[0]
    vlist = []
    for row in retrows:
        tp = []
        tp.append(row['category_id'])
        tp.append(row['sample_count'])
        tp.append(row['sum_1'])
        tp.append(row['sum_2'])
        tp.append(row['sum_3'])
        tp.append(row['sum_4'])
        tp.append(row['sum_5'])
        tp.append(row['comment_count'])
        tp.append(row['rate_1'])
        tp.append(row['rate_2'])
        tp.append(row['rate_3'])
        tp.append(row['rate_4'])
        tp.append(row['rate_5'])
        tp.append(row['rate_good'])
        tp.append(row['rate_bad'])
        tp.append(row['origin_dt'])
        tp.append(row['dt'])
        tp.append(row['name'])
        # print row['category_id']
        vlist.append(tp)

    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_analytic_category_rating',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True
    )
    # print "rows affected, (1): %s, (2): %s" %(afr1, afr2)


def getSqlCatRating():

    today = timeHelper.getNow()
    sql  = '''
        select e.*,'%s' as dt,c.name from (
        select
        category_id,
        count(1) as sample_count,
        sum(a.Score1Count) as sum_1,
        sum(a.Score2Count) as sum_2,
        sum(a.Score3Count) as sum_3,
        sum(a.Score4Count) as sum_4,
        sum(a.Score5Count) as sum_5,
        sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count) as comment_count,
        sum(a.Score1Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_1,
        sum(a.Score2Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_2,
        sum(a.Score3Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_3,
        sum(a.Score4Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_4,
        sum(a.Score5Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_5,
        sum(a.Score5Count+a.Score4Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_good,
        sum(a.Score1Count+a.Score2Count)/(sum(a.Score1Count+a.Score2Count+a.Score3Count+a.Score4Count+a.Score5Count)+1) as rate_bad,
        max(a.dt) as origin_dt

        from

        (select * from jd_item_comment_count_latest where CommentCount>100) a
        left join
        jd_item_category b
        on a.SkuId = b.sku_id
        -- where a.dt > '2015-10-1'

        group by b.category_id
        ) e
        left JOIN
        jd_category c
        on e.category_id = c.id

    ''' %(today)
    return sql

def test():
    print "test"

if __name__ == "__main__":

    while True:
        print 'job start: %s' %timeHelper.getNowLong()
        t1 = time.time()
        ret = calculate_base_rating_for_categories()
        print ret
        t2 = time.time()
        print "Finished in seconds: %s" %(t2-t1)

        remaining = timeHelper.getTimeLeftTillTomorrow()
        print "now sleeping for hours: %s" %(remaining/3600)

        time.sleep(remaining)
