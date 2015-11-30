# encoding: utf-8

import dbhelper
import MySQLdb
import time
import logging


def persist_db_history_and_latest(table_name, num_cols, value_list, is_many=True, need_history=False, need_flow=False):
    tbl_latest = '%s_latest' %table_name
    ps_list = []
    for i in xrange(num_cols):
        ps_list.append('%s')
    values_str = ','.join(ps_list)

    t1 = time.time()
    tcur = t1
    affected_rows = 99999
    affected_rows3 = 99999
    if need_history:
        sql = 'replace into %s values(%s)' %(table_name,values_str)
        affected_rows = dbhelper.executeSqlWriteMany(sql,value_list,is_dirty=True)
        t2 = time.time()
        tcur = t2
        logging.debug('persist_db_history_and_latest, history using time: %s' %(t2-t1))
    if need_flow:
        sql = 'replace into %s values(%s)' %(table_name+'_flow',values_str)
        affected_rows3 = dbhelper.executeSqlWriteMany(sql,value_list,is_dirty=True)
        t21 = time.time()
        logging.debug('persist_db_history_and_latest, flow using time: %s' %(t21-tcur))
        tcur = t21
    sql2 = 'replace into %s values(%s)' %(tbl_latest,values_str)
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,value_list,is_dirty=True)
    t3 = time.time()
    logging.debug('persist_db_history_and_latest, latest using time: %s' %(t3-tcur))
    status = -1
    if affected_rows>0 and affected_rows2>0 and affected_rows3>0:
        status = 0
    ret = {
        'status':status,
        'affected_rows_latest': affected_rows2,
        'affected_rows_history': affected_rows,
        'affected_rows_flow': affected_rows3,
    }
    return ret

def persist_db_history_and_lastest_empty_first(table_name, num_cols, value_list, is_many=True, need_history=False, sql_create_table=None):

    ret = {
        'status':-1,
        'deleted_rows': -1,
        'affected_rows_latest':-1,
        'affected_rows':-1
    }

    tbl_latest = '%s_latest' %table_name
    ps_list = []
    for i in xrange(num_cols):
        ps_list.append('%s')
    values_str = ','.join(ps_list)

    sql_empty = 'drop table if exists %s' %tbl_latest
    if sql_create_table is None:
        sql_empty = 'delete from %s' %tbl_latest
    print sql_empty

    sql = 'replace into %s values(%s)' %(table_name,values_str)
    sql2 = 'replace into %s values(%s)' %(tbl_latest,values_str)

    conn = dbhelper.getConnection()
    affected_rows = 0
    try:
        cursor1 = conn.cursor()
        cursor1.execute('set @@session.tx_isolation="serializable"')
        t1 = time.time()
        afr1 = cursor1.execute(sql_empty)
        t2 = time.time()
        afr15 = -1
        if sql_create_table is not None:
            afr15 = cursor1.execute(sql_create_table)
        afr2 = cursor1.executemany(sql2, value_list)
        t3 = time.time()
        afr3 = 0
        if need_history:
            afr3 = cursor1.executemany(sql,value_list)
        conn.commit()
        t4 = time.time()
        affected_rows = cursor1.rowcount
        ret = {
            'status':0,
            'deleted_rows': afr1,
            'affected_rows_latest':afr2,
            'affected_rows':afr3
        }
        print 'Rows deleted: %s\nRows added latest: %s\nRows added: %s' %(afr1,afr2,afr3)
        print 'delete data using seconds: %0.1f' %(t2-t1)
        print 'inserting data using seconds: %0.1f' %(t3-t2)
        print 'commit using seconds: %0.1f' %(t4-t3)
    except Exception as e:
        conn.rollback()
        print e
        return ret
    finally:
        conn.close()
    return ret


if __name__ == '__main__':
    persist_db_history_and_latest('ok',5,[])