# encoding: utf-8

import dbhelper
import MySQLdb

def persist_db_history_and_latest(table_name, num_cols, value_list, is_many=True, need_history=False):
    tbl_latest = '%s_latest' %table_name
    ps_list = []
    for i in xrange(num_cols):
        ps_list.append('%s')
    values_str = ','.join(ps_list)

    affected_rows = 99999
    if need_history:
        sql = 'replace into %s values(%s)' %(table_name,values_str)
        affected_rows = dbhelper.executeSqlWriteMany(sql,value_list)
    sql2 = 'replace into %s values(%s)' %(tbl_latest,values_str)
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,value_list)
    status = -1
    if affected_rows>0 and affected_rows2>0:
        status = 0
    ret = {
        'status':status,
        'affected_rows':affected_rows,
        'affected_rows2':affected_rows2
    }
    return ret

def persist_db_history_and_lastest_empty_first(table_name, num_cols, value_list, is_many=True, need_history=False):

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

    sql_empty = 'delete from %s' %tbl_latest
    sql = 'replace into %s values(%s)' %(table_name,values_str)
    sql2 = 'replace into %s values(%s)' %(tbl_latest,values_str)

    conn = dbhelper.getConnection()
    affected_rows = 0
    try:
        cursor1 = conn.cursor()
        afr1 = cursor1.execute(sql_empty)
        afr2 = cursor1.executemany(sql2, value_list)
        afr3 = 0
        if need_history:
            afr3 = cursor1.executemany(sql,value_list)
        conn.commit()
        affected_rows = cursor1.rowcount
        ret = {
            'status':0,
            'deleted_rows': afr1,
            'affected_rows_latest':afr2,
            'affected_rows':afr3
        }
        print 'Rows deleted: %s\nRows added latest: %s\nRows added: %s' %(afr1,afr2,afr3)
    except Exception as e:
        conn.rollback()
        print e
        return ret
    finally:
        conn.close()
    return ret


if __name__ == '__main__':
    persist_db_history_and_latest('ok',5,[])